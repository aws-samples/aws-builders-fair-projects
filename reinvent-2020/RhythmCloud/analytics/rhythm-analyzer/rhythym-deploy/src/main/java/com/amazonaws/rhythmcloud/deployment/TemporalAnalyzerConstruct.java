package com.amazonaws.rhythmcloud.deployment;

import software.amazon.awscdk.core.Aws;
import software.amazon.awscdk.core.CfnOutput;
import software.amazon.awscdk.core.Construct;
import software.amazon.awscdk.services.iam.*;
import software.amazon.awscdk.services.kinesisanalytics.CfnApplicationCloudWatchLoggingOptionV2;
import software.amazon.awscdk.services.kinesisanalytics.CfnApplicationV2;
import software.amazon.awscdk.services.logs.LogGroup;
import software.amazon.awscdk.services.logs.LogStream;
import software.amazon.awscdk.services.logs.RetentionDays;
import software.amazon.awscdk.services.logs.StreamOptions;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class TemporalAnalyzerConstruct extends Construct {
  private final ManagedPolicy rhythmAnalyzerPolicy;
  private final Role rhythmAnalyzerRole;
  private final CfnApplicationV2 rhythmAnalyzerApplication;
  private final LogGroup rhythmAnalyzerLogGroup;
  private final LogStream rhythmAnalyzerLogStream;

  public TemporalAnalyzerConstruct(
      final Construct scope, final String id, final TemporalAnalyzerProps props) {
    super(scope, id);

    String content =
        String.format(
            "%s/%s", props.getRhythmCloudArtifactsBucket().getBucketArn(), props.getContentPath());
    PolicyStatement s3ReadArtifactPolicy =
        PolicyStatement.Builder.create()
            .sid("ReadCode")
            .effect(Effect.ALLOW)
            .actions(Arrays.asList("s3:GetObject", "s3:GetObjectVersion"))
            .resources(Collections.singletonList(content))
            .build();

    PolicyStatement kinesisMetadataReaderPolicyStatement =
        PolicyStatement.Builder.create()
            .sid("KinesisMetadataReader")
            .effect(Effect.ALLOW)
            .actions(Arrays.asList("kinesis:ListStreams", "kinesis:ListShards"))
            .resources(Collections.singletonList("*"))
            .build();

    PolicyStatement kinesisWriterPolicyStatement =
        PolicyStatement.Builder.create()
            .sid("KinesisWriter")
            .effect(Effect.ALLOW)
            .actions(
                Arrays.asList("kinesis:DescribeStream", "kinesis:PutRecord", "kinesis:PutRecords"))
            .resources(
                Collections.singletonList(props.getRhythmCloudAnalysisOutputStream().getAttrArn()))
            .build();

    PolicyStatement kinesisReaderPolicyStatement =
        PolicyStatement.Builder.create()
            .sid("KinesisReader")
            .effect(Effect.ALLOW)
            .actions(
                Arrays.asList(
                    "kinesis:DescribeStream", "kinesis:GetShardIterator", "kinesis:GetRecords"))
            .resources(
                Arrays.asList(
                    props.getRhythmCloudSystemHitStream().getAttrArn(),
                    props.getRhythmCloudUserHitStream().getAttrArn()))
            .build();

    PolicyStatement cloudWatchAnalyzerPolicyStatement =
        PolicyStatement.Builder.create()
            .sid("CloudWatchAnalyzer")
            .effect(Effect.ALLOW)
            .actions(
                Arrays.asList(
                    "logs:DescribeLogGroups", "logs:DescribeLogStreams", "logs:PutLogEvents"))
            .resources(
                Collections.singletonList(
                    String.format("arn:aws:logs:%s:%s:log-group:*", Aws.REGION, Aws.ACCOUNT_ID)))
            .build();

    // CDK does not support timestream db yet
    // TODO: Once you add the right props for TimeStream DB,
    // please change the ARN to the ARN of the timestream table
    PolicyStatement timeStreamDBPolicyStatement =
        PolicyStatement.Builder.create()
            .sid("TimeStreamDBAll")
            .effect(Effect.ALLOW)
            .actions(
                Arrays.asList(
                    "timestream:WriteRecords", "timestream:CancelQuery", "timestream:UpdateTable"))
            .resources(Collections.singletonList("*"))
            .build();

    rhythmAnalyzerRole =
        Role.Builder.create(this, "rhythm-cloud-analyzer-role")
            .roleName("rhythm-cloud-analyzer-role")
            .assumedBy(new ServicePrincipal("kinesisanalytics.amazonaws.com"))
            .build();

    rhythmAnalyzerPolicy =
        ManagedPolicy.Builder.create(this, "rhythm-cloud-analyzer-policy")
            .managedPolicyName("rhythm-cloud-analyzer-policy")
            .description("Managed policy for rhythym analyzer")
            .statements(
                Arrays.asList(
                    s3ReadArtifactPolicy,
                    kinesisWriterPolicyStatement,
                    kinesisReaderPolicyStatement,
                    kinesisMetadataReaderPolicyStatement,
                    cloudWatchAnalyzerPolicyStatement,
                    timeStreamDBPolicyStatement))
            .build();

    rhythmAnalyzerRole.addManagedPolicy(rhythmAnalyzerPolicy);

    rhythmAnalyzerLogGroup =
        LogGroup.Builder.create(this, "rhythm-analyzer-log-group")
            .logGroupName("/aws/kinesis-analytics/rhythm-analyzer")
            .retention(RetentionDays.ONE_DAY)
            .build();

    rhythmAnalyzerLogStream =
        rhythmAnalyzerLogGroup.addStream(
            "kinesis-analytics-log-stream",
            StreamOptions.builder().logStreamName("kinesis-analytics-log-stream").build());

    CfnOutput.Builder.create(this, "rhythm-analyzer-log-group-output")
        .exportName("rhythm-analyzer-log-group-output")
        .description("Rhythm Analyzer Log Group")
        .value(rhythmAnalyzerLogGroup.getLogGroupArn())
        .build();

    props.getRhythmCloudArtifactsBucket().grantRead(rhythmAnalyzerRole);
    rhythmAnalyzerLogGroup.grantWrite(rhythmAnalyzerRole);

    Map<String, String> systemHitPropertyMap = new HashMap<>();
    systemHitPropertyMap.put("aws.region", "us-east-1");
    systemHitPropertyMap.put("flink.stream.initpos", "LATEST");
    systemHitPropertyMap.put("flink.shard.getrecords.intervalmillis", "1000");
    systemHitPropertyMap.put("input.stream.name", props.getRhythmCloudSystemHitStream().getName());
    systemHitPropertyMap.put("AggregationEnabled", "false");
    CfnApplicationV2.PropertyGroupProperty systemHitPropertyGroup =
        CfnApplicationV2.PropertyGroupProperty.builder()
            .propertyGroupId("SYSTEMHIT")
            .propertyMap(systemHitPropertyMap)
            .build();

    Map<String, String> userHitPropertyMap = new HashMap<>();
    userHitPropertyMap.put("aws.region", "us-east-1");
    userHitPropertyMap.put("flink.stream.initpos", "LATEST");
    userHitPropertyMap.put("flink.shard.getrecords.intervalmillis", "1000");
    userHitPropertyMap.put("input.stream.name", props.getRhythmCloudUserHitStream().getName());
    userHitPropertyMap.put("AggregationEnabled", "false");
    CfnApplicationV2.PropertyGroupProperty userHitPropertyGroup =
        CfnApplicationV2.PropertyGroupProperty.builder()
            .propertyGroupId("USERHIT")
            .propertyMap(userHitPropertyMap)
            .build();

    Map<String, String> temporalAnalyzerPropertyMap = new HashMap<>();
    temporalAnalyzerPropertyMap.put("aws.region", "us-east-1");
    temporalAnalyzerPropertyMap.put(
        "output.stream.name", props.getRhythmCloudAnalysisOutputStream().getName());
    temporalAnalyzerPropertyMap.put("AggregationEnabled", "true");
    CfnApplicationV2.PropertyGroupProperty temporalAnalyzerPropertyGroup =
        CfnApplicationV2.PropertyGroupProperty.builder()
            .propertyGroupId("TEMPORALANALYSIS")
            .propertyMap(temporalAnalyzerPropertyMap)
            .build();

    // CDK for timestream is not available yet
    // Manually create the resources and hard code the values here
    // TODO: Replace when CDK is available for timestream
    Map<String, String> timeStreamSinkPropertyMap = new HashMap<>();
    timeStreamSinkPropertyMap.put("aws.region", "us-east-1");
    timeStreamSinkPropertyMap.put("timestream.db.name", "rhythm_cloud");
    timeStreamSinkPropertyMap.put("timestream.db.table.name", "rhythm");
    timeStreamSinkPropertyMap.put("timestream.db.batch_size", "10");
    CfnApplicationV2.PropertyGroupProperty timeStreamSinkPropertyGroup =
        CfnApplicationV2.PropertyGroupProperty.builder()
            .propertyGroupId("TIMESTREAM")
            .propertyMap(timeStreamSinkPropertyMap)
            .build();

    CfnApplicationV2.ApplicationConfigurationProperty applicationConfigurationProperty =
        CfnApplicationV2.ApplicationConfigurationProperty.builder()
            .applicationSnapshotConfiguration(
                CfnApplicationV2.ApplicationSnapshotConfigurationProperty.builder()
                    .snapshotsEnabled(true)
                    .build())
            .applicationCodeConfiguration(
                CfnApplicationV2.ApplicationCodeConfigurationProperty.builder()
                    .codeContent(
                        CfnApplicationV2.CodeContentProperty.builder()
                            .s3ContentLocation(
                                CfnApplicationV2.S3ContentLocationProperty.builder()
                                    .bucketArn(props.getRhythmCloudArtifactsBucket().getBucketArn())
                                    .fileKey(props.getContentPath())
                                    .build())
                            .build())
                    .codeContentType("ZIPFILE")
                    .build())
            .flinkApplicationConfiguration(
                CfnApplicationV2.FlinkApplicationConfigurationProperty.builder()
                    .parallelismConfiguration(
                        CfnApplicationV2.ParallelismConfigurationProperty.builder()
                            .autoScalingEnabled(true)
                            .parallelism(2)
                            .parallelismPerKpu(1)
                            .configurationType("CUSTOM")
                            .build())
                    .monitoringConfiguration(
                        CfnApplicationV2.MonitoringConfigurationProperty.builder()
                            .logLevel("INFO")
                            .metricsLevel("TASK")
                            .configurationType("CUSTOM")
                            .build())
                    .build())
            .environmentProperties(
                CfnApplicationV2.EnvironmentPropertiesProperty.builder()
                    .propertyGroups(
                        Arrays.asList(
                            systemHitPropertyGroup,
                            userHitPropertyGroup,
                            timeStreamSinkPropertyGroup))
                    .build())
            .build();

    rhythmAnalyzerApplication =
        CfnApplicationV2.Builder.create(this, "rhythm-analyzer")
            .applicationName("rhythm-analyzer")
            .applicationDescription("Analyzes the rhythm")
            .serviceExecutionRole(rhythmAnalyzerRole.getRoleArn())
            .runtimeEnvironment("FLINK-1_8")
            .applicationConfiguration(applicationConfigurationProperty)
            .build();

    String applicationName = rhythmAnalyzerApplication.getRef();

    CfnApplicationCloudWatchLoggingOptionV2.Builder.create(this, "cloud-watch-logging")
        .applicationName(applicationName)
        .cloudWatchLoggingOption(
            CfnApplicationCloudWatchLoggingOptionV2.CloudWatchLoggingOptionProperty.builder()
                .logStreamArn(
                    String.format(
                        "arn:aws:logs:%s:%s:log-group:%s:log-stream:%s",
                        Aws.REGION,
                        Aws.ACCOUNT_ID,
                        rhythmAnalyzerLogGroup.getLogGroupName(),
                        rhythmAnalyzerLogStream.getLogStreamName()))
                .build())
        .build();

    CfnOutput.Builder.create(this, "rhythm-analyzer-application-output")
        .exportName("rhythm-analyzer-application-output")
        .description("Rhythm Analyzer Application")
        .value(applicationName)
        .build();
  }

  public ManagedPolicy getRhythmAnalyzerPolicy() {
    return rhythmAnalyzerPolicy;
  }

  public Role getRhythmAnalyzerRole() {
    return rhythmAnalyzerRole;
  }

  public CfnApplicationV2 getRhythmAnalyzerApplication() {
    return rhythmAnalyzerApplication;
  }

  public LogGroup getTemporalAnalyzerLogGroup() {
    return rhythmAnalyzerLogGroup;
  }

  public LogStream getTemporalAnalyzerLogStream() {
    return rhythmAnalyzerLogStream;
  }
}
