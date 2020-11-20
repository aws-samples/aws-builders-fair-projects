package com.amazonaws.rhythmcloud.process;

import com.amazonaws.rhythmcloud.domain.DrumBeat;
import lombok.extern.slf4j.Slf4j;
import org.apache.beam.sdk.transforms.SerializableFunction;

@Slf4j
public class MetronomeFilterFn implements SerializableFunction<DrumBeat, Boolean> {
  @Override
  public Boolean apply(DrumBeat input) {
    log.info("Filtering {}", input.toString());
    return !(input.getDrum().equalsIgnoreCase("metronome"));
  }
}
