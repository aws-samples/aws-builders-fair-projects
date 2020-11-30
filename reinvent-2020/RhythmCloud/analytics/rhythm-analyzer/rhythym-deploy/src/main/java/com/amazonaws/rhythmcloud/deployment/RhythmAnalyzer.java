package com.amazonaws.rhythmcloud.deployment;

import software.amazon.awscdk.core.App;

public class RhythmAnalyzer extends App {
    public RhythmAnalyzer() {
        new RhythmAnalyzerStack(this, "rhythm-analyzer");
    }

    public static void main(final String[] args) {
        new RhythmAnalyzer().synth();
    }
}
