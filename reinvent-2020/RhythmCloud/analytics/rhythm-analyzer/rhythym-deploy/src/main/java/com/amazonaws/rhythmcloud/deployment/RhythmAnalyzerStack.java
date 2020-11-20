package com.amazonaws.rhythmcloud.deployment;

import software.amazon.awscdk.core.CfnOutput;
import software.amazon.awscdk.core.Construct;
import software.amazon.awscdk.core.Stack;
import software.amazon.awscdk.core.StackProps;

// TODO: Please make the hard coded values such as bucket arn and content path
public class RhythmAnalyzerStack extends Stack {
    public RhythmAnalyzerStack(final Construct scope, final String id) {
        this(scope, id, null);
    }

    public RhythmAnalyzerStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        RhythymCloudFoundationProps rhythymCloudFoundationProps =
                RhythymCloudFoundationProps.builder()
                        .setRhythmCloudArtifactsBucketArn("arn:aws:s3:::rhythm-cloud-artifacts-v1")
                        .build();
        RhythmCloudFoundationConstruct rhythmCloudFoundationConstruct =
                new RhythmCloudFoundationConstruct(
                        this, "rhythm-cloud-foundation-construct", rhythymCloudFoundationProps);

        TemporalAnalyzerProps temporalAnalyzerProps =
                TemporalAnalyzerProps.builder()
                        .setRhythmCloudArtifactsBucket(
                                rhythmCloudFoundationConstruct.getRhythmCloudArtifactRepository())
                        .setRhythmCloudSystemHitStream(
                                rhythmCloudFoundationConstruct.getRhythmCloudSystemHitStream())
                        .setRhythmCloudUserHitStream(
                                rhythmCloudFoundationConstruct.getRhythmCloudUserHitStream())
                        .setRhythmCloudAnalysisOutputStream(
                                rhythmCloudFoundationConstruct.getRhythmCloudAnalysisOutputStream())
                        .setContentPath("flink-application-0.1-SNAPSHOT.jar")
                        .build();
        new TemporalAnalyzerConstruct(this, "temporal-analyzer-construct", temporalAnalyzerProps);

        CfnOutput.Builder.create(this, "rhythm-artifacts-s3-bucket")
                .exportName("rhythm-artifacts-s3-bucket")
                .description("Bucket containing all the Rhythm Cloud artifacts")
                .value(rhythmCloudFoundationConstruct.getRhythmCloudArtifactRepository().getBucketArn())
                .build();

        CfnOutput.Builder.create(this, "rhythm-analysis-output-stream")
                .exportName("rhythm-analysis-output-stream")
                .description("Output Kinesis Stream ARN")
                .value(rhythmCloudFoundationConstruct.getRhythmCloudAnalysisOutputStream().getAttrArn())
                .build();

        CfnOutput.Builder.create(this, "rhythm-system-hit-stream")
                .exportName("rhythm-system-hit-stream")
                .description("System Hit Kinesis Stream ARN")
                .value(rhythmCloudFoundationConstruct.getRhythmCloudSystemHitStream().getAttrArn())
                .build();

        CfnOutput.Builder.create(this, "rhythm-user-hit-stream")
                .exportName("rhythm-user-hit-stream")
                .description("User Hit Kinesis Stream ARN")
                .value(rhythmCloudFoundationConstruct.getRhythmCloudUserHitStream().getAttrArn())
                .build();
    }
}
