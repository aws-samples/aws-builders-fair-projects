package com.amazonaws.rhythmcloud.io;

import com.amazonaws.rhythmcloud.domain.SequencedDrumBeat;
import lombok.extern.slf4j.Slf4j;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.values.KV;

@Slf4j
public class LogSink {
  public static class PrintToLogFn extends DoFn<KV<String, SequencedDrumBeat>, Void> {
    @ProcessElement
    public void processElement(ProcessContext c) {
      log.info("KEY: {}, ELEMENT: {}", c.element().getKey(), c.element().getValue().toString());
    }
  }
}
