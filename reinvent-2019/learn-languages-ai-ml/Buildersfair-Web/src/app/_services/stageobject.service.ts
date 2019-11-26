import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { StageObject } from '../_models/stageobject';

@Injectable({
  providedIn: 'root'
})
export class StageObjectService {
  baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  getStageObjects(): Observable<StageObject[]> {
    return this.http.get<StageObject[]>(this.baseUrl + 'stageobjects');
  }
}
