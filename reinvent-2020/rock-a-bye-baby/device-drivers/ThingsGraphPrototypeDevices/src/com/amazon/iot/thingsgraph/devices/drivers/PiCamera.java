package com.amazon.iot.thingsgraph.devices.drivers;

import java.io.File;
import java.io.IOException;
import java.io.InterruptedIOException;
import java.util.concurrent.TimeUnit;

public class PiCamera implements CameraDevice {

    private static final PiCamera DEVICE = new PiCamera();

    public static PiCamera getInstance() {
        return DEVICE;
    }

    private PiCamera() {
        //try {
            //ProcessBuilder pb = new ProcessBuilder("raspistill");
            //pb.start();
        //} catch(IOException e) {
        //    throw new IllegalStateException("PiCamera failed to run raspistill");
        //}
    }

    @Override
    public void takeStill(String saveFile) throws IOException {
        //Process process = new ProcessBuilder("raspistill -o " 
        //                                        + saveFile
        //                                        + " -n -t 1")
        //                        .start();
        Process process = Runtime.getRuntime().exec("raspistill -o " + saveFile + " -n -t 1 -q 10");
        try {
            if(!process.waitFor(2, TimeUnit.SECONDS)) {
                System.out.println("raspistill process didn't compltete successfully");
                process.destroy();
            }
        } catch (InterruptedException e) {
            throw new InterruptedIOException(e.getMessage());
        }
    }
    
    @Override
    public void takeVideo(String saveFile) throws IOException {
        //Process process = new ProcessBuilder("raspistill -o " 
        //                                        + saveFile
        //                                        + " -n -t 1")
        //                        .start();
        Process process = Runtime.getRuntime().exec("raspivid -o pivideo.h264 -t 60000 -w 640 -h 480 -fps 25 -b 1200000 -p 0,0,640,480");
        try {
            if(!process.waitFor(70, TimeUnit.SECONDS)) {
                System.out.println("raspvid process didn't compltete successfully");
                process.destroy();
            }
        } catch (InterruptedException e) {
            throw new InterruptedIOException(e.getMessage());
        }
        
        process = Runtime.getRuntime().exec("MP4Box -add pivideo.h264 " + saveFile);
        try {
            if(!process.waitFor(20, TimeUnit.SECONDS)) {
                System.out.println("MP4Box process didn't compltete successfully");
                process.destroy();
            }
        } catch (InterruptedException e) {
            throw new InterruptedIOException(e.getMessage());
        }
        
    }
    
}
