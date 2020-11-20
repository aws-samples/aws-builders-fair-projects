package com.amazonaws.rhythmcloud.io;

import lombok.extern.slf4j.Slf4j;
import org.apache.flink.util.Preconditions;
import software.amazon.awssdk.regions.Region;

import java.io.Serializable;

@Slf4j
public class TimestreamDBConfig implements Serializable {
  private static final long serialVersionUID = 1L;

  private static final long DEFAULT_RECORD_FLUSH_INTERVAL = 60_000L;
  private static final int DEFAULT_BATCH_SIZE = 10_000;
  private static final int DEFAULT_MAX_CONNECTIONS = 5_000;
  private static final int DEFAULT_REQUEST_TIMEOUT = 20_000;
  private static final int DEFAULT_MAX_ERROR_RETRY = 10;
  private static final Region DEFAULT_REGION = Region.US_EAST_1;

  private final int maxConnections;
  private final int requestTimeout;
  private final int maxErrorRetryLimit;
  private final int batchSize;
  private final long recordFlushInterval;
  private final Region region;
  private final String databaseName;
  private final String tableName;

  public TimestreamDBConfig(TimestreamDBConfig.Builder builder) {
    Preconditions.checkArgument(builder != null, "TimestreamDBConfig builder can not be null");
    Preconditions.checkNotNull(builder.getMaxConnections(), "Max connections cannot be null");
    Preconditions.checkNotNull(builder.getRequestTimeout(), "Request timeout cannot be null");
    Preconditions.checkNotNull(
        builder.getMaxErrorRetryLimit(), "Max error retry limit cannot be null");
    Preconditions.checkNotNull(builder.getBatchSize(), "Batch size cannot be null");
    Preconditions.checkNotNull(
        builder.getRecordFlushInterval(), "Record flush interval cannot be null");
    Preconditions.checkNotNull(builder.getRegion(), "Region cannot be null");
    Preconditions.checkNotNull(builder.getDatabaseName(), "Database name cannot be null");
    Preconditions.checkNotNull(builder.getTableName(), "Table name cannot be null");

    this.maxConnections = builder.getMaxConnections();
    this.requestTimeout = builder.getRequestTimeout();
    this.maxErrorRetryLimit = builder.getMaxErrorRetryLimit();
    this.batchSize = builder.getBatchSize();
    this.recordFlushInterval = builder.getRecordFlushInterval();
    this.region = builder.getRegion();
    this.databaseName = builder.getDatabaseName();
    this.tableName = builder.getTableName();
    log.debug("Timestream Configuration <START>");
    log.debug("Timestream Configuration max connections: {}", this.getMaxConnections());
    log.debug("Timestream Configuration request timeout: {}", this.getRequestTimeout());
    log.debug("Timestream Configuration max error retry limit: {}", this.getMaxErrorRetryLimit());
    log.debug("Timestream Configuration batch size: {}", this.getBatchSize());
    log.debug("Timestream Configuration record flush interval: {}", this.getRecordFlushInterval());
    log.debug("Timestream Configuration region: {}", this.getRegion());
    log.debug("Timestream Configuration database name: {}", this.getDatabaseName());
    log.debug("Timestream Configuration table name: {}", this.getTableName());
    log.debug("Timestream Configuration <END>");
  }

  public int getMaxConnections() {
    return maxConnections;
  }

  public int getRequestTimeout() {
    return requestTimeout;
  }

  public int getMaxErrorRetryLimit() {
    return maxErrorRetryLimit;
  }

  public int getBatchSize() {
    return batchSize;
  }

  public long getRecordFlushInterval() {
    return recordFlushInterval;
  }

  public Region getRegion() {
    return region;
  }

  public String getDatabaseName() {
    return databaseName;
  }

  public String getTableName() {
    return tableName;
  }

  /** A builder used to create an instance of a TimestreamDBConfig. */
  public static class Builder {
    private int maxConnections = DEFAULT_MAX_CONNECTIONS;
    private int requestTimeout = DEFAULT_REQUEST_TIMEOUT;
    private int maxErrorRetryLimit = DEFAULT_MAX_ERROR_RETRY;
    private int batchSize = DEFAULT_BATCH_SIZE;
    private long recordFlushInterval = DEFAULT_RECORD_FLUSH_INTERVAL;
    private Region region = DEFAULT_REGION;
    private String databaseName;
    private String tableName;

    public Builder() {}

    public Builder(
        Region region,
        int maxConnections,
        int requestTimeout,
        int maxErrorRetryLimit,
        int batchSize,
        long recordFlushInterval,
        String databaseName,
        String tableName) {
      this.region = region;
      this.maxConnections = maxConnections;
      this.requestTimeout = requestTimeout;
      this.maxErrorRetryLimit = maxErrorRetryLimit;
      this.batchSize = batchSize;
      this.recordFlushInterval = recordFlushInterval;
      this.databaseName = databaseName;
      this.tableName = tableName;
    }

    public TimestreamDBConfig.Builder maxConnections(int maxConnections) {
      this.maxConnections = maxConnections;
      return this;
    }

    public TimestreamDBConfig.Builder requestTimeout(int requestTimeout) {
      this.requestTimeout = requestTimeout;
      return this;
    }

    public TimestreamDBConfig.Builder maxErrorRetryLimit(int maxErrorRetryLimit) {
      this.maxErrorRetryLimit = maxErrorRetryLimit;
      return this;
    }

    public TimestreamDBConfig.Builder region(Region region) {
      this.region = region;
      return this;
    }

    public TimestreamDBConfig.Builder batchSize(int batchSize) {
      this.batchSize = batchSize;
      return this;
    }

    public TimestreamDBConfig.Builder recordFlushInterval(Long recordFlushInterval) {
      this.recordFlushInterval = recordFlushInterval;
      return this;
    }

    public TimestreamDBConfig.Builder databaseName(String databaseName) {
      this.databaseName = databaseName;
      return this;
    }

    public TimestreamDBConfig.Builder tableName(String tableName) {
      this.tableName = tableName;
      return this;
    }

    public TimestreamDBConfig build() {
      return new TimestreamDBConfig(this);
    }

    public int getMaxConnections() {
      return this.maxConnections;
    }

    public int getRequestTimeout() {
      return this.requestTimeout;
    }

    public int getMaxErrorRetryLimit() {
      return this.maxErrorRetryLimit;
    }

    public int getBatchSize() {
      return this.batchSize;
    }

    public long getRecordFlushInterval() {
      return this.recordFlushInterval;
    }

    public String getDatabaseName() {
      return this.databaseName;
    }

    public String getTableName() {
      return this.tableName;
    }

    public Region getRegion() {
      return this.region;
    }
  }
}
