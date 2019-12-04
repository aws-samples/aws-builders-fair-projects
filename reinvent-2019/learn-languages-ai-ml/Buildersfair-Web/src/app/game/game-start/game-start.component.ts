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
  languageCode: string;

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

  // tslint:disable-next-line: use-lifecycle-interface
  ngAfterViewInit() {
    document.getElementById('btnEnglish').click();
  }

  createGame() {

    const username = document.getElementById('userName') as HTMLInputElement;

    const gameInfo = {
      user_name: username.value,
      language_code: this.languageCode
    };

    this.gameService.createGame(gameInfo).subscribe((newGameId: number) => {

      this.alertify.success('A new game created : ' + newGameId);
      this.gameStart(newGameId);
    }, error => {
      this.alertify.error(error);
    });
  }

  selectLanguage(languageCode: string) {
    this.languageCode = languageCode;
    // console.log(this.languageCode);

    this.selectButton('btnEnglish', false);
    this.selectButton('btnKorean', false);
    this.selectButton('btnChinese', false);
    this.selectButton('btnJapanese', false);
    this.selectButton('btnSpanish', false);

    switch (this.languageCode) {
      case 'en-US':
        this.selectButton('btnEnglish', true);
        break;
      case 'ko-KR':
        this.selectButton('btnKorean', true);
        break;
      case 'cmn-CN':
        this.selectButton('btnChinese', true);
        break;
      case 'ja-JP':
        this.selectButton('btnJapanese', true);
        break;
      case 'es-ES':
        this.selectButton('btnSpanish', true);
        break;
    }
  }

  selectButton(elementId: string, flag: boolean) {

    const x = document.getElementById(elementId);

    if (flag === false) {
      x.classList.remove('btn-secondary');
      x.classList.add('btn-light');
    } else {
      x.classList.remove('btn-light');
      x.classList.add('btn-secondary');
    }
  }

  gameStart(newGameId: number) {
    this.gameId = newGameId;
    this.gameCreated.emit(this.gameId);
  }
}
