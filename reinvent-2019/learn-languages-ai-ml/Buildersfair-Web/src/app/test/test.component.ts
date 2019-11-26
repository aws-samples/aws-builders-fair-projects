import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css']
})
export class TestComponent implements OnInit {
  feature: string;

  constructor() { }

  ngOnInit() {
    this.feature = 'rekognition';
    this.goTest(this.feature);
  }

  public goTest(feature: string): void {

    if (feature === 'rekognition') {
      document.getElementById('nav-rekognition-tab').classList.add('active');
      document.getElementById('nav-textract-tab').classList.remove('active');
      document.getElementById('nav-polly-tab').classList.remove('active');
      document.getElementById('nav-transcribe-tab').classList.remove('active');
    } else if (feature === 'textract') {
      document.getElementById('nav-rekognition-tab').classList.remove('active');
      document.getElementById('nav-textract-tab').classList.add('active');
      document.getElementById('nav-polly-tab').classList.remove('active');
      document.getElementById('nav-transcribe-tab').classList.remove('active');
    } else if (feature === 'polly') {
      document.getElementById('nav-rekognition-tab').classList.remove('active');
      document.getElementById('nav-textract-tab').classList.remove('active');
      document.getElementById('nav-polly-tab').classList.add('active');
      document.getElementById('nav-transcribe-tab').classList.remove('active');
    } else if (feature === 'transcribe') {
      document.getElementById('nav-rekognition-tab').classList.remove('active');
      document.getElementById('nav-textract-tab').classList.remove('active');
      document.getElementById('nav-polly-tab').classList.remove('active');
      document.getElementById('nav-transcribe-tab').classList.add('active');
    }

    this.feature = feature;
  }
}
