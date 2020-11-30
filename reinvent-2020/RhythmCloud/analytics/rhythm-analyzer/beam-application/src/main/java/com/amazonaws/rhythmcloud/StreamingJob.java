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
package com.amazonaws.rhythmcloud;

import com.amazonaws.regions.Regions;
import com.amazonaws.rhythmcloud.configuration.AppOptions;
import com.amazonaws.rhythmcloud.domain.DrumBeat;
import com.amazonaws.rhythmcloud.domain.SequencedDrumBeat;
import com.amazonaws.rhythmcloud.io.DrumBeatParser;
import com.amazonaws.rhythmcloud.io.LogSink;
import com.amazonaws.rhythmcloud.process.MetronomeFilterFn;
import com.amazonaws.rhythmcloud.process.Sequencer;
import com.amazonaws.rhythmcloud.process.SessionStageKVFn;
import com.amazonaws.rhythmcloud.process.TimestampAssignerFn;
import lombok.extern.slf4j.Slf4j;
import org.apache.beam.runners.flink.FlinkRunner;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.coders.CannotProvideCoderException;
import org.apache.beam.sdk.coders.KvCoder;
import org.apache.beam.sdk.coders.SerializableCoder;
import org.apache.beam.sdk.coders.StringUtf8Coder;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.options.PipelineOptionsValidator;
import org.apache.beam.sdk.transforms.Filter;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.transforms.windowing.AfterProcessingTime;
import org.apache.beam.sdk.transforms.windowing.GlobalWindows;
import org.apache.beam.sdk.transforms.windowing.Repeatedly;
import org.apache.beam.sdk.transforms.windowing.Window;
import org.apache.beam.sdk.values.KV;
import org.apache.commons.lang3.ArrayUtils;
import org.joda.time.Duration;

@Slf4j
public class StreamingJob {
  static final Duration THIRTY_SECONDS = Duration.standardSeconds(30);

  public static void main(String[] args) throws CannotProvideCoderException {
    log.info("Starting the Rhythm Analyzer BEAM application");
    String[] kinesisSystemDrumBeatArgs =
        AppOptions.argsFromKinesisApplicationProperties(args, "SYSTEMHIT");
    String[] kinesisUserDrumBeatArgs =
        AppOptions.argsFromKinesisApplicationProperties(args, "USERHIT");
    String[] kinesisTemporalAnalysisArgs =
        AppOptions.argsFromKinesisApplicationProperties(args, "TEMPORALANALYSIS");

    AppOptions options =
        PipelineOptionsFactory.fromArgs(
                ArrayUtils.addAll(
                    args,
                    ArrayUtils.addAll(
                        kinesisSystemDrumBeatArgs,
                        ArrayUtils.addAll(kinesisUserDrumBeatArgs, kinesisTemporalAnalysisArgs))))
            .as(AppOptions.class);
    options.setRunner(FlinkRunner.class);
    options.setRegion(Regions.getCurrentRegion().getName());
    options.setCheckpointingMode("EXACTLY_ONCE");
    options.setCheckpointingInterval(50000L); // 5 second checkpoints
    options.setStreaming(true);

    PipelineOptionsValidator.validate(AppOptions.class, options);

    log.info("Starting the rhythm analyzer application with {}", options.toString());

    Pipeline pipeline = Pipeline.create(options);
    pipeline.getSchemaRegistry().registerPOJO(DrumBeat.class);
    pipeline.getSchemaRegistry().registerPOJO(SequencedDrumBeat.class);
    pipeline
        .getCoderRegistry()
        .registerCoderForClass(DrumBeat.class, SerializableCoder.of(DrumBeat.class));
    pipeline
        .getCoderRegistry()
        .registerCoderForClass(
            SequencedDrumBeat.class, SerializableCoder.of(SequencedDrumBeat.class));

    pipeline
        .apply("System beat stream", DrumBeatParser.readSystemBeats(options))
        .apply(
            "Parse system drum beat events", ParDo.of(new DrumBeatParser.KinesisDrumBeatParser()))
        .setCoder(pipeline.getCoderRegistry().getCoder(DrumBeat.class))
        .apply("Filter out metronome beat", Filter.by(new MetronomeFilterFn()))
        .apply("Assign Timestamp", ParDo.of(new TimestampAssignerFn()))
        .apply("Create Key Value Pair", ParDo.of(new SessionStageKVFn()))
        .setCoder(
            KvCoder.of(StringUtf8Coder.of(), pipeline.getCoderRegistry().getCoder(DrumBeat.class)))
        .apply(
            "Windowing",
            Window.<KV<String, DrumBeat>>into(new GlobalWindows())
                .triggering(
                    Repeatedly.forever(
                        AfterProcessingTime.pastFirstElementInPane().plusDelayOf(THIRTY_SECONDS)))
                .withAllowedLateness(Duration.ZERO)
                .discardingFiredPanes())
        .apply("Sequence the stream within the pane per key", ParDo.of(new Sequencer()))
        .setCoder(
            KvCoder.of(
                StringUtf8Coder.of(),
                pipeline.getCoderRegistry().getCoder(SequencedDrumBeat.class)))
        .apply("Log", ParDo.of(new LogSink.PrintToLogFn()));

    pipeline.run().waitUntilFinish(Duration.millis(0));
  }
}
