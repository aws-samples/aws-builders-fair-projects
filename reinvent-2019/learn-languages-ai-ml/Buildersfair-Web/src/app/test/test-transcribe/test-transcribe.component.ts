import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { TestService } from 'src/app/_services/test.service';
import { AlertifyService } from 'src/app/_services/alertify.service';
import { TranscribeLanguage } from 'src/app/_models/transcribeLanguage';
import Recorder from 'js-audio-recorder';
import { AnonymousSubject } from 'rxjs/internal/Subject';

@Component({
  selector: 'app-test-transcribe',
  templateUrl: './test-transcribe.component.html',
  styleUrls: ['./test-transcribe.component.css']
})
export class TestTranscribeComponent implements OnInit {
  transcribeLanguages: TranscribeLanguage[];
  recorder = new Recorder({
    sampleBits: 16,
    sampleRate: 160000,
    numChannels: 1,
    compiling: false
  });
  canvas: HTMLCanvasElement = null;
  ctx: any;
  drawRecordId = null;

  constructor(private http: HttpClient,
              private testService: TestService,
              private alertify: AlertifyService) { }

  ngOnInit() {
    this.getTranscribeLanguages();
  }

  getTranscribeLanguages() {
    this.testService.getTranscribeLanguageList().subscribe((transcribeLanguages: TranscribeLanguage[]) => {
      this.transcribeLanguages = transcribeLanguages;
    }, error => {
      console.log(error);
    });
  }

  async startRecording() {
    // https://www.npmjs.com/package/js-audio-recorder
    this.recorder.start().then(() => {
    }, error => {
      console.log(error);
    });
  }

  stopRecording() {
    this.recorder.stop();
    this.drawRecord();
    this.transcribe();
  }

  play() {
    this.recorder.play();
  }

  drawRecord() {

    if (this.canvas === null ) {
      this.canvas = document.getElementById('canvas') as HTMLCanvasElement;
      this.ctx = this.canvas.getContext('2d');
    }

    this.drawRecordId = requestAnimationFrame(this.drawRecord);

    // Gert audio size data in real time
    const dataArray = this.recorder.getRecordAnalyseData();
    const bufferLength = dataArray.length;

    // Fill background color
    this.ctx.fillStyle = 'rgb(200, 200, 200)';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Set the waveform drawing color
    this.ctx.lineWidth = 2;
    this.ctx.strokeStyle = 'rgb(0, 0, 0)';

    this.ctx.beginPath();

    // How many positions a point occupies, a total of bufferLength points to be drawn
    const sliceWidth = this.canvas.width * 1.0 / bufferLength;
    let x = 0; // X-axis position of the plotted point

    for (let i = 0; i < bufferLength; i++) {
        const v = dataArray[i] / 128.0 ;
        const y = v * this.canvas.height / 2;

        if (i === 0) {
            // first point
            this.ctx.moveTo(x, y);
        } else {
            // remaining points
            this.ctx.lineTo(x, y);
        }
        // Pan in turn to draw all points
        x += sliceWidth;
    }
    this.ctx.lineTo(this.canvas.width, this.canvas.height / 2);
    this.ctx.stroke();
  }

  transcribe() {

    const sel = document.getElementById('optLanguages') as HTMLSelectElement;
    const language = sel.options[sel.selectedIndex].value;

    const WAVblob: Blob = this.recorder.getWAVBlob();

    const fd = new FormData();
    fd.append('WAVblob', WAVblob);
    fd.append('language_code', language);

    // console.log(fd);

    this.alertify.message('Now working on it...');

    this.testService.transcribeTest(fd).subscribe(response => {

      this.alertify.success('Transcribe success.');
      // this.labels = response;

    }, error => {
      this.alertify.error('Something wrong. Try again.');
    });
  }
}
