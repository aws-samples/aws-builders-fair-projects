package com.amazon.iot.thingsgraph.devices.utils;

import com.amazonaws.services.iot.client.AWSIotQos;

import java.util.List;

public class DeviceConfig {
    private String thingName;
    private String deviceType;
    private String standardDeviceType;
    private List<String> subscriptionTopics;
    private AWSIotQos awsIotQos;
    private String returnValue;

    public String getThingName() {
        return thingName;
    }

    public void setThingName(String thingName) {
        this.thingName = thingName;
    }

    public String getDeviceType() {
        return deviceType;
    }

    public void setDeviceType(String deviceType) {
        this.deviceType = deviceType;
    }

    public String getStandardDeviceType() {
        return standardDeviceType;
    }

    public void setStandardDeviceType(String standardDeviceType) {
        this.standardDeviceType = standardDeviceType;
    }

    public List<String> getSubscriptionTopics() {
        return subscriptionTopics;
    }

    public void setSubscriptionTopics(List<String> subscriptionTopics) {
        this.subscriptionTopics = subscriptionTopics;
    }

    public AWSIotQos getAwsIotQos() {
        return awsIotQos;
    }

    public void setAwsIotQos(AWSIotQos awsIotQos) {
        this.awsIotQos = awsIotQos;
    }

    public String getReturnValue() {
        return returnValue;
    }

    public void setReturnValue(String returnValue) {
        this.returnValue = returnValue;
    }
}
