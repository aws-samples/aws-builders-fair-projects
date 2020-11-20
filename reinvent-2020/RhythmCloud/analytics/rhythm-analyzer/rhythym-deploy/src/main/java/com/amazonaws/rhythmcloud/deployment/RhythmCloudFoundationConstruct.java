package com.amazonaws.rhythmcloud.deployment;

import software.amazon.awscdk.core.CfnOutput;
import software.amazon.awscdk.core.Construct;
import software.amazon.awscdk.services.kinesis.CfnStream;
import software.amazon.awscdk.services.s3.Bucket;
import software.amazon.awscdk.services.s3.IBucket;

public class RhythmCloudFoundationConstruct extends Construct {
    CfnStream rhythmCloudSystemHitStream;
    CfnStream rhythmCloudUserHitStream;
    CfnStream rhythmCloudAnalysisOutputStream;
    IBucket rhythmCloudArtifactRepository;

    public RhythmCloudFoundationConstruct(Construct scope,
                                          String id,
                                          final RhythymCloudFoundationProps props) {
        super(scope, id);

        rhythmCloudArtifactRepository = Bucket.fromBucketArn(
                this,
                "rhythm-cloud-artifacts-s3-bucket",
                props.getRhythmCloudArtifactsBucketArn());

        rhythmCloudSystemHitStream = CfnStream.Builder.create(this, "rhythm-cloud-system-hit-stream")
                .name("rhythm-cloud-system-hit-stream")
                .shardCount(1)
                .retentionPeriodHours(24)
                .build();

        rhythmCloudUserHitStream = CfnStream.Builder.create(this, "rhythm-cloud-user-hit-stream")
                .name("rhythm-cloud-user-hit-stream")
                .shardCount(1)
                .retentionPeriodHours(24)
                .build();

        rhythmCloudAnalysisOutputStream = CfnStream.Builder.create(this, "rhythm-cloud-analysis-output-stream")
                .name("rhythm-cloud-analysis-output-stream")
                .shardCount(1)
                .retentionPeriodHours(24)
                .build();

        CfnOutput.Builder.create(this, "rhythm-artifacts-s3-bucket-output")
                .exportName("rhythm-artifacts-s3-bucket-output")
                .description("Bucket containing all the Rhythm Cloud artifacts")
                .value(rhythmCloudArtifactRepository.getBucketArn())
                .build();

        CfnOutput.Builder.create(this, "rhythm-analysis-output-stream-output")
                .exportName("rhythm-analysis-output-stream-output")
                .description("Output Kinesis Stream ARN")
                .value(rhythmCloudAnalysisOutputStream.getAttrArn())
                .build();

        CfnOutput.Builder.create(this, "rhythm-system-hit-stream-output")
                .exportName("rhythm-system-hit-stream-output")
                .description("System Hit Kinesis Stream ARN")
                .value(rhythmCloudSystemHitStream.getAttrArn())
                .build();

        CfnOutput.Builder.create(this, "rhythm-user-hit-stream-output")
                .exportName("rhythm-user-hit-stream-output")
                .description("User Hit Kinesis Stream ARN")
                .value(rhythmCloudUserHitStream.getAttrArn())
                .build();
    }

    public IBucket getRhythmCloudArtifactRepository() {
        return rhythmCloudArtifactRepository;
    }

    public CfnStream getRhythmCloudSystemHitStream() {
        return rhythmCloudSystemHitStream;
    }

    public CfnStream getRhythmCloudUserHitStream() {
        return rhythmCloudUserHitStream;
    }

    public CfnStream getRhythmCloudAnalysisOutputStream() {
        return rhythmCloudAnalysisOutputStream;
    }
}
