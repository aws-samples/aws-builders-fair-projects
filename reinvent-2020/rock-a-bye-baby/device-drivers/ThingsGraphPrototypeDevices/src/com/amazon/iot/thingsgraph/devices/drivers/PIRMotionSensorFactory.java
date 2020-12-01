package com.amazon.iot.thingsgraph.devices.drivers;

import com.pi4j.component.sensor.MotionSensor;
import com.pi4j.component.sensor.MotionSensorChangeEvent;
import com.pi4j.component.sensor.MotionSensorListener;
import com.pi4j.component.sensor.impl.GpioMotionSensorComponent;
import com.pi4j.io.gpio.GpioController;
import com.pi4j.io.gpio.GpioFactory;
import com.pi4j.io.gpio.GpioPinDigitalInput;
import com.pi4j.io.gpio.Pin;
import com.pi4j.io.gpio.RaspiPin;

public class PIRMotionSensorFactory {

    public static MotionSensor getGPIOMotionSensor(int pinNumber) {
        GpioController controller = GpioFactory.getInstance();
        Pin pin = RaspiPin.getPinByAddress(pinNumber);
        GpioPinDigitalInput inputPin = controller.provisionDigitalInputPin(pin);
        return new GpioMotionSensorComponent(inputPin);
    }

    private static void main(String[] args) throws InterruptedException {
        MotionSensor sensor = PIRMotionSensorFactory.getGPIOMotionSensor(0);
        sensor.addListener(new MotionSensorListener() {
            
            @Override
            public void onMotionStateChange(MotionSensorChangeEvent arg0) {
                if(arg0.isMotionDetected()) {
                    System.out.println("Motion detected at " + arg0.getTimestamp());
                } else {
                    System.out.println("It is quite at " + arg0.getTimestamp());
                }
            }
        });
        // Wait indefinitely until interrupted
        Object lock = new Object();
        synchronized (lock) {
            while(true) {
                lock.wait();
            }
        }
    }
}
