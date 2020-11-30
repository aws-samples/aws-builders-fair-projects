package com.amazonaws.rhythmcloud;

import com.amazonaws.rhythmcloud.domain.DrumHitReading;
import com.amazonaws.rhythmcloud.domain.DrumHitReadingResult;
import com.amazonaws.rhythmcloud.domain.DrumHitReadingWithId;
import com.amazonaws.rhythmcloud.io.BoundedOutOfOrdernessGenerator;
import com.amazonaws.rhythmcloud.io.Kinesis;
import com.amazonaws.rhythmcloud.io.TimestreamPoint;
import com.amazonaws.rhythmcloud.process.SequenceDrumHitsKeyedProcessFunction;
import com.amazonaws.services.kinesisanalytics.runtime.KinesisAnalyticsRuntime;
import com.twitter.chill.protobuf.ProtobufSerializer;
import lombok.extern.slf4j.Slf4j;
import org.apache.flink.api.common.functions.FilterFunction;
import org.apache.flink.api.common.functions.JoinFunction;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.api.java.functions.KeySelector;
import org.apache.flink.streaming.api.CheckpointingMode;
import org.apache.flink.streaming.api.TimeCharacteristic;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.EventTimeSessionWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import software.amazon.awssdk.services.timestreamwrite.model.MeasureValueType;

import java.util.Map;
import java.util.Properties;

@Slf4j
public class TemporalAnalyzer {
  public static void main(String[] args) throws Exception {
    try {
      log.info("Starting the rhythm analyzer");
      final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
      /*
      EventTime
         Event time means that the time is determined by the event's individual custom timestamp.
      IngestionTime
         Ingestion time means that the time is determined when the element enters the Flink streaming data flow.
      ProcessingTime
         Processing time for operators means that the operator uses the system clock of the machine to determine the
         current time of the data stream.
      */
      env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);
      /*
      https://www.bookstack.cn/read/Flink-1.10-en/4836c4072c95392f.md

      Flink’s checkpointing enabled, the Flink Kinesis Consumer will consume
      records from shards in Kinesis streams and periodically checkpoint
      each shard’s progress. In case of a job failure, Flink will restore the streaming
      program to the state of the latest complete checkpoint and re-consume
      the records from Kinesis shards.
      */
      env.enableCheckpointing(
          5_000L, CheckpointingMode.EXACTLY_ONCE); // checkpoint every 5000L- 5 seconds

      /*
      Register the serializers
       */
      env.getConfig()
          .registerTypeWithKryoSerializer(DrumHitReading.class, ProtobufSerializer.class);
      env.getConfig()
          .registerTypeWithKryoSerializer(DrumHitReadingWithId.class, ProtobufSerializer.class);

      Map<String, Properties> properties = KinesisAnalyticsRuntime.getApplicationProperties();

      /*
      The FlinkKinesisConsumer is an exactly-once parallel streaming data source
      that subscribes to multiple AWS Kinesis streams within the same AWS service region,
      and can transparently handle resharding of streams while the job is running.
      Each subtask of the consumer is responsible for fetching data records
      from multiple Kinesis shards. The number of shards fetched by each subtask will
      change as shards are closed and created by Kinesis.
      If streaming topologies choose to use the event time notion for record timestamps,
      an approximate arrival timestamp will be used by default.
      This timestamp is attached to records by Kinesis once they were successfully
      received and stored by streams. Note that this timestamp is typically
      referred to as a Kinesis server-side timestamp, and there are no guarantees
      about the accuracy or order correctness. You can override this default with a
      custom timestamp.

      In order to work with event time, Flink needs to know the events timestamps, meaning each element in the
      stream needs to have the event timestamp assigned. This is done by accessing/extracting the timestamp
      from some field in the element by using a TimstampAssigner.

      Watermarks tells the system about progress in event time. This is done by specifying WatermarkGenerator.
       */
      DataStream<DrumHitReading> systemHitSource =
          Kinesis.createSourceFromConfig(Constants.Stream.SYSTEMHIT, properties, env);
      DataStream<DrumHitReading> userHitSource =
          Kinesis.createSourceFromConfig(Constants.Stream.USERHIT, properties, env);

      // Assume events will be out of order because MQTT, AWS IoT Core does not
      // guarantee order of events
      SingleOutputStreamOperator<DrumHitReading> withTimestampAndWatermarkSystemHitSource =
          systemHitSource.assignTimestampsAndWatermarks(new BoundedOutOfOrdernessGenerator());
      SingleOutputStreamOperator<DrumHitReading> withTimestampAndWatermarkUserHitSource =
          userHitSource.assignTimestampsAndWatermarks(new BoundedOutOfOrdernessGenerator());

      // Isolate metronome beat
      SingleOutputStreamOperator<DrumHitReading> metronomeHitStream =
          withTimestampAndWatermarkSystemHitSource
              .filter(
                  (FilterFunction<DrumHitReading>)
                      drumHitReading -> (drumHitReading.getDrum().equalsIgnoreCase("metronome")))
              .name("Metronome Stream");

      // Read the system hit stream without the metronome beat
      // Since the system hit and user hit have to be overlapped
      // the window has to be shifted to the point where the user
      // starts playing the drum. Though we could potentially use
      // EventSessionWindow, we are choosing to roll our own
      // window using the KeyedWindowProcess function.
      SingleOutputStreamOperator<DrumHitReadingWithId> systemHitStream =
          withTimestampAndWatermarkSystemHitSource
              .filter(
                  (FilterFunction<DrumHitReading>)
                      drumHitReading -> (!drumHitReading.getDrum().equalsIgnoreCase("metronome")))
              .keyBy(
                  drumHitReading ->
                      String.format(
                          "%d-%d",
                          drumHitReading.getSessionId(),
                          Constants.Stream.SYSTEMHIT.getStreamCode()))
              .process(
                  new SequenceDrumHitsKeyedProcessFunction(
                      Constants.Stream.SYSTEMHIT,
                      TypeInformation.of(DrumHitReading.class).createSerializer(env.getConfig()),
                      env.getConfig().isObjectReuseEnabled()))
              .name("System Hit Stream");

      SingleOutputStreamOperator<DrumHitReadingWithId> userHitStream =
          withTimestampAndWatermarkUserHitSource
              .keyBy(
                  drumHitReading ->
                      String.format(
                          "%d-%d",
                          drumHitReading.getSessionId(), Constants.Stream.USERHIT.getStreamCode()))
              .process(
                  new SequenceDrumHitsKeyedProcessFunction(
                      Constants.Stream.USERHIT,
                      TypeInformation.of(DrumHitReading.class).createSerializer(env.getConfig()),
                      env.getConfig().isObjectReuseEnabled()))
              .name("User Hit Stream");

      DataStream<DrumHitReadingResult> resultDataStream =
          systemHitStream
              .keyBy(DrumHitReadingWithId::getSessionId)
              .join(userHitStream.keyBy(DrumHitReadingWithId::getSessionId))
              .where((KeySelector<DrumHitReadingWithId, Long>) DrumHitReadingWithId::getId)
              .equalTo((KeySelector<DrumHitReadingWithId, Long>) DrumHitReadingWithId::getId)
              .window(EventTimeSessionWindows.withGap(Time.minutes(1L)))
              .apply(
                  (JoinFunction<DrumHitReadingWithId, DrumHitReadingWithId, DrumHitReadingResult>)
                      (system, user) ->
                          new DrumHitReadingResult(
                              system.getSessionId(),
                              system.getId(),
                              system.getDrum(),
                              user.getDrum(),
                              system.getTimestamp(),
                              user.getTimestamp(),
                              user.getVoltage(),
                              system.getDrum().equalsIgnoreCase(user.getDrum()) ? 10L : 0L));

      resultDataStream
          .map((MapFunction<DrumHitReadingResult, String>) DrumHitReadingResult::toString)
          .addSink(
              Kinesis.createKinesisSinkFromConfig(
                  Constants.Stream.TEMPORALANALYSIS, properties, env));

      resultDataStream
          .map(
              (MapFunction<DrumHitReadingResult, TimestreamPoint>)
                  drumHitReadingResult -> {
                    TimestreamPoint timestreamPoint = new TimestreamPoint();
                    timestreamPoint.setMeasureName("score");
                    timestreamPoint.setMeasureValue(drumHitReadingResult.getScore().toString());
                    timestreamPoint.setMeasureValueType(MeasureValueType.BIGINT);
                    timestreamPoint.setTime(drumHitReadingResult.getUserTimestamp());
                    timestreamPoint.setTimeUnit("NANOSECONDS");
                    timestreamPoint.addDimension(
                        "session_id", drumHitReadingResult.getSessionId().toString());
                    timestreamPoint.addDimension(
                        "sequence_id", drumHitReadingResult.getSequenceId().toString());
                    timestreamPoint.addDimension(
                        "system_drum", drumHitReadingResult.getSystemDrum());
                    timestreamPoint.addDimension("user_drum", drumHitReadingResult.getUserDrum());
                    timestreamPoint.addDimension(
                        "voltage", drumHitReadingResult.getUserVoltage().toString());

                    return timestreamPoint;
                  })
          .addSink(Kinesis.createTimeSinkFromConfig(Constants.Stream.TIMESTREAM, properties, env));

      env.execute("Temporal Analyzer");
    } catch (Exception err) {
      log.error("Temporal analyzer failed", err);
    }
  }
}
