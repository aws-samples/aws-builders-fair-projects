package com.amazon.iot.thingsgraph.devices.drivers;

import java.io.IOException;
import java.io.InterruptedIOException;
import java.util.concurrent.TimeUnit;

/*
Uses imagesnap to take picture with Macbook camera

Note: 0.2.6 not working, but 0.2.5 does
  https://github.com/rharder/imagesnap/issues/16
  https://netix.dl.sourceforge.net/project/iharder/imagesnap/ImageSnap-v0.2.5.tgz
    (extract + copy imagesnap executable to /usr/local/bin/ )
 */
public class MacbookCamera implements CameraDevice {

    private static final MacbookCamera DEVICE = new MacbookCamera();

    public static MacbookCamera getInstance() {
        return DEVICE;
    }

    private MacbookCamera() {
    }

    @Override
    public void takeStill(String saveFile) throws IOException {
        Process process = Runtime.getRuntime().exec("imagesnap -w 1 " + saveFile);
        try {
            if(!process.waitFor(3, TimeUnit.SECONDS)) {
                System.out.println("imagesnap process didn't complete successfully");
                process.destroy();
            }
        } catch (InterruptedException e) {
            throw new InterruptedIOException(e.getMessage());
        }
    }
    
    @Override
    public void takeVideo(String saveFile) throws IOException {
        Process process = Runtime.getRuntime().exec("imagesnap -w 1 " + saveFile);
        try {
            if(!process.waitFor(3, TimeUnit.SECONDS)) {
                System.out.println("imagesnap process didn't complete successfully");
                process.destroy();
            }
        } catch (InterruptedException e) {
            throw new InterruptedIOException(e.getMessage());
        }	
    }

}
