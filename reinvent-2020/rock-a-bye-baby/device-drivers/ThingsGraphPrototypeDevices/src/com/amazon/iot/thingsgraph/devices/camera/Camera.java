package com.amazon.iot.thingsgraph.devices.camera;

import com.amazon.iot.thingsgraph.devices.drivers.CameraDevice;
import com.amazon.iot.thingsgraph.devices.drivers.MacbookCamera;
import com.amazon.iot.thingsgraph.devices.drivers.PiCamera;
import com.amazon.iot.thingsgraph.devices.utils.DeviceUtils;
import com.amazonaws.services.iot.client.AWSIotDevice;
import com.amazonaws.services.iot.client.AWSIotDeviceProperty;
import com.amazonaws.services.iot.client.AWSIotException;
import com.amazonaws.services.iot.client.AWSIotMessage;
import com.amazonaws.services.iot.client.AWSIotMqttClient;
import com.amazonaws.services.iot.client.AWSIotQos;
import com.amazonaws.services.iot.client.AWSIotTimeoutException;
import com.amazonaws.services.iot.client.AWSIotTopic;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.model.GeneratePresignedUrlRequest;
import com.amazonaws.services.s3.model.PutObjectRequest;
import org.apache.commons.cli.CommandLine;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.locks.ReentrantLock;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.document.DynamoDB;
import com.amazonaws.services.dynamodbv2.document.Item;
import com.amazonaws.services.dynamodbv2.document.Table;
import java.util.UUID;


public class Camera extends AWSIotDevice {

    private static final String DEFAULT_BUCKET_NAME = "gg-r-pi";

    public static void main(String args[]) throws IOException, AWSIotException {

        CommandLine cmd = DeviceUtils.parseAndVerifyArguments(args);
        
        System.out.println(DeviceUtils.getOptions());
        
        if(cmd.hasOption("h")) {
            System.out.println(DeviceUtils.getOptions());
            System.exit(0);
        }

        String thingName = DeviceUtils.getThingName(cmd);

        AWSIotMqttClient client = DeviceUtils.getClient(cmd);
        client.connect();

        CameraDevice cameraDevice = cmd.hasOption("m") ? MacbookCamera.getInstance() : PiCamera.getInstance();

        String bucketName = cmd.hasOption("b") ? cmd.getOptionValue("b") : DEFAULT_BUCKET_NAME;

        Camera device = new Camera(thingName, client, DeviceUtils.getS3Client(cmd), DeviceUtils.getDDBClient(cmd), cameraDevice, bucketName);

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

    private final CameraDevice mCamera;
    private final AWSIotMqttClient mIotClient;
    private final AmazonS3 mS3;
    private final ReentrantLock mLock;
    private final String bucketName;
    private final String thingName;
    private final AmazonDynamoDB ddb;

    @AWSIotDeviceProperty(allowUpdate=false)
    private volatile String lastImage;

    ExecutorService threadPool = Executors.newCachedThreadPool();

    public Camera(String thingName, AWSIotMqttClient client, AmazonS3 s3, AmazonDynamoDB ddbclient, CameraDevice cameraDevice, String bucketName) throws AWSIotException, IOException {
        super(thingName);
        this.thingName = thingName;
        mLock = new ReentrantLock();
        mCamera = cameraDevice;
        mIotClient = client;
        mS3 = s3;
        ddb = ddbclient;
        this.bucketName = bucketName;
        mIotClient.attach(this);
        try {
            this.delete(1000);
        } catch(AWSIotTimeoutException e) {
            // Timed out to delete shadow. Continue with previous state.
        }

        try {
            mIotClient.subscribe(getTopic(thingName + "/capture", t -> capture()), 1000, true);
        } catch (AWSIotTimeoutException e) {
            throw new RuntimeException("Failed to subscribe to topic");
        }
    }

    public String getLastImage() {
        return lastImage;
    }


    private void capture() throws IOException {
        mLock.lock();
        try {
            long key = System.currentTimeMillis();
//            String imgFileName = "/tmp/" + key + ".jpg";
//            mCamera.takeStill(imgFileName);
            String imgFileName = "/tmp/" + key + ".mp4";
            mCamera.takeVideo(imgFileName);

            File img = new File(imgFileName);
//            String s3ItemName = key + ".jpg";
            String s3ItemName = key + ".mp4";
            mS3.putObject(new PutObjectRequest(bucketName, s3ItemName, img)); // TODO non-public read
            img.delete();
            URL preSignedURL = mS3.generatePresignedUrl(new GeneratePresignedUrlRequest(bucketName,
                                                                                        s3ItemName).withExpiration(new Date(key + (1000 * 60 * 60 * 24 * 7)-60)));
            lastImage = preSignedURL.toString();

            addEventToHistory(lastImage);
            threadPool.execute(() -> {
                try {
                    String message = "{\"lastClickedImage\" : \"" + lastImage + "\", \"s3BucketName\" : \"" + bucketName
                                     + "\", \"s3ItemName\" : \"" + s3ItemName + "\"}";
                    System.out.println("publish : " + message);
                    mIotClient.publish(thingName + "/capture/finished", message, 1000);
                } catch (AWSIotException | AWSIotTimeoutException e) {
                    System.out.println(e);
                    e.printStackTrace();
                }
            });
        } finally {
            mLock.unlock();
        }
    }

    private void addEventToHistory(String s3url) {
        final DynamoDB dynamoDB = new DynamoDB(ddb);
        String tableName = "Eventhistory-3igowz2cfvdljkpzki3qo4x63a-dev";
        String id = UUID.randomUUID().toString();
        Date date = new Date();
        SimpleDateFormat formatter = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");
        String creationTime= formatter.format(date);

        Table table = dynamoDB.getTable(tableName);
        
        try {

            Item item = new Item().withPrimaryKey("id", id).withString("CreationTime", creationTime)
                .withString("VideoLink", s3url);
            table.putItem(item);

        }
        catch (Exception e) {
            System.err.println("Create items failed.");
            System.err.println(e.getMessage());

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
        void run(T input) throws Exception;
    }
}
