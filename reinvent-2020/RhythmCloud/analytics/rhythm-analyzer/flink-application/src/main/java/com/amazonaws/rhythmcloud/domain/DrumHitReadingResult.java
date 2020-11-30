package com.amazonaws.rhythmcloud.domain;

import com.google.gson.annotations.SerializedName;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.io.Serializable;

@Data
@AllArgsConstructor
@NoArgsConstructor
@ToString
public class DrumHitReadingResult implements Serializable {
  @SerializedName("sessionId")
  private Long sessionId;

  @SerializedName("sequenceId")
  private Long sequenceId;

  @SerializedName("systemDrum")
  private String systemDrum;

  @SerializedName("userDrum")
  private String userDrum;

  @SerializedName("systemTimestamp")
  private Long systemTimestamp;

  @SerializedName("userTimestamp")
  private Long userTimestamp;

  @SerializedName("userVoltage")
  private Double userVoltage;

  @SerializedName("score")
  private Long score;
}
