import { Component, OnInit, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-game-splash',
  templateUrl: './game-splash.component.html',
  styleUrls: ['./game-splash.component.css']
})
export class GameSplashComponent implements OnInit {
  @Input() stage: string;
  @Output() go = new EventEmitter<string>();
  constructor() { }

  ngOnInit() {
  }

  gameStart() {
    this.go.emit('start');
  }
}
