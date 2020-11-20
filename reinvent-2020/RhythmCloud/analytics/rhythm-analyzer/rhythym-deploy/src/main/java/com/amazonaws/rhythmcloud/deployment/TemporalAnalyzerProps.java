package com.amazonaws.rhythmcloud.deployment;

import software.amazon.awscdk.services.kinesis.CfnStream;
import software.amazon.awscdk.services.s3.IBucket;

public interface TemporalAnalyzerProps {
    public static Builder builder() {
        return new Builder();
    }

    IBucket getRhythmCloudArtifactsBucket();

    CfnStream getRhythmCloudSystemHitStream();

    CfnStream getRhythmCloudUserHitStream();

    CfnStream getRhythmCloudAnalysisOutputStream();

    String getContentPath();

    public static class Builder {
        private IBucket rhythmCloudArtifactsBucket;
        private CfnStream rhythmCloudSystemHitStream;
        private CfnStream rhythmCloudUserHitStream;
        private CfnStream rhythmCloudAnalysisOutputStream;
        private String contentPath;

        public Builder setRhythmCloudSystemHitStream(CfnStream stream) {
            this.rhythmCloudSystemHitStream = stream;
            return this;
        }

        public Builder setRhythmCloudUserHitStream(CfnStream stream) {
            this.rhythmCloudUserHitStream = stream;
            return this;
        }

        public Builder setRhythmCloudAnalysisOutputStream(CfnStream stream) {
            this.rhythmCloudAnalysisOutputStream = stream;
            return this;
        }

        public Builder setRhythmCloudArtifactsBucket(IBucket bucket) {
            this.rhythmCloudArtifactsBucket = bucket;
            return this;
        }

        public Builder setContentPath(String contentPath) {
            this.contentPath = contentPath;
            return this;
        }

        public TemporalAnalyzerProps build() {
            if (this.rhythmCloudArtifactsBucket == null) {
                throw new NullPointerException("The rhythm cloud artifacts bucket property is required.");
            }
            if (this.rhythmCloudSystemHitStream == null) {
                throw new NullPointerException("The rhythm cloud system hit stream property is required.");
            }
            if (this.rhythmCloudUserHitStream == null) {
                throw new NullPointerException("The rhythm cloud user hit stream property is required.");
            }
            if (this.rhythmCloudAnalysisOutputStream == null) {
                throw new NullPointerException("The rhythm cloud analysis output stream property is required.");
            }
            if (this.contentPath == null || this.contentPath.isEmpty()) {
                throw new NullPointerException("The content path property is required.");
            }

            return new TemporalAnalyzerProps() {
                @Override
                public IBucket getRhythmCloudArtifactsBucket() {
                    return rhythmCloudArtifactsBucket;
                }

                @Override
                public CfnStream getRhythmCloudSystemHitStream() {
                    return rhythmCloudSystemHitStream;
                }

                @Override
                public CfnStream getRhythmCloudUserHitStream() {
                    return rhythmCloudUserHitStream;
                }

                @Override
                public CfnStream getRhythmCloudAnalysisOutputStream() {
                    return rhythmCloudAnalysisOutputStream;
                }

                @Override
                public String getContentPath() {
                    return contentPath;
                }
            };
        }
    }
}
