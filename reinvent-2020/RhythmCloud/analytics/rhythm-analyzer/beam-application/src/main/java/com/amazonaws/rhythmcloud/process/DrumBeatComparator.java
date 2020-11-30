package com.amazonaws.rhythmcloud.process;

import com.amazonaws.rhythmcloud.domain.DrumBeat;
import org.apache.beam.sdk.values.KV;

import java.util.Comparator;

public class DrumBeatComparator implements Comparator<KV<String, DrumBeat>> {
  @Override
  public int compare(KV<String, DrumBeat> o1, KV<String, DrumBeat> o2) {
    return o1.getValue().getTimestamp().compareTo(o2.getValue().getTimestamp());
  }
}
