import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Ranking } from '../_models/ranking';

@Injectable({
  providedIn: 'root'
})
export class LeaderboardService {
  baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  getRankings(): Observable<Ranking[]> {
    return this.http.get<Ranking[]>(this.baseUrl + 'rankings');
  }

  get(gameId): Observable<number> {
    return this.http.get<number>(this.baseUrl + 'rankings/' + gameId);
  }
}
