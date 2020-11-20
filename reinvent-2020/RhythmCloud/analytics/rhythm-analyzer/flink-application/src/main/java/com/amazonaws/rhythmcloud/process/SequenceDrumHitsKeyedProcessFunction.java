package com.amazonaws.rhythmcloud.process;

import com.amazonaws.rhythmcloud.Constants;
import com.amazonaws.rhythmcloud.domain.DrumHitReading;
import com.amazonaws.rhythmcloud.domain.DrumHitReadingWithId;
import lombok.extern.slf4j.Slf4j;
import org.apache.flink.api.common.state.MapState;
import org.apache.flink.api.common.state.MapStateDescriptor;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.api.common.typeutils.TypeSerializer;
import org.apache.flink.api.common.typeutils.base.ListSerializer;
import org.apache.flink.api.common.typeutils.base.LongSerializer;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;

import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;

@Slf4j
public class SequenceDrumHitsKeyedProcessFunction
    extends KeyedProcessFunction<String, DrumHitReading, DrumHitReadingWithId> {
  private static final String DRUM_HIT_QUEUE_STATE_NAME = "drumHitQueue";
  private static final String DRUM_HIT_SEQUENCE_STATE_NAME = "drumHitSequence";

  private final Constants.Stream type;
  private final boolean isObjectReuseEnabled;
  /*
   * The input type serializer for buffering events to managed state.
   */
  private final TypeSerializer<DrumHitReading> drumHitReadingTypeSerializer;

  /*
   * The queue of input elements keyed by event timestamp.
   */
  private transient MapState<Long, List<DrumHitReading>> windowState;

  /*
   * Sequence number state.
   */
  private transient ValueState<Long> sequenceState;
  /*
  The last seen watermark.
  This will be used to decide if an incoming element is late or not.
  */
  long lastWatermark = Long.MIN_VALUE;

  public SequenceDrumHitsKeyedProcessFunction(
      Constants.Stream type,
      TypeSerializer<DrumHitReading> drumHitReadingTypeSerializer,
      boolean isObjectReuseEnabled) {
    this.type = type;
    this.drumHitReadingTypeSerializer = drumHitReadingTypeSerializer;
    this.isObjectReuseEnabled = isObjectReuseEnabled;
  }
  /*
  processElement() receives input events one by one. You can react to each input
  by producing one or more output events to the next operator by calling
  out.collect(someOutput). You can also pass data to a side output or ignore
  a particular input altogether.

  onTimer() is called by Flink when a previously-registered timer fires.
  Both event time and processing time timers are supported.

  open() is equivalent to a constructor. It is called inside of the
   TaskManager’s JVM, and is used for initialization, such as registering
   Flink-managed state. It is also the right place to initialize fields
   that are not serializable and cannot be transferred from the JobManager’s JVM.
   */

  @Override
  public void onTimer(long timestamp, OnTimerContext context, Collector<DrumHitReadingWithId> out)
      throws Exception {
    super.onTimer(timestamp, context, out);

    log.info("Timer registered at {} has fired", timestamp);
    Long watermark = context.timerService().currentWatermark();
    PriorityQueue<Long> sortedTimestamps = getSortedTimestamps();
    Long sequenceNumber = sequenceState.value();
    if (sequenceNumber == null || sequenceNumber.equals(0L)) {
      sequenceNumber = 1L;
    }
    while (!sortedTimestamps.isEmpty() && sortedTimestamps.peek() <= watermark) {
      long sortedTimestamp = sortedTimestamps.poll();
      for (DrumHitReading drumHitReading : windowState.get(sortedTimestamp)) {
        out.collect(
            new DrumHitReadingWithId(
                drumHitReading.getSessionId(),
                drumHitReading.getDrum(),
                drumHitReading.getTimestamp(),
                drumHitReading.getVoltage(),
                sequenceNumber,
                this.type));
        sequenceNumber += 1;
        sequenceState.update(sequenceNumber);
        log.info("Emitting {}", drumHitReading.toString());
      }
      windowState.remove(sortedTimestamp);
    }

    if (sortedTimestamps.isEmpty()) {
      windowState.clear();
    }

    if (!sortedTimestamps.isEmpty()) {
      // protect against overflow
      if (watermark + 1 > watermark) {
        context.timerService().registerEventTimeTimer(watermark + 1);
      }
    }
  }

  @Override
  public void open(Configuration parameters) throws Exception {
    super.open(parameters);
    // create a map-based queue to buffer input elements
    if (windowState == null) {
      windowState =
          getRuntimeContext()
              .getMapState(
                  new MapStateDescriptor<>(
                      DRUM_HIT_QUEUE_STATE_NAME,
                      LongSerializer.INSTANCE,
                      new ListSerializer<>(this.drumHitReadingTypeSerializer)));
    }

    // create a value state
    if (sequenceState == null) {
      sequenceState =
          getRuntimeContext()
              .getState(new ValueStateDescriptor<>(DRUM_HIT_SEQUENCE_STATE_NAME, Types.LONG));
    }
  }

  @Override
  public void processElement(
      DrumHitReading drumHitReading, Context context, Collector<DrumHitReadingWithId> collector)
      throws Exception {
    // Add hit to state
    long currentEventTime = drumHitReading.getTimestamp();
    // In event-time processing we assume correctness of the watermark.
    // Events with timestamp smaller than (or equal to) the
    // last seen watermark are considered late.
    // TODO: Add late arriving data to side output
    if (currentEventTime > lastWatermark) {
      log.info("Adding to state: {}", drumHitReading.toString());
      addToStateValuesList(
          windowState,
          currentEventTime,
          drumHitReading,
          this.isObjectReuseEnabled,
          this.drumHitReadingTypeSerializer);

      // Register the event timer
      context.timerService().registerEventTimeTimer(context.timerService().currentWatermark() + 1);
    }
  }

  private static <K, V> void addToStateValuesList(
      MapState<K, List<V>> mapState,
      K key,
      V value,
      boolean isObjectReuseEnabled,
      TypeSerializer<V> drumHitReadingTypeSerializer)
      throws Exception {
    List<V> valuesList = mapState.get(key);
    if (valuesList == null) {
      valuesList = new ArrayList<>();
    }
    if (isObjectReuseEnabled) {
      // copy the object so that the original object may be reused
      valuesList.add(drumHitReadingTypeSerializer.copy(value));
    } else {
      valuesList.add(value);
    }
    mapState.put(key, valuesList);
  }

  /**
   * Gets the sorted timestamps of any buffered events.
   *
   * @return a sorted list of timestamps that have at least one buffered event.
   */
  private PriorityQueue<Long> getSortedTimestamps() throws Exception {
    PriorityQueue<Long> sortedTimestamps = new PriorityQueue<>(10);
    for (Long timestamp : windowState.keys()) {
      sortedTimestamps.offer(timestamp);
    }
    return sortedTimestamps;
  }
}
