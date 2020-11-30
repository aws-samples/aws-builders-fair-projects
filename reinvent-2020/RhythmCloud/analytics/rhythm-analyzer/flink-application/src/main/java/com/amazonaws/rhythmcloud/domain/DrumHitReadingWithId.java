package com.amazonaws.rhythmcloud.domain;

import com.amazonaws.rhythmcloud.Constants;
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
public class DrumHitReadingWithId implements Serializable {
  @SerializedName("sessionId")
  private Long sessionId;

  @SerializedName("drum")
  private String drum;

  @SerializedName("timestamp")
  private Long timestamp;

  @SerializedName("voltage")
  private Double voltage;

  @SerializedName("id")
  private Long id;

  @SerializedName("type")
  private Constants.Stream type;
}
