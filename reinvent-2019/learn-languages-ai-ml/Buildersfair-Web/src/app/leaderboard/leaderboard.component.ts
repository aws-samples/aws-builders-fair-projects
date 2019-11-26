import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Ranking } from '../_models/ranking';
import { LeaderboardService } from '../_services/leaderboard.service';

@Component({
  selector: 'app-leaderboard',
  templateUrl: './leaderboard.component.html',
  styleUrls: ['./leaderboard.component.css']
})
export class LeaderboardComponent implements OnInit {
  rankingColumns: string[];
  rankings: Ranking[];

  constructor(private http: HttpClient,
              private leaderboardService: LeaderboardService) { }

  ngOnInit() {
    this.rankingColumns = this.getRankingColumns();
    this.getRankings();
  }

  getRankings() {
    this.leaderboardService.getRankings().subscribe((rankings: Ranking[]) => {
      this.rankings = rankings;
    }, error => {
      console.log(error);
    });
  }

  getRankingColumns(): string[] {
    return ['total_rank', 'game_id', 'name', 'total_score', 'total_found_objects', 'total_playtime'];
  }
}
