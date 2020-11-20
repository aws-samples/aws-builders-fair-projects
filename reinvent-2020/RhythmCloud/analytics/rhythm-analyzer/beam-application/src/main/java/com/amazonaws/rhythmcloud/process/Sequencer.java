package com.amazonaws.rhythmcloud.process;

import com.amazonaws.rhythmcloud.domain.DrumBeat;
import com.amazonaws.rhythmcloud.domain.SequencedDrumBeat;
import lombok.extern.slf4j.Slf4j;
import org.apache.beam.sdk.coders.ListCoder;
import org.apache.beam.sdk.coders.SerializableCoder;
import org.apache.beam.sdk.coders.VarIntCoder;
import org.apache.beam.sdk.coders.VarLongCoder;
import org.apache.beam.sdk.state.*;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.windowing.BoundedWindow;
import org.apache.beam.sdk.values.KV;

import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;

@Slf4j
public class Sequencer extends DoFn<KV<String, DrumBeat>, KV<String, SequencedDrumBeat>> {
  static final Long ALLOWED_LATENESS = 30000L;

  @StateId("map")
  private final StateSpec<MapState<Long, List<DrumBeat>>> mapSpec =
      StateSpecs.map(VarLongCoder.of(), ListCoder.of(SerializableCoder.of(DrumBeat.class)));

  @StateId("sequence")
  private final StateSpec<ValueState<Integer>> sequeunceSpec = StateSpecs.value(VarIntCoder.of());

  @TimerId("next")
  private final TimerSpec nextTimerSpec = TimerSpecs.timer(TimeDomain.EVENT_TIME);

  Long lastWatermark = Long.MIN_VALUE;

  @ProcessElement
  public void process(
      ProcessContext context,
      BoundedWindow window,
      @StateId("map") MapState<Long, List<DrumBeat>> mapState,
      @TimerId("next") Timer nextTimer) {
    log.debug("Buffering event: {}", context.element().getValue().toString());
    bufferEvent(context.element(), mapState);
    nextTimer.set(window.maxTimestamp());
    log.info("Timer set for {}", window.maxTimestamp());
    //    nextTimer.set(context.element().getValue().toJodaTime().plus(ALLOWED_LATENESS));
  }

  @OnTimer("next")
  public void onNextTimestamp(
      OnTimerContext context,
      @StateId("map") MapState<Long, List<DrumBeat>> mapState,
      @StateId("sequence") ValueState<Integer> sequenceState) {
    log.debug(
        "Timer triggered {} {}",
        context.fireTimestamp().toString(),
        context.timestamp().toString());

    Integer sequenceNumber = 0;
    if (sequenceState != null && sequenceState.read() != null) {
      sequenceNumber = sequenceState.read();
    }

    PriorityQueue<Long> sortedTimestamps = getSortedTimestamps(mapState);
    while (!sortedTimestamps.isEmpty()) {
      long timestamp = sortedTimestamps.poll();
      for (DrumBeat event : mapState.get(timestamp).read()) {
        String key = String.format("%s-%s", event.getStageName(), event.getSessionId());
        KV<String, SequencedDrumBeat> sequencedDrumBeat =
            KV.of(
                key,
                new SequencedDrumBeat(
                    sequenceNumber + 1,
                    event.getSessionId(),
                    event.getDrum(),
                    event.getTimestamp(),
                    event.getVoltage(),
                    event.getStageName()));
        log.debug("Collecting {}", sequencedDrumBeat.getValue().toString());
        context.output(sequencedDrumBeat);
      }
    }
    mapState.clear();
    sequenceState.write(sequenceNumber);
  }

  /**
   * Gets the sorted timestamps of any buffered events.
   *
   * @param mapState Bag of events with timestamps
   * @return a sorted list of timestamps that have at least one buffered event
   */
  private PriorityQueue<Long> getSortedTimestamps(
      @StateId("map") MapState<Long, List<DrumBeat>> mapState) {
    PriorityQueue<Long> sortedTimestamps = new PriorityQueue<>();
    for (Long timestamp : mapState.keys().read()) {
      sortedTimestamps.offer(timestamp);
    }
    return sortedTimestamps;
  }
  /**
   * Buffers an element for future processing
   *
   * @param event DrumBeat event
   */
  private void bufferEvent(
      KV<String, DrumBeat> event, @StateId("map") MapState<Long, List<DrumBeat>> mapState) {
    Long timestamp = event.getValue().toJodaTime().getMillis();
    List<DrumBeat> elements = mapState.get(timestamp).read();
    if (elements == null || elements.size() == 0) {
      elements = new ArrayList<>();
    }

    elements.add(event.getValue());
    mapState.put(timestamp, elements);
  }
}
