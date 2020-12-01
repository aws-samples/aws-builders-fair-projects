package com.amazon.iot.thingsgraph.devices.screen;

import com.amazon.iot.thingsgraph.devices.utils.DeviceUtils;
import com.amazonaws.services.iot.client.AWSIotDevice;
import com.amazonaws.services.iot.client.AWSIotDeviceProperty;
import com.amazonaws.services.iot.client.AWSIotException;
import com.amazonaws.services.iot.client.AWSIotMessage;
import com.amazonaws.services.iot.client.AWSIotMqttClient;
import com.amazonaws.services.iot.client.AWSIotQos;
import com.amazonaws.services.iot.client.AWSIotTimeoutException;
import com.amazonaws.services.iot.client.AWSIotTopic;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.lang3.StringUtils;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class DisplayDevice extends AWSIotDevice {

    public static void main(String args[]) throws IOException, AWSIotException {

        CommandLine cmd = DeviceUtils.parseAndVerifyArguments(args);

        if(cmd.hasOption("h")) {
            System.out.println(DeviceUtils.getOptions());
            System.exit(0);
        }

        String thingName = DeviceUtils.getThingName(cmd);

        AWSIotMqttClient client = DeviceUtils.getClient(cmd);
        client.connect();

        DisplayDevice device = new DisplayDevice(thingName, client);

        try {
            device.waitForStop();
        } catch (InterruptedException e) {
        }
        System.exit(0);
    }

    private final AWSIotMqttClient mIotClient;
    private final com.amazon.iot.thingsgraph.devices.drivers.DisplayDevice mDisplayDriver;

    private volatile boolean mRunning = true;

    @AWSIotDeviceProperty(name="imageUri", allowUpdate=false)
    private volatile String imageUri;

    ScheduledExecutorService threadPool = Executors.newScheduledThreadPool(Runtime.getRuntime().availableProcessors());

    public DisplayDevice(String thingName, AWSIotMqttClient client) throws AWSIotException, IOException {
        super(thingName);
        mDisplayDriver = com.amazon.iot.thingsgraph.devices.drivers.DisplayDevice.getInstance();
        mIotClient = client;
        mIotClient.attach(this);
        try {
            this.delete(1000);
        } catch(AWSIotTimeoutException e) {
            // Timed out to delete shadow. Continue with previous state.
        }

        try {
            mIotClient.subscribe(getTopic(thingName + "/display", t -> {
                JSONObject shadowState;
                System.out.println("received message " + t.getStringPayload());
                try {
                    shadowState = new JSONObject(t.getStringPayload());
                } catch (JSONException e) {
                    System.out.println(e.getMessage());
                    e.printStackTrace();
                    throw new RuntimeException(e);
                }
                String url = shadowState.optString("imageUri");
                if(StringUtils.isNotBlank(url)) {
                    display(url);
                    threadPool.schedule(() -> {stopDisplay(); return true;}, 10, TimeUnit.SECONDS);
                } else {
                    // TODO invoke against /end instead of closing if url to display is null?
                    System.out.println("stopping display");
                    stopDisplay();
                }
            }), 1000, true);

            mIotClient.subscribe(getTopic(thingName + "/end", t -> {
                stopDisplay();
            }), 1000, true);
        } catch (AWSIotTimeoutException e) {
            throw new RuntimeException("Failed to subscribe to topic");
        }
    }

    public String getImageUri() {
        return imageUri;
    }

    public void setImageUri(String imageUri) {
        this.imageUri = imageUri;
    }

    void display(String url) throws IOException {
        System.out.println("message : display " + url);
        setImageUri(url);
        mDisplayDriver.refreshDisplay(url);
        notifyObservers();
    }

    void stopDisplay() throws IOException {
        System.out.println("message : stop");
        setImageUri(null);
        mDisplayDriver.stopDisplay();
        notifyObservers();
    }

    @Override
    public void onShadowUpdate(String jsonState) {
        super.onShadowUpdate(jsonState);
        notifyObservers();
    }

    private void notifyObservers() {
        String state = onDeviceReport();
        threadPool.execute(() -> {
            try {
                mIotClient.publish("screen/display/response", state, 1000);
                System.out.println("published response : " + state);
            } catch (AWSIotTimeoutException | AWSIotException e) {
                System.out.println(e);
                e.printStackTrace();
            }
        });
    }

    public synchronized void waitForStop() throws InterruptedException {
        while (mRunning) {
            this.wait();
        }
    }

    public synchronized void close() throws IOException {
        try {
            mRunning = false;
            mDisplayDriver.stopDisplay();
        } finally {
            this.notifyAll();
        }
    }

    private AWSIotTopic getTopic(String topicName, Action<AWSIotMessage> onMessageAction) {
        System.out.println("Subscribing to topic : " + topicName);
        return new AWSIotTopic(topicName, AWSIotQos.QOS1) {
            public void onMessage(AWSIotMessage message) {
                try {
                    onMessageAction.run(message);
                } catch(Exception e) {
                    System.out.println(e);
                    e.printStackTrace();
                }
            };
        };
    }

    private static interface Action<T> {
        void run(T msg) throws Exception;
    }
}
