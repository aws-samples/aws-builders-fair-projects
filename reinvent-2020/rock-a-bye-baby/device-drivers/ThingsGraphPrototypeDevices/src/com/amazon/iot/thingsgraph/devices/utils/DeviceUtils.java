package com.amazon.iot.thingsgraph.devices.utils;

import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.AWSCredentialsProvider;
import com.amazonaws.auth.DefaultAWSCredentialsProviderChain;
import com.amazonaws.internal.StaticCredentialsProvider;
import com.amazonaws.regions.DefaultAwsRegionProviderChain;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder;
import com.amazonaws.services.iot.client.AWSIotMqttClient;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.Options;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder;

public class DeviceUtils {

    public static Options getOptions() {
        Options options = new Options();
        options.addOption("f", "propertiesFile", true, "File containing device properties");
        options.addOption("p", "port", true, "Port for embedded webservice");
        options.addOption("n", "thingName", true, "Thing name. Override the default value in properties file");
        options.addOption("i", "clientId", true, "Client Id. Override the default value in properties file");
        options.addOption("a", "additionalOptions", true, "Additional options for device");
        options.addOption("g", "gpioPorts", true, "Gpio port numbers");
        options.addOption("h", "help", false, "");
        options.addOption("b", "bucket", true, "Bucket to save images to");
        options.addOption("m", "osx", false, "running on Mac OSX"); // e.g. for camera
        return options;
    }

    public static CommandLine parseAndVerifyArguments(String[] args) {
        CommandLineParser paser = new DefaultParser();
        CommandLine cmd = null;
        Options options = getOptions();

        try {
            cmd = paser.parse(options, args);
        } catch (Exception e) {
            throw new IllegalArgumentException(options.toString(), e);
        }

        //if(StringUtils.isEmpty(cmd.getOptionValue("f"))) {throw new IllegalArgumentException("Properties file path is not present in the command line. Usage " + options);}
        //if(StringUtils.isEmpty(cmd.getOptionValue("e"))) {throw new IllegalArgumentException("Endpoint is not present in the command line. Usage " + options);}
        return cmd;
    }

    public static String getFileContentsAsString(File file) throws IOException {
        try(FileReader fr = new FileReader(file); BufferedReader br = new BufferedReader(fr)) {
            StringBuilder builder = new StringBuilder();
            String line;
            while((line = br.readLine()) != null) {
                builder.append(line);
                builder.append("\n");
            }
            return builder.toString();
        }
    }

    public static AWSIotMqttClient getClient(CommandLine cmd) throws IOException {
        String propertiesFile = cmd.getOptionValue("f");
        PropertiesUtils propertiesUtil = new PropertiesUtils(propertiesFile);
        CertificateUtils.KeyStorePasswordPair pair = CertificateUtils.getKeyStorePasswordPair(propertiesUtil.getConfig("certificateFile"),
                propertiesUtil.getConfig("privateKeyFile"), null);

        String clientEndpoint = propertiesUtil.getConfig("clientEndpoint");
        String clientId = propertiesUtil.getConfig("clientId");
        if(cmd.hasOption("i")) {
            clientId = cmd.getOptionValue("i");
        }

        System.out.println("clientEndpoint : " + clientEndpoint);
        System.out.println("clientId : " + clientId);
        System.out.println("Key password : " + pair.keyPassword);



        return new AWSIotMqttClient(clientEndpoint, clientId, pair.keyStore, pair.keyPassword);
    }

    public static AmazonS3 getS3Client(CommandLine cmd) throws IOException {
        String propertiesFile = cmd.getOptionValue("f");
        PropertiesUtils propertiesUtil = new PropertiesUtils(propertiesFile);

        String accessKey = propertiesUtil.getConfig("accessKeyId");
        String secretKey = propertiesUtil.getConfig("secretKey");
        if(accessKey != null && secretKey != null) {
            AWSCredentialsProvider credentialsProvider = new StaticCredentialsProvider(new AWSCredentials() {

                @Override
                public String getAWSSecretKey() {
                    return secretKey;
                }

                @Override
                public String getAWSAccessKeyId() {
                    return accessKey;
                }
            });

            String region = propertiesUtil.getConfig("region");
            if(region == null || region.length() == 0) {
                region = new DefaultAwsRegionProviderChain().getRegion();
            }
            return AmazonS3ClientBuilder.standard().withCredentials(credentialsProvider).withRegion(region).build();
        } else {
            return AmazonS3ClientBuilder.defaultClient();
        }
    }

    public static AmazonDynamoDB getDDBClient(CommandLine cmd) throws IOException {
        String propertiesFile = cmd.getOptionValue("f");
        PropertiesUtils propertiesUtil = new PropertiesUtils(propertiesFile);

        String accessKey = propertiesUtil.getConfig("accessKeyId");
        String secretKey = propertiesUtil.getConfig("secretKey");
        if(accessKey != null && secretKey != null) {
            AWSCredentialsProvider credentialsProvider = new StaticCredentialsProvider(new AWSCredentials() {

                @Override
                public String getAWSSecretKey() {
                    return secretKey;
                }

                @Override
                public String getAWSAccessKeyId() {
                    return accessKey;
                }
            });

            String region = propertiesUtil.getConfig("region");
            if(region == null || region.length() == 0) {
                region = new DefaultAwsRegionProviderChain().getRegion();
            }
            return AmazonDynamoDBClientBuilder.standard().withCredentials(credentialsProvider).withRegion(region).build();
        } else {
            return AmazonDynamoDBClientBuilder.defaultClient();
        }
    }

    public static String getThingName(CommandLine cmd) throws IOException {
        String thingName = cmd.getOptionValue("n");
        if(thingName != null) return thingName;

        String propertiesFile = cmd.getOptionValue("f");
        PropertiesUtils propertiesUtil = new PropertiesUtils(propertiesFile);
        return propertiesUtil.getConfig("thingName");
    }
}
