package com.amazonaws.rhythmcloud;

import lombok.extern.slf4j.Slf4j;
import org.apache.flink.streaming.connectors.kinesis.config.ConsumerConfigConstants;

@Slf4j
public final class Constants {
    public static final String DEFAULT_REGION_NAME = "us-east-1";

    public static final String STREAM_LATEST_POSITION = "LATEST";

    public static final String STREAM_POLL_INTERVAL = "1000";
    public static final String TIMESTREAM_DB_NAME = "rhythm_cloud";
    public static final String TIMESTREAM_DB_TABLE_NAME = "rhythm";
    public static final String TIMESTREAM_DB_BATCH_SIZE = "1000";

    public enum Stream {
        SYSTEMHIT(1),
        USERHIT(2),
        TEMPORALANALYSIS(3),
        TIMESTREAM(4);

        private final int streamCode;

        Stream(int streamCode) {
            this.streamCode = streamCode;
        }

        public int getStreamCode() {
            return this.streamCode;
        }
    }

    public static String getPropertyGroupName(Stream stream) {
        String propertyGroupName = null;
        switch (stream) {
            case SYSTEMHIT:
                propertyGroupName = "SYSTEMHIT";
                break;
            case USERHIT:
                propertyGroupName = "USERHIT";
                break;
            case TEMPORALANALYSIS:
                propertyGroupName = "TEMPORALANALYSIS";
                break;
            case TIMESTREAM:
                propertyGroupName = "TIMESTREAM";
                break;
        }
        return propertyGroupName;
    }

    public static String getStreamName(Stream stream) {
        String streamName = null;
        switch (stream) {
            case SYSTEMHIT:
                streamName = "rhythm-cloud-system-hit-stream";
                break;
            case USERHIT:
                streamName = "rhythm-cloud-user-hit-stream";
                break;
            case TEMPORALANALYSIS:
                streamName = "rhythm-cloud-analysis-output-stream";
                break;
        }
        return streamName;
    }
}
