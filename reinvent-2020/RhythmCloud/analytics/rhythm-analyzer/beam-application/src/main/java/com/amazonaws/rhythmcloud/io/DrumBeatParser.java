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
package com.amazonaws.rhythmcloud.io;

import com.amazonaws.regions.Regions;
import com.amazonaws.rhythmcloud.configuration.AppOptions;
import com.amazonaws.rhythmcloud.domain.DrumBeat;
import com.amazonaws.services.kinesis.clientlibrary.lib.worker.InitialPositionInStream;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.internal.Streams;
import com.google.gson.stream.JsonReader;
import lombok.extern.slf4j.Slf4j;
import org.apache.beam.sdk.io.kinesis.KinesisIO;
import org.apache.beam.sdk.io.kinesis.KinesisRecord;
import org.apache.beam.sdk.transforms.DoFn;
import org.joda.time.Duration;
import org.joda.time.Instant;

import java.io.ByteArrayInputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

@Slf4j
public class DrumBeatParser {
  protected static Gson gson = null;

  static /*package*/ synchronized Gson getGson() {
    if (gson != null) {
      return gson;
    } else {
      GsonBuilder builder = new GsonBuilder();
      builder.registerTypeAdapter(
          Instant.class,
          (JsonDeserializer<Instant>)
              (json, typeOfT, context) -> Instant.parse(json.getAsString()));
      gson = builder.create();
    }
    return gson;
  }

  /**
   * Since KinesisIO is based on UnboundedSource.CheckpointMark, it uses the standard checkpoint
   * mechanism, provided by Beam UnboundedSource.UnboundedReader.
   *
   * <p>Once a KinesisRecord has been read (actually, pulled from a records queue that is feed
   * separately by actually fetching the records from Kinesis shard), then the shard checkpoint will
   * be updated by using the record SequenceNumber and then, depending on runner implementation of
   * UnboundedSource and checkpoints processing, will be saved.
   */
  public static class KinesisDrumBeatParser extends DoFn<KinesisRecord, DrumBeat> {
    private static DrumBeat parseDrumBeatEvent(byte[] event) {
      try (InputStreamReader reader = new InputStreamReader(new ByteArrayInputStream(event))) {
        JsonReader jsonReader = new JsonReader(reader);
        JsonElement jsonElement = Streams.parse(jsonReader);
        return getGson().fromJson(jsonElement, DrumBeat.class);
      } catch (Exception e) {
        log.error("Could not parse event '{}'", new String(event, StandardCharsets.UTF_8), e);
      }

      throw new IllegalArgumentException("Could not parse input event.");
    }

    @ProcessElement
    public void processElement(@Element KinesisRecord record, OutputReceiver<DrumBeat> out) {
      DrumBeat drumBeatEvent = parseDrumBeatEvent(record.getDataAsBytes());
      log.debug("Successfully parsed Drum beat: {}", drumBeatEvent.toString());
      out.output(drumBeatEvent);
    }
  }

  public static KinesisIO.Read readSystemBeats(AppOptions options) {
    return KinesisIO.<DrumBeat>read()
        .withStreamName(options.getSystemBeatInputStreamName())
        .withAWSClientsProvider(
            new KinesisClientProviderWithDefaultCredentials(
                Regions.fromName(Regions.getCurrentRegion().getName())))
        .withMaxReadTime(Duration.standardMinutes(1)) // to prevent endless running in case of error
        .withInitialPositionInStream(
            InitialPositionInStream.valueOf(options.getSystemBeatInitialPosition()))
        .withFixedDelayRateLimitPolicy(
            Duration.millis(options.getSystemBeatGetRecordsIntervalMillis()));
  }

  public static KinesisIO.Read readUserBeats(AppOptions options) {
    return KinesisIO.<DrumBeat>read()
        .withStreamName(options.getUserBeatInputStreamName())
        .withAWSClientsProvider(
            new KinesisClientProviderWithDefaultCredentials(
                Regions.fromName(Regions.getCurrentRegion().getName())))
        .withMaxReadTime(Duration.standardMinutes(1)) // to prevent endless running in case of error
        .withInitialPositionInStream(
            InitialPositionInStream.valueOf(options.getUserBeatInitialPosition()))
        .withFixedDelayRateLimitPolicy(
            Duration.millis(options.getUserBeatGetRecordsIntervalMillis()));
  }
}
