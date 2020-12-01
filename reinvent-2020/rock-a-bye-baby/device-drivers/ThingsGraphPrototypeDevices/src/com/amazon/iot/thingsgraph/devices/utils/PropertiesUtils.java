package com.amazon.iot.thingsgraph.devices.utils;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class PropertiesUtils {

    private final String mPropertiesFileName;
    private final Properties mProperties;

    public PropertiesUtils(String fileName) throws IOException {
        mPropertiesFileName = fileName;
        mProperties = new Properties();
        try(InputStream stream = new FileInputStream(new File(mPropertiesFileName))) {
            mProperties.load(stream);
        } finally {
            //
        }
    }

    public String getConfig(String propertyName) {
        return mProperties.getProperty(propertyName);
    }
}
