/*
 * Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
package com.amazonaws.rhythmcloud.configuration;

import com.amazonaws.services.kinesisanalytics.runtime.KinesisAnalyticsRuntime;
import org.apache.beam.runners.flink.FlinkPipelineOptions;
import org.apache.beam.sdk.io.aws2.options.AwsOptions;
import org.apache.beam.sdk.options.Description;
import org.apache.beam.sdk.options.StreamingOptions;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.Map;
import java.util.Properties;

public interface AppOptions extends FlinkPipelineOptions, StreamingOptions, AwsOptions {
  Logger LOGGER = LoggerFactory.getLogger(AppOptions.class);
  /* Property Bag */

  @Description("Initial position of the system beat kinesis stream")
  public String getSystemBeatInitialPosition();

  public void setSystemBeatInitialPosition(String value);

  @Description("System beat kinesis stream poll interval")
  public Long getSystemBeatGetRecordsIntervalMillis();

  public void setSystemBeatGetRecordsIntervalMillis(Long value);

  @Description("Name of the system beat kinesis input stream")
  public String getSystemBeatInputStreamName();

  public void setSystemBeatInputStreamName(String value);

  @Description("Initial position of the user beat kinesis stream")
  public String getUserBeatInitialPosition();

  public void setUserBeatInitialPosition(String value);

  @Description("User beat kinesis stream poll interval")
  public Long getUserBeatGetRecordsIntervalMillis();

  public void setUserBeatGetRecordsIntervalMillis(Long value);

  @Description("Name of the user beat kinesis input stream")
  public String getUserBeatInputStreamName();

  public void setUserBeatInputStreamName(String value);

  @Description("Name of the temporal analysis kinesis output stream")
  public String getOutputStreamName();

  public void setOutputStreamName(String value);
  /* Property Bag */

  /**
   * Reads KDA application properties
   *
   * @param args
   * @param applicationPropertyGroupName Name of the group property to read
   * @return Application properties formatted as command line arguments
   */
  static String[] argsFromKinesisApplicationProperties(
      String[] args, String applicationPropertyGroupName) {
    Properties properties = null;

    try {
      Map<String, Properties> kdaProperties = KinesisAnalyticsRuntime.getApplicationProperties();

      if (kdaProperties == null) {
        LOGGER.warn("Kinesis Analytics Runtime returned no properties");
      }

      LOGGER.info(
          "Reading {} from properties returned by Kinesis Analytics Runtime",
          applicationPropertyGroupName);
      assert kdaProperties != null;
      properties = kdaProperties.get(applicationPropertyGroupName);

      if (properties == null) {
        LOGGER.warn("Unable to load application properties from kinesis analytics runtime");
        return new String[0];
      }
    } catch (IOException e) {
      LOGGER.warn("Unable to load application properties from kinesis analytics runtime");
    }

    LOGGER.info("Successfully read properties for : {}", applicationPropertyGroupName);

    // Format the property bag to argument format required by beam
    assert properties != null;
    String[] argsFromKinesisApplicationProperties =
        properties.entrySet().stream()
            .map(
                property ->
                    String.format(
                        "--%s%s=%s",
                        Character.toLowerCase(((String) property.getKey()).charAt(0)),
                        ((String) property.getKey()).substring(1),
                        property.getValue()))
            .toArray(String[]::new);

    return argsFromKinesisApplicationProperties;
  }
}
