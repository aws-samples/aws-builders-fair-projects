package com.amazonaws.rhythmcloud.deployment;

public interface RhythymCloudFoundationProps {
    public static Builder builder() {
        return new Builder();
    }

    String getRhythmCloudArtifactsBucketArn();

    public static class Builder {
        private String rhythmCloudArtifactsBucketArn;

        public Builder setRhythmCloudArtifactsBucketArn(String rhythmCloudArtifactsBucketArn) {
            this.rhythmCloudArtifactsBucketArn = rhythmCloudArtifactsBucketArn;
            return this;
        }

        public RhythymCloudFoundationProps build() {
            if (this.rhythmCloudArtifactsBucketArn == null ||
                    this.rhythmCloudArtifactsBucketArn.isEmpty()) {
                throw new NullPointerException("The rhythym cloud artifacts bucket arn property is required.");
            }

            return new RhythymCloudFoundationProps() {
                @Override
                public String getRhythmCloudArtifactsBucketArn() {
                    return rhythmCloudArtifactsBucketArn;
                }
            };
        }
    }
}
