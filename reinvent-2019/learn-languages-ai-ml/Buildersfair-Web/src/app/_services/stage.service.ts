import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { StageInfo } from '../_models/stageinfo';
import { StageScore } from '../_models/stagescore';

@Injectable({
  providedIn: 'root'
})
export class StageService {
  baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  getStage(gameId, stageId): Observable<StageInfo> {
    return this.http.get<StageInfo>(this.baseUrl + 'stages?game_id=' + gameId + '&stage_id=' + stageId);
  }

  startStage(stageInfo): Observable<number> {
    return this.http.post<number>(this.baseUrl + 'stageslogs', stageInfo);
  }

  endStage(stageInfo): Observable<number> {
    return this.http.put<number>(this.baseUrl + 'stageslogs', stageInfo);
  }

  uploadPicture(stageObject): Observable<StageScore> {
    return this.http.post<StageScore>(this.baseUrl + 'stages', stageObject);
  }

  uploadTest(body): Observable<any> {
    return this.http.post(this.baseUrl + 'testpictures', body);
  }
}
