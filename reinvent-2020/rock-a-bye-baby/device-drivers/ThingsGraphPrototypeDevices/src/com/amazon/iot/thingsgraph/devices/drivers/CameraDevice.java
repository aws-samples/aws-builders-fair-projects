package com.amazon.iot.thingsgraph.devices.drivers;

import java.io.IOException;

/*
Common interface for camera device drivers
 */
public interface CameraDevice {
    void takeStill(String saveFile) throws IOException;
    void takeVideo(String saveFile) throws IOException;
}
