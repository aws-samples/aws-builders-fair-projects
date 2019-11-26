import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { GameService } from 'src/app/_services/game.service';
import { AlertifyService } from 'src/app/_services/alertify.service';
import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-game-start',
  templateUrl: './game-start.component.html',
  styleUrls: ['./game-start.component.css']
})
export class GameStartComponent implements OnInit {
  @Input() stage: string;
  @Input() gameId: number;
  @Output() gameCreated = new EventEmitter<number>();
  gameForm: FormGroup;

  constructor(private http: HttpClient,
              private gameService: GameService,
              private fb: FormBuilder,
              private alertify: AlertifyService) { }

  ngOnInit() {
    this.initGameForm();
  }

  initGameForm() {
    this.gameForm = this.fb.group({
      userName: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(50)]]
    });
  }

  createGame() {

    console.log(this.gameForm.value);

    this.gameService.createGame(this.gameForm.value).subscribe((newGameId: number) => {

      this.alertify.success('A new game created : ' + newGameId);
      this.gameStart(newGameId);
    }, error => {
      this.alertify.error(error);
    });
  }

  gameStart(newGameId: number) {
    this.gameId = newGameId;
    this.gameCreated.emit(this.gameId);
  }
}
