import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { TestService } from 'src/app/_services/test.service';
import { AlertifyService } from 'src/app/_services/alertify.service';
import { FormsModule } from '@angular/forms';
import { PollyLanguage } from 'src/app/_models/pollyLanguage';
import { PollyVoice } from 'src/app/_models/pollyVoice';

@Component({
  selector: 'app-test-polly',
  templateUrl: './test-polly.component.html',
  styleUrls: ['./test-polly.component.css']
})

export class TestPollyComponent implements OnInit {
  texttospeech: any;
  audioPolly = new Audio();
  pollyLanguages: PollyLanguage[];
  pollyVoices: PollyVoice[];

  constructor(private http: HttpClient,
              private testService: TestService,
              private alertify: AlertifyService) { }

  ngOnInit() { }

  // tslint:disable-next-line: use-lifecycle-interface
  ngAfterViewInit() {

    setTimeout(() => {
      this.getPollyLanguages();
      this.selectPollyLanguage('en-US');
    });
  }

  getPollyLanguages() {
    this.testService.getPollyLanguageList().subscribe((pollyLanguages: PollyLanguage[]) => {
      this.pollyLanguages = pollyLanguages;
    }, error => {
      console.log(error);
    });
  }

  selectPollyLanguage(languageCode) {
    this.pollyVoices = null;

    this.testService.getPollyVoiceList(languageCode).subscribe((pollyVoices: PollyVoice[]) => {
      this.pollyVoices = pollyVoices;
    }, error => {
      console.log(error);
    });
  }

  public speech() {

    const body = {
      text: 'Learn languages with AWS AI/ML'
    };

    this.alertify.message('Now working on it...');

    this.testService.pollyTest(body).subscribe((result: any) => {

      console.log(result);

      this.alertify.success('Polly call success.');
      this.audioPolly.src = result.mediaUri;
      this.audioPolly.load();
      this.audioPolly.play();

    }, error => {
      this.alertify.error('Something wrong. Try again.');
    });
  }
}
