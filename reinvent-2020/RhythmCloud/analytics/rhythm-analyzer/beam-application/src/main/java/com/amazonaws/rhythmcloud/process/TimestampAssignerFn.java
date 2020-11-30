package com.amazonaws.rhythmcloud.process;

import com.amazonaws.rhythmcloud.domain.DrumBeat;
import org.apache.beam.sdk.transforms.DoFn;

public class TimestampAssignerFn extends DoFn<DrumBeat, DrumBeat> {
  @ProcessElement
  public void processElement(ProcessContext context) {
    context.outputWithTimestamp(context.element(), context.element().toJodaTime());
  }
}
