package com.amazon.iot.thingsgraph.devices.motionsensor;

import java.io.IOException;
import java.util.concurrent.locks.ReentrantLock;

import org.apache.commons.cli.CommandLine;
import com.amazon.iot.thingsgraph.devices.drivers.PIRMotionSensorFactory;
import com.amazon.iot.thingsgraph.devices.utils.DeviceUtils;
import com.amazonaws.services.iot.client.AWSIotDevice;
import com.amazonaws.services.iot.client.AWSIotDeviceProperty;
import com.amazonaws.services.iot.client.AWSIotException;
import com.amazonaws.services.iot.client.AWSIotMqttClient;
import com.amazonaws.services.iot.client.AWSIotTimeoutException;
import com.pi4j.component.sensor.MotionSensor;
import com.pi4j.component.sensor.MotionSensorChangeEvent;
import com.pi4j.component.sensor.MotionSensorListener;

public class RaspiMotionSensor extends AWSIotDevice {

    public static void main(String args[]) throws IOException, AWSIotException {

        CommandLine cmd = DeviceUtils.parseAndVerifyArguments(args);

        if(cmd.hasOption("h")) {
            System.out.println(DeviceUtils.getOptions());
            System.exit(0);
        }

        int gpioPort = Integer.parseInt(cmd.getOptionValue("g"));
        String thingName = DeviceUtils.getThingName(cmd);

        AWSIotMqttClient client = DeviceUtils.getClient(cmd);
        client.connect();

        RaspiMotionSensor device = new RaspiMotionSensor(thingName, client, gpioPort);

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

    private final MotionSensor mMotionSensor;
    private final AWSIotMqttClient mIotClient;
    private final ReentrantLock mLock;

    @AWSIotDeviceProperty(allowUpdate=false)
    private volatile boolean isMotionDetected = false;
    @AWSIotDeviceProperty(allowUpdate=false)
    private volatile long lastActivityTime = 0;

    public RaspiMotionSensor(String thingName, AWSIotMqttClient client, int gpioPort) throws AWSIotException, IOException {
        super(thingName);
        mLock = new ReentrantLock();
        mMotionSensor = PIRMotionSensorFactory.getGPIOMotionSensor(gpioPort);

        mIotClient = client;
        mIotClient.attach(this);
        try {
            this.delete(1000);
        } catch(AWSIotTimeoutException e) {
            // Timed out to delete shadow. Continue with previous state.
        }

        mMotionSensor.addListener(new MotionSensorListener() {
            
            @Override
            public void onMotionStateChange(MotionSensorChangeEvent arg0) {
                mLock.lock();
                try {
                    isMotionDetected = arg0.isMotionDetected();
                    if(arg0.isMotionDetected()) {
                        lastActivityTime = arg0.getTimestamp().getTime();
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
            }
        });
    }

    public boolean isIsMotionDetected() {
        return isMotionDetected;
    }

    public long getLastActivityTime() {
        return lastActivityTime;
    }

}
