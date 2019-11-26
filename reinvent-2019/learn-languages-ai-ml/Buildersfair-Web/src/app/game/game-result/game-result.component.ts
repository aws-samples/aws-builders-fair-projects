import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { GameResult } from 'src/app/_models/gameresult';
import { HttpClient } from '@angular/common/http';
import { GameResultService } from 'src/app/_services/gameresult.service';
import { LeaderboardService } from 'src/app/_services/leaderboard.service';
import { AlertifyService } from 'src/app/_services/alertify.service';

@Component({
  selector: 'app-game-result',
  templateUrl: './game-result.component.html',
  styleUrls: ['./game-result.component.css']
})
export class GameResultComponent implements OnInit {
  @Input() gameId: number;
  @Output() go = new EventEmitter<string>();
  gameResult: GameResult;
  gameRanking: number;
  constructor(private http: HttpClient,
              private gameResultService: GameResultService,
              private leaderboardService: LeaderboardService,
              private alertify: AlertifyService) { }

  ngOnInit() {
    this.getGameResult();
  }

  public getGameResult() {

    this.gameResultService.getGameResult(this.gameId).subscribe((gameResult: GameResult) => {
      this.gameResult = gameResult;
    }, error => {
      this.alertify.error(error);
    });

    this.leaderboardService.get(this.gameId).subscribe(response => {
      this.gameRanking = response;
    }, error => {
      this.alertify.error(error);
    });
  }

  gameStart() {
    this.go.emit('start');
  }
}
