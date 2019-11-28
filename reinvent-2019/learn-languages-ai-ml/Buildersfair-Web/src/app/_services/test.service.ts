import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { PollyLanguage } from '../_models/pollyLanguage';
import { PollyVoice } from '../_models/pollyVoice';
import { TranscribeLanguage } from '../_models/transcribeLanguage';

@Injectable({
  providedIn: 'root'
})
export class TestService {
  baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  rekognitionTest(body): Observable<any> {
    return this.http.post(this.baseUrl + 'test/rekognition', body);
  }

  textractTest(body): Observable<any> {
    return this.http.post(this.baseUrl + 'test/textract', body);
  }

  pollyTest(body): Observable<any> {
    return this.http.post<any>(this.baseUrl + 'test/polly', body);
  }

  getPollyLanguageList(): Observable<PollyLanguage[]> {
    return this.http.get<PollyLanguage[]>(this.baseUrl + 'test/polly/languages');
  }

  getPollyVoiceList(languageCode): Observable<PollyVoice[]> {
    return this.http.get<PollyVoice[]>(this.baseUrl + 'test/polly/voices?languageCode=' + languageCode);
  }

  transcribeTest(body): Observable<any> {
    return this.http.post(this.baseUrl + 'test/transcribe', body);
  }

  getTranscribeLanguageList(): Observable<TranscribeLanguage[]> {
    return this.http.get<TranscribeLanguage[]>(this.baseUrl + 'test/transcribe/languages');
  }
}
