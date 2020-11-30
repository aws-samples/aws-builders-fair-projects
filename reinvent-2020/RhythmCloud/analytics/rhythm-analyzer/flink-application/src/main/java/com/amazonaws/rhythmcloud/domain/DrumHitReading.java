package com.amazonaws.rhythmcloud.domain;

import com.google.gson.annotations.JsonAdapter;
import com.google.gson.annotations.SerializedName;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@AllArgsConstructor
@NoArgsConstructor
@ToString
@JsonAdapter(DrumHitReadingDeserializer.class)
public class DrumHitReading {
  @SerializedName("sessionId")
  private Long sessionId;

  @SerializedName("drum")
  private String drum;

  @SerializedName("timestamp")
  private Long timestamp;

  @SerializedName("voltage")
  private Double voltage;
}
