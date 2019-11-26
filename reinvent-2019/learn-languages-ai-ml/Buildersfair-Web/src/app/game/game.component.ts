import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css']
})
export class GameComponent implements OnInit {
  stage: string;
  gameId: number;
  stageId: number;

  constructor() { }

  ngOnInit() {
    this.stage = 'start';
    this.gameId = 0;
    this.stageId = 0;
  }

  goStage(stage: string) {
    this.stage = stage;
  }

  onGameCreated(gameId: number) {
    this.gameId = gameId;
    this.goStage('stage');

  }

  onStageCompleted(stageId: number) {
    let isGameCompleted = false;

    if (stageId === 0 || stageId >= 2) {
      isGameCompleted = true;
    }

    if (isGameCompleted) {
      this.goStage('result');
    } else {
      this.goStage('stage');
    }
  }
}
