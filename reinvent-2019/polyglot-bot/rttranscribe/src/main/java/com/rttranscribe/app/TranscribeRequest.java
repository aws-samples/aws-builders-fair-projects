
package com.rttranscribe.app;

public class TranscribeRequest {
    String s3Path;
    String languageCode;

    public String getS3Path() {
        return s3Path;
    }

    public void setS3Path(String s3Path) {
        this.s3Path = s3Path;
    }

    public String getLanguageCode() {
        return languageCode;
    }

    public void setLanguageCode(String languageCode) {
        this.languageCode = languageCode;
    }

    public TranscribeRequest(String s3Path, String languageCode) {
        this.s3Path = s3Path;
        this.languageCode = languageCode;
    }

    public TranscribeRequest() {
    }
}