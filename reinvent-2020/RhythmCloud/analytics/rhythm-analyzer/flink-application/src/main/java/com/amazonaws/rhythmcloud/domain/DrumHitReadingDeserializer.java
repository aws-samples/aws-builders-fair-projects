package com.amazonaws.rhythmcloud.domain;

import com.google.gson.*;

import java.lang.reflect.Type;

public class DrumHitReadingDeserializer implements JsonDeserializer<DrumHitReading> {
  @Override
  public DrumHitReading deserialize(
      JsonElement json, Type typeOfT, JsonDeserializationContext context)
      throws JsonParseException {
    JsonObject jsonObject = json.getAsJsonObject();

    return new DrumHitReading(
        jsonObject.get("sessionId").getAsLong(),
        jsonObject.get("drum").getAsString(),
        jsonObject.get("timestamp").getAsLong(),
        jsonObject.get("voltage").getAsDouble());
  }
}
