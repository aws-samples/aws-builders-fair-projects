package com.amazon.iot.thingsgraph.devices.motionsensor;

import com.amazon.iot.thingsgraph.devices.utils.DeviceUtils;
import com.amazonaws.services.iot.client.AWSIotDevice;
import com.amazonaws.services.iot.client.AWSIotDeviceProperty;
import com.amazonaws.services.iot.client.AWSIotException;
import com.amazonaws.services.iot.client.AWSIotMqttClient;
import org.apache.commons.cli.CommandLine;

import java.io.IOException;
import java.time.Instant;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;

/**
 * Convenient virtual implementation of a periodic motion sensor for testing
 * Alternates between motion true/false messages every 10 seconds
 */
public class VirtualMotionSensor extends AWSIotDevice {

    public static void main(String args[]) throws IOException, AWSIotException {

        CommandLine cmd = DeviceUtils.parseAndVerifyArguments(args);

        if(cmd.hasOption("h")) {
            System.out.println(DeviceUtils.getOptions());
            System.exit(0);
        }

        String thingName = DeviceUtils.getThingName(cmd);

        AWSIotMqttClient awsIotMqttClient = DeviceUtils.getClient(cmd);
        awsIotMqttClient.connect();
        VirtualMotionSensor device = new VirtualMotionSensor(thingName, awsIotMqttClient);

        try {
            Object ob = new Object();
            synchronized (ob) {
                while (true) {
                    ob.wait();
                }
            }
        } catch (InterruptedException e) {
        }
        System.exit(0);
    }

    private final AWSIotMqttClient mIotClient;
    private final ReentrantLock mLock;

    @AWSIotDeviceProperty(allowUpdate=false)
    private volatile boolean isMotionDetected = false;
    @AWSIotDeviceProperty(allowUpdate=false)
    private volatile long lastActivityTime = 0;

    public VirtualMotionSensor(String thingName, AWSIotMqttClient awsIotMqttClient) throws AWSIotException, IOException {
        super(thingName);
        mLock = new ReentrantLock();

        mIotClient = awsIotMqttClient;
        mIotClient.attach(this);

        Thread periodicMotion = new Thread(new PeriodicMotion());
        periodicMotion.start(); // TODO handle for graceful shutdown
    }

    private class PeriodicMotion implements Runnable {

        @Override
        public void run() {
            while(true) {
                mLock.lock();
                try {
                    isMotionDetected = !isMotionDetected;
                    if (isMotionDetected) {
                        lastActivityTime = Instant.now().toEpochMilli();
                    }
                } finally {
                    mLock.unlock();
                }
                System.out.println("State change : " + onDeviceReport());
                try {
                    mIotClient.publish(thingName + "/motion", "{\"isMotionDetected\" : " + isMotionDetected + " }", 1000);
                } catch (Exception e) {
                    System.out.println(e.getMessage());
                    e.printStackTrace();
                }
                try {
                    TimeUnit.SECONDS.sleep(60);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                    return;
                }
            }
        }
    }

    public boolean isIsMotionDetected() {
        return isMotionDetected;
    }

    public long getLastActivityTime() {
        return lastActivityTime;
    }
}
