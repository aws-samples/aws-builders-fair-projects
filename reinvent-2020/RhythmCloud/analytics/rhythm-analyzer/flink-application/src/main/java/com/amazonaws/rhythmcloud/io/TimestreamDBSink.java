package com.amazonaws.rhythmcloud.io;

import org.apache.flink.api.common.state.ListState;
import org.apache.flink.api.common.state.ListStateDescriptor;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.runtime.state.FunctionInitializationContext;
import org.apache.flink.runtime.state.FunctionSnapshotContext;
import org.apache.flink.streaming.api.checkpoint.CheckpointedFunction;
import org.apache.flink.streaming.api.functions.sink.RichSinkFunction;
import org.apache.flink.util.Preconditions;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import software.amazon.awssdk.core.client.config.ClientOverrideConfiguration;
import software.amazon.awssdk.core.retry.RetryPolicy;
import software.amazon.awssdk.core.retry.backoff.BackoffStrategy;
import software.amazon.awssdk.http.apache.ApacheHttpClient;
import software.amazon.awssdk.services.timestreamwrite.TimestreamWriteClient;
import software.amazon.awssdk.services.timestreamwrite.model.Dimension;
import software.amazon.awssdk.services.timestreamwrite.model.Record;
import software.amazon.awssdk.services.timestreamwrite.model.WriteRecordsRequest;
import software.amazon.awssdk.services.timestreamwrite.model.WriteRecordsResponse;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class TimestreamDBSink extends RichSinkFunction<TimestreamPoint>
    implements CheckpointedFunction {
  private static final Logger LOG = LoggerFactory.getLogger(TimestreamDBSink.class);

  private final TimestreamDBConfig timestreamDBConfig;
  private transient TimestreamWriteClient timestreamWriteClient;
  private List<Record> bufferedRecords;
  private transient ListState<Record> checkpointedState;
  private long emptyListTimestamp;

  public TimestreamDBSink(TimestreamDBConfig timestreamDBConfig) {
    this.timestreamDBConfig =
        Preconditions.checkNotNull(
            timestreamDBConfig, "TimestreamDB client config should not be null");
    this.bufferedRecords = new ArrayList<>();
    this.emptyListTimestamp = System.currentTimeMillis();
  }

  @Override
  public void snapshotState(FunctionSnapshotContext functionSnapshotContext) throws Exception {
    checkpointedState.clear();
    for (Record element : bufferedRecords) {
      checkpointedState.add(element);
    }
  }

  @Override
  public void initializeState(FunctionInitializationContext functionInitializationContext)
      throws Exception {
    ListStateDescriptor<Record> descriptor = new ListStateDescriptor<>("recordList", Record.class);

    checkpointedState =
        functionInitializationContext.getOperatorStateStore().getListState(descriptor);

    if (functionInitializationContext.isRestored()) {
      for (Record element : checkpointedState.get()) {
        bufferedRecords.add(element);
      }
    }
  }

  @Override
  public void open(Configuration parameters) throws Exception {
    super.open(parameters);

    RetryPolicy.Builder retryPolicy =
        RetryPolicy.builder()
            .numRetries(timestreamDBConfig.getMaxErrorRetryLimit())
            .backoffStrategy(BackoffStrategy.defaultThrottlingStrategy());

    ApacheHttpClient.Builder httpClientBuilder =
        ApacheHttpClient.builder().maxConnections(timestreamDBConfig.getMaxConnections());

    ClientOverrideConfiguration.Builder overrideConfig =
        ClientOverrideConfiguration.builder()
            .apiCallAttemptTimeout(Duration.ofMillis(timestreamDBConfig.getRequestTimeout()))
            .retryPolicy(retryPolicy.build());

    this.timestreamWriteClient =
        TimestreamWriteClient.builder()
            .httpClientBuilder(httpClientBuilder)
            .overrideConfiguration(overrideConfig.build())
            .region(timestreamDBConfig.getRegion())
            .build();
  }

  @Override
  public void close() throws Exception {
    super.close();
  }

  @Override
  public void invoke(TimestreamPoint value, Context context) throws Exception {
    // Add the record to the buffer
    List<Dimension> dimensions = new ArrayList<>();
    for (Map.Entry<String, String> entry : value.getDimensions().entrySet()) {
      Dimension dim = Dimension.builder().name(entry.getKey()).value(entry.getValue()).build();
      dimensions.add(dim);
    }
    Record measure =
        Record.builder()
            .dimensions(dimensions)
            .measureName(value.getMeasureName())
            .measureValueType(value.getMeasureValueType())
            .measureValue(value.getMeasureValue())
            .timeUnit(value.getTimeUnit())
            .time(String.valueOf(value.getTime()))
            .build();
    bufferedRecords.add(measure);

    // If buffer is full or time to publish
    if (shouldPublish()) {
      WriteRecordsRequest writeRecordsRequest =
          WriteRecordsRequest.builder()
              .databaseName(this.timestreamDBConfig.getDatabaseName())
              .tableName(this.timestreamDBConfig.getTableName())
              .records(this.bufferedRecords)
              .build();
      try {
        WriteRecordsResponse writeRecordsResponse =
            this.timestreamWriteClient.writeRecords(writeRecordsRequest);
        LOG.debug("writeRecords Status: " + writeRecordsResponse.sdkHttpResponse().statusCode());
        this.bufferedRecords.clear();
        this.emptyListTimestamp = System.currentTimeMillis();
      } catch (Exception e) {
        LOG.error("Error: " + e);
      }
    }
  }

  // Method to validate if record batch should be published.
  // This method would return true if the accumulated records has reached the batch size.
  // Or if records have been accumulated for last RECORDS_FLUSH_INTERVAL_MILLISECONDS time interval.
  private boolean shouldPublish() {
    if (bufferedRecords.size() == timestreamDBConfig.getBatchSize()) {
      LOG.debug("Batch of size " + bufferedRecords.size() + " should get published");
      return true;
    } else if (System.currentTimeMillis() - emptyListTimestamp
        >= timestreamDBConfig.getRecordFlushInterval()) {
      LOG.debug("Records after flush interval should get published");
      return true;
    }
    return false;
  }
}
