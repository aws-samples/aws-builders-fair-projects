package com.amazon.iot.thingsgraph.devices.drivers;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InterruptedIOException;
import java.io.OutputStream;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;

public class DisplayDevice {

    private static final DisplayDevice DEVICE = new DisplayDevice();

    public static DisplayDevice getInstance() {
        return DEVICE;
    }

    public static void main(String[] args) throws InterruptedException, IOException {
        if(args == null || args.length != 1) {
            throw new IllegalArgumentException("usage java DisaplyDevice \"<Images directory path>\"");
        }
        DisplayDevice device = getInstance();
        device.startDisplay(new File(args[0]));
        for(int i = 0; i < 20; i++) {
            Thread.sleep(1000);
            if(i < 10) {
                device.showNextImage();
            } else {
                device.showPreviousImage();
            }
        }

        device.stopDisplay();
        System.out.println("Stopped");
        Thread.sleep(10000);
        System.exit(0);
    }

    private final ReentrantLock mStateLock;
    private volatile Process mImageDisaplyProcess;
    private String mXWindowId;

    private DisplayDevice() {
        mStateLock = new ReentrantLock();
    }

    public boolean refreshDisplay(String url) throws IOException {
        stopDisplay();
        return startDisplay(url);
    }

    public boolean startDisplay(File directory) throws IOException {
        return startDisplay(directory.toString());
    }

    public boolean startDisplay(String url) throws IOException {
        if(mImageDisaplyProcess == null) {
            mStateLock.lock();


            try {
                if(mImageDisaplyProcess == null) {
                    // execute feh to view image - https://feh.finalrewind.org/
                    Process process = Runtime.getRuntime().exec("feh -Z -F -Y " + url);
                    StreamGobbler output = new StreamGobbler(process.getInputStream());
                    StreamGobbler error = new StreamGobbler(process.getErrorStream());
                    output.start();
                    error.start();

                    // TODO handling feh errors? e.g. Can't open X display

                    try {
                        Thread.sleep(10000);
                    } catch(InterruptedException e) {
                        throw new InterruptedIOException(e.getMessage());
                    }

                    // use xdotool to basically get a handle on the feh window so it can be closed
                    //   https://www.freebsd.org/cgi/man.cgi?query=xdotool
                    Process xwindowFinder = Runtime.getRuntime().exec("xdotool search --name feh*");
                    ByteArrayOutputStream xwindowIdByteArrayOutputStream = new ByteArrayOutputStream();
                    StreamGobbler xwindowIdOutputStreamGobbler = new StreamGobbler(xwindowFinder.getInputStream(), xwindowIdByteArrayOutputStream);
                    StreamGobbler xwindowIdError = new StreamGobbler(xwindowFinder.getErrorStream());
                    xwindowIdOutputStreamGobbler.start();
                    xwindowIdError.start();
                    try {
                        if(!xwindowFinder.waitFor(1, TimeUnit.SECONDS)) {
                            System.out.println("xwindowId finder proceess didn't complete as expected.");
                            process.destroy();
                            xwindowFinder.destroy();
                            return false;
                        }
                        xwindowIdOutputStreamGobbler.join(1000);
                        if(xwindowIdOutputStreamGobbler.isAlive()) {
                            System.out.println("xwindowId finder response reader didn't exit as expected");
                            process.destroy();
                            return false;
                        }
                    } catch(InterruptedException e) {
                        throw new InterruptedIOException(e.getMessage());
                    }
                    String xwindowId = new String(xwindowIdByteArrayOutputStream.toByteArray());
                    if(xwindowId.length() == 0) {
                        System.out.println("xwindowId is not found.");
                        process.destroy();
                        return false;
                    }
                    System.out.println("XWindow Id : " + xwindowId);
                    mXWindowId = xwindowId;
                    mImageDisaplyProcess = process;
                    return true;
                }
            } finally {
                mStateLock.unlock();
            }
        }
        return false;
    }

    private void simulateButtonPress(String button) throws IOException {
        Process process = Runtime.getRuntime().exec("xdotool key --window " + mXWindowId + " " + button);
        StreamGobbler output = new StreamGobbler(process.getInputStream());
        StreamGobbler error = new StreamGobbler(process.getErrorStream());
        output.start();
        error.start();

        try {
            if(!process.waitFor(1, TimeUnit.SECONDS)) {
            process.destroy();
            throw new IOException("Key press simulator didn't finish normally");
            }
        } catch (InterruptedException e) {
            throw new InterruptedIOException(e.getMessage());
        }
    }

    public void showNextImage() throws IOException {
        Process process = mImageDisaplyProcess;
        if(process == null) {
            throw new IllegalStateException("No image displayer is running");
        }
        simulateButtonPress("n");
    }

    public void showPreviousImage() throws IOException {
        Process process = mImageDisaplyProcess;
        if(process == null) {
            throw new IllegalStateException("No image displayer is running");
        }
        simulateButtonPress("p");
    }

    public void stopDisplay() throws IOException {
        Process imageProcess = mImageDisaplyProcess;
        if(imageProcess != null) {
            mStateLock.lock();
            try {
                // This check is required to avoid a close call stopping unintended display process
                // Assume there is display process A is running currently to display images in directory /tmp/A
                // Client issued 2 close calls to stop process A
                // Suppose that first close got the lock and stopped the process.
                // Assume, immediately after first stop request closing the process another
                // client issued a call to start displaying images in dir /tmp/B.
                // If new start call get state lock before already waiting second stop call, start call will
                // start a new display process B.
                // Now second stop call, which was originally intended to stop process A, will stop process B.
                if(imageProcess == mImageDisaplyProcess) {
                    mImageDisaplyProcess = null;
                    simulateButtonPress("Escape");
                    try {
                        if(!imageProcess.waitFor(1, TimeUnit.SECONDS)) {
                            imageProcess.destroyForcibly();
                        }
                    } catch (InterruptedException e) {
                        throw new InterruptedIOException(e.getMessage());
                    }
                    mXWindowId = null;
                }
            } finally {
                mStateLock.unlock();
            }
        }
    }

    private static class StreamGobbler extends Thread {

        private final InputStream mInputStream;
        private final OutputStream mOutputStream;

        public StreamGobbler(InputStream inputStream) {
            this(inputStream, System.out);
        }

        public StreamGobbler(InputStream inputStream, OutputStream outputStram) {
            mInputStream = inputStream;
            mOutputStream = outputStram;
        }

        @Override
        public void run() {
            byte[] buffer = new byte[1024];
            int numberOfBytesRead = 0;
            try {
                while (!isInterrupted() && ((numberOfBytesRead = mInputStream.read(buffer)) != -1)) {
                    mOutputStream.write(buffer, 0, numberOfBytesRead);
                }
            } catch (IOException e) {
                System.out.println(e.getMessage());
                e.printStackTrace();
            }
        }
    }
}
