/*
 * Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
package com.amazonaws.rhythmcloud.domain;

import com.google.gson.annotations.SerializedName;
import lombok.*;
import org.apache.beam.sdk.schemas.JavaFieldSchema;
import org.apache.beam.sdk.schemas.annotations.DefaultSchema;
import org.apache.beam.sdk.schemas.annotations.SchemaCreate;

import java.io.Serializable;

@Builder
@NoArgsConstructor
@Getter
@Setter
@ToString
@DefaultSchema(JavaFieldSchema.class)
public class SequencedDrumBeat implements Serializable {
  @SerializedName("sequenceId")
  private Integer sequenceId;

  @SerializedName("sessionId")
  private String sessionId;

  @SerializedName("drum")
  private String drum;

  @SerializedName("timestamp")
  private Long timestamp;

  @SerializedName("voltage")
  private Double voltage;

  @SerializedName("stageName")
  private String stageName;

  @SchemaCreate
  public SequencedDrumBeat(
      Integer sequenceId,
      String sessionId,
      String drum,
      Long timestamp,
      Double voltage,
      String stageName) {
    this.sequenceId = sequenceId;
    this.sessionId = sessionId;
    this.drum = drum;
    this.timestamp = timestamp;
    this.voltage = voltage;
    this.stageName = stageName;
  }
}
