package com.rttranscribe.app;


import java.io.File;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URI;

import java.net.URISyntaxException;

import com.amazonaws.AmazonServiceException;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3URI;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.S3Object;
import com.amazonaws.services.s3.model.S3ObjectInputStream;

import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.transcribestreaming.TranscribeStreamingAsyncClient;

public class RTTranscribe implements RequestHandler<TranscribeRequest, String> {

private static Region region = Region.US_WEST_2;
    @Override
    public String handleRequest(TranscribeRequest request, Context context) {
        try {
            context.getLogger().log("Input: " + request.getS3Path());
            AmazonS3URI s3URI = new AmazonS3URI(request.getS3Path());
            String bucketName = s3URI.getBucket();
            String key = s3URI.getKey();
            context.getLogger().log("bucketName" + bucketName +"key"+ key);
            File s3FileObj = getFileFromS3(bucketName,key);
            TranscribeStreamingSynchronousClient  synchronousClient = new TranscribeStreamingSynchronousClient(RTTranscribe.getClient());
            String finalTranscript = synchronousClient.transcribeFile(s3FileObj, request.getLanguageCode());
            context.getLogger().log("Output: " + finalTranscript);   
            return finalTranscript;
        }
        catch(Exception ex) {
            return "";
        }
    }
    

    
    public static TranscribeStreamingAsyncClient getClient() {
        String endpoint = "https://transcribestreaming." + RTTranscribe.region.toString().toLowerCase().replace('_','-') + ".amazonaws.com";
        try {
            return TranscribeStreamingAsyncClient.builder()
                    .endpointOverride(new URI(endpoint))
                    .region(RTTranscribe.region)
                    .build();
        } catch (URISyntaxException e) {
            throw new IllegalArgumentException("Invalid URI syntax for endpoint: " + endpoint);
        }

    }

    private File getFileFromS3(String bucket_name, String key_name){
        File localFile = new File("/tmp/tmpraw.raw");
        System.out.format("Downloading %s from S3 bucket %s...\n", key_name, bucket_name);
        AmazonS3 s3 = AmazonS3ClientBuilder.standard().withRegion(Regions.DEFAULT_REGION).build();
        try {
            S3Object o = s3.getObject(bucket_name, key_name);
            S3ObjectInputStream s3is = o.getObjectContent();
            FileOutputStream fos = new FileOutputStream(localFile);
            byte[] read_buf = new byte[1024];
            int read_len = 0;
            while ((read_len = s3is.read(read_buf)) > 0) {
                fos.write(read_buf, 0, read_len);
            }
            s3is.close();
            fos.close();
        } catch (AmazonServiceException e) {
            System.out.println(e);
            System.exit(1);
        } catch (FileNotFoundException e) {
            System.out.println(e);
            System.exit(1);
        } catch (IOException e) {
            System.out.println(e);
            System.exit(1);

        }
            return localFile;
        }



}