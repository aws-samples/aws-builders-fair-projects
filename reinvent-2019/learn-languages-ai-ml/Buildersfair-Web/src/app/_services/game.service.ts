import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Game } from '../_models/game';
import { GameResult } from '../_models/gameresult';

@Injectable({
  providedIn: 'root'
})
export class GameService {
  baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  getGames(): Observable<Game[]> {
    return this.http.get<Game[]>(this.baseUrl + 'games');
  }

  getGame(gameId): Observable<Game> {
    return this.http.get<Game>(this.baseUrl + 'games/' + gameId);
  }

  createGame(userName): Observable<number> {
    return this.http.post<number>(this.baseUrl + 'games', userName);
  }

  calcGameResult(gameId): Observable<GameResult> {
    return this.http.get<GameResult>(this.baseUrl + 'gameresults/' + gameId + '/calc');
  }
}
