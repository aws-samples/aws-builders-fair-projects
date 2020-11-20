package com.amazonaws.rhythmcloud.io;

import com.amazonaws.rhythmcloud.domain.DrumHitReading;
import org.apache.flink.streaming.api.functions.AssignerWithPeriodicWatermarks;
import org.apache.flink.streaming.api.watermark.Watermark;

public class BoundedOutOfOrdernessGenerator
    implements AssignerWithPeriodicWatermarks<DrumHitReading> {
  private final long maxOutOfOrderness = 30_000; // 30 seconds
  private long currentMaxTimestamp;

  // If you are looking for a time lag, change the current max timestamp to
  // System.currentmillis() which will compare the processing time with
  // the event time.
  @Override
  public Watermark getCurrentWatermark() {
    return new Watermark(currentMaxTimestamp - maxOutOfOrderness - 1);
  }

  /*
  In order to work with event time, Flink needs to know the events timestamps,
  meaning each element in the stream needs to have its event timestamp assigned.
  This is usually done by accessing/extracting the timestamp from some field in
  the element by using a TimestampAssigner.

  Timestamp assignment goes hand-in-hand with generating watermarks,
  which tell the system about progress in event time.
  You can configure this by specifying a WatermarkGenerator.

  The Flink API expects a WatermarkStrategy that contains both a
  TimestampAssigner and WatermarkGenerator.
   */
  @Override
  public long extractTimestamp(DrumHitReading drumHitReading, long previousElementTimestamp) {
    long timestamp = drumHitReading.getTimestamp();
    currentMaxTimestamp = Math.max(timestamp, currentMaxTimestamp);
    return timestamp;
  }
}
