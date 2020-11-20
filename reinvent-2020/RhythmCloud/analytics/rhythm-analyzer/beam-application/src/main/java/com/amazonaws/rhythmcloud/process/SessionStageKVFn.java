package com.amazonaws.rhythmcloud.process;

import com.amazonaws.rhythmcloud.domain.DrumBeat;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.values.KV;

public class SessionStageKVFn extends DoFn<DrumBeat, KV<String, DrumBeat>> {
  @ProcessElement
  public void processElement(ProcessContext context) {
    String key =
        String.format("%s-%s", context.element().getStageName(), context.element().getSessionId());
    context.output(KV.of(key, context.element()));
  }
}
