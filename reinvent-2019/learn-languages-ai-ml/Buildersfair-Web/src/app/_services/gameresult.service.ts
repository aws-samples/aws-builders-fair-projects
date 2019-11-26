import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { GameResult } from '../_models/gameresult';

@Injectable({
  providedIn: 'root'
})
export class GameResultService {
  baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  getGameResults(): Observable<GameResult[]> {
    return this.http.get<GameResult[]>(this.baseUrl + 'gameresults');
  }

  getGameResult(gameId): Observable<GameResult> {
    return this.http.get<GameResult>(this.baseUrl + 'gameresults/' + gameId);
  }
}
