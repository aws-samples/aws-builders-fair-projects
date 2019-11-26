import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { StageLog } from '../_models/stagelog';

@Injectable({
  providedIn: 'root'
})
export class StageLogService {
  baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  getStageLogs(): Observable<StageLog[]> {
    return this.http.get<StageLog[]>(this.baseUrl + 'stagelogs');
  }

  getStageLog(gameId, actionType): Observable<StageLog> {
    return this.http.get<StageLog>(this.baseUrl + 'stagelogs/' + gameId + '/' + actionType);
  }

  addStageLog(stageLog): Observable<StageLog> {
    return this.http.post<StageLog>(this.baseUrl + 'stagelogs', stageLog);
  }

  updateStageLog(stageLog): Observable<StageLog> {
    return this.http.put<StageLog>(this.baseUrl + 'stagelogs', stageLog);
  }
}
