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

    const sel = document.getElementById('selectLanguages') as HTMLSelectElement;
    const language = sel.options[sel.selectedIndex].value;

    let voice = '';
    const radios = document.getElementsByName('radioVoices');
    // tslint:disable-next-line: prefer-for-of
    for (let i = 0; i < radios.length; i++) {
      const item = radios[i];
      if ((item as HTMLInputElement).checked === true) {
        voice = (item as HTMLInputElement).value;
      }
    }

    console.log(language + ',' + voice);

    const texttospeech = document.getElementById('texttospeech') as HTMLInputElement;
    console.log(texttospeech.value);

    const body = {
      language_code: language,
      text: texttospeech.value,
      voice_name: voice
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
