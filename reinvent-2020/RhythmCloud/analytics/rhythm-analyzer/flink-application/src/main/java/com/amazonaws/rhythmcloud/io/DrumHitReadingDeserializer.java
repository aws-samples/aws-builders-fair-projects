package com.amazonaws.rhythmcloud.io;

import com.amazonaws.rhythmcloud.domain.DrumHitReading;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.internal.Streams;
import com.google.gson.stream.JsonReader;
import lombok.extern.slf4j.Slf4j;
import org.apache.flink.api.common.serialization.AbstractDeserializationSchema;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.api.java.typeutils.TypeExtractor;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

@Slf4j
public class DrumHitReadingDeserializer extends AbstractDeserializationSchema<DrumHitReading> {
  private static final Gson gson = new GsonBuilder().create();

  public DrumHitReading deserialize(byte[] bytes) throws IOException {
    try {
      JsonReader jsonReader =
          new JsonReader(new InputStreamReader(new ByteArrayInputStream(bytes)));
      JsonElement jsonElement = Streams.parse(jsonReader);
      DrumHitReading reading = gson.fromJson(jsonElement, DrumHitReading.class);
      log.info("Successfully translated: {}", reading);
      return reading;
    } catch (Exception e) {
      String s = new String(bytes, StandardCharsets.UTF_8);
      log.error("cannot parse event '{}'", s, e);
      throw new IOException(String.format("Cannot de-serialize %s", s), e);
    }
  }

  public boolean isEndOfStream(DrumHitReading event) {
    return false;
  }

  @Override
  public TypeInformation<DrumHitReading> getProducedType() {
    return TypeExtractor.getForClass(DrumHitReading.class);
  }
}
