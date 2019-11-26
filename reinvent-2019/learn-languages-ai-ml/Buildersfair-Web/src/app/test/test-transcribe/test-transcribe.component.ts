import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { TestService } from 'src/app/_services/test.service';
import { AlertifyService } from 'src/app/_services/alertify.service';
import { TranscribeLanguage } from 'src/app/_models/transcribeLanguage';

@Component({
  selector: 'app-test-transcribe',
  templateUrl: './test-transcribe.component.html',
  styleUrls: ['./test-transcribe.component.css']
})
export class TestTranscribeComponent implements OnInit {
  transcribeLanguages: TranscribeLanguage[];

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

  startRecording() {

    const body = {
      mediaUri: 'https://reinvent-indiamazones.s3-us-west-2.amazonaws.com/pollytest'
    };

    this.alertify.message('Now working on it...');

    this.testService.transcribeTest(body).subscribe((result: any) => {

      console.log(result);

      this.alertify.success('Transcription success.');

    }, error => {
      this.alertify.error('Something wrong. Try again.');
    });
  }
}
