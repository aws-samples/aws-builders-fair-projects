import { Component, OnInit, Input, Output, EventEmitter, OnDestroy } from '@angular/core';
import { StageService } from 'src/app/_services/stage.service';
import { StageLogService } from 'src/app/_services/stagelog.service';
import { AlertifyService } from 'src/app/_services/alertify.service';
import { WebcamUtil, WebcamImage, WebcamInitError } from 'ngx-webcam';
import { StageInfo } from 'src/app/_models/stageinfo';
import { StageScore } from 'src/app/_models/stagescore';
import { Subject, Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { CardObject } from 'src/app/_models/object';

@Component({
  selector: 'app-game-stage',
  templateUrl: './game-stage.component.html',
  styleUrls: ['./game-stage.component.css']
})
export class GameStageComponent implements OnInit, OnDestroy {

  // ===============================================================================
  // Angular component constructor and destructor

  constructor(private http: HttpClient,
              private stageService: StageService,
              private stageLogService: StageLogService,
              private alertify: AlertifyService) { }

  public get triggerObservable(): Observable<void> {
    return this.trigger.asObservable();
  }

  public get nextWebcamObservable(): Observable<boolean|string> {
    return this.nextWebcam.asObservable();
  }
  @Input() stage: string;
  @Input() gameId: number;
  @Input() stageId: number;
  @Output() stageCompleted = new EventEmitter<number>();

  // stage info
  public difficulty = '';
  public message = '';
  public modalTimer: number;

  // score info
  public objectsScore: number;
  public timeScore: number;
  public clearScore: number;
  public stageScore: number;
  public totalScore: number;
  public stageIsCompleted: string;

  // object info
  public objects: CardObject[];
  public totalObjectCount = 0;
  public foundObjectCount = 0;

  // game status info
  public gameStarted = false;
  public isWaiting = false;

  // display control flags
  public displayStageStartModal = 'none';
  public displayStageClearModal = 'none';
  public displayStageFailedModal = 'none';
  public displayObjectList = false;

  // ===============================================================================
  // Timer handler
  // tslint:disable-next-line:member-ordering
  private intervalId = 0;
  // tslint:disable-next-line:member-ordering
  public seconds = 0.0;

  // ===============================================================================
  // Webcam handler

  // latest snapshot
  // tslint:disable-next-line:member-ordering
  public webcamImage: WebcamImage = null;

  // webcam snapshot trigger
  // tslint:disable-next-line:member-ordering
  private trigger: Subject<void> = new Subject<void>();

  // switch to next / previous / specific webcam; true/false: forward/backwards, string: deviceId
  // tslint:disable-next-line:member-ordering
  private nextWebcam: Subject<boolean|string> = new Subject<boolean|string>();

  // toggle webcam on/off
  // tslint:disable-next-line:member-ordering
  public showWebcam = true;
  // tslint:disable-next-line:member-ordering
  public allowCameraSwitch = true;
  // tslint:disable-next-line:member-ordering
  public multipleWebcamsAvailable = false;
  // tslint:disable-next-line:member-ordering
  public deviceId: string;
  // tslint:disable-next-line:member-ordering
  public videoOptions: MediaTrackConstraints = {
    // width: {ideal: 1024},
    // height: {ideal: 576}
  };

  // tslint:disable-next-line:member-ordering
  public errors: WebcamInitError[] = [];

  // ===============================================================================
  // audio handler

  // tslint:disable-next-line:member-ordering
  audioClock = new Audio();
  // tslint:disable-next-line:member-ordering
  audioShutter = new Audio();
  // tslint:disable-next-line:member-ordering
  audioFound = new Audio();
  // tslint:disable-next-line:member-ordering
  audioNotFound = new Audio();
  // tslint:disable-next-line:member-ordering
  audioStageClear = new Audio();
  audioStageFailed = new Audio();

  ngOnInit() {
    WebcamUtil.getAvailableVideoInputs()
      .then((mediaDevices: MediaDeviceInfo[]) => {
        this.multipleWebcamsAvailable = mediaDevices && mediaDevices.length > 1;
      });

    // Use enter key to get the current snapshot
    // tslint:disable-next-line:only-arrow-functions
    document.body.addEventListener('keypress', function(event) {
      if (event.keyCode === 13) {
          console.log('You pressed Enter key.');
          document.getElementById('buttonSnapshot').click();
      }
    });

    this.loadAudio();

    this.stageId = 1;
    this.totalScore = 0;
    this.getStageInfo();
  }

  ngOnDestroy() {
    this.clearTimer();
  }

  // ===============================================================================
  // Game play flow related functions
  onStageStart() {
    // start game
    this.displayStageStartModal = 'none';
    this.displayObjectList = true;
    this.isWaiting = false;
    this.gameStarted = true;

    this.addStageLog();
    this.runTimer();
  }

  onStageEnd() {
    //
    this.displayStageClearModal = 'none';
    this.displayStageFailedModal = 'none';

    if (this.stageIsCompleted === 'Y' && this.stageId < 2) {
      this.stageId++;
      this.displayObjectList = false;

      this.getStageInfo();
    } else {
      // go to result page
      this.stageCompleted.emit(this.stageId);
    }
  }

  gameEnd() {
    console.log('game end!');
    this.stageCompleted.emit(0);
  }

  // ===============================================================================
  // API call handlers
  public getStageInfo() {
    this.stageService.getStage(this.gameId, this.stageId).subscribe((stageInfo: StageInfo) => {
      // get stage objects
      this.objects = stageInfo.stage_objects;
      this.totalObjectCount = this.objects.length;
      this.foundObjectCount = 0;

      // init score
      this.objectsScore = 0;
      this.timeScore = 0;
      this.clearScore = 0;
      this.stageScore = 0;

      // stage info
      this.seconds = stageInfo.stage_time;
      this.difficulty = stageInfo.stage_difficulty;

      // show start modal dialog
      this.displayStageStartModal = 'block';
      this.modalTimer = 4;
      this.intervalId = window.setInterval(() => {
        this.modalTimer -= 1;

        if (this.modalTimer === 0 || this.modalTimer < 0) {

          clearInterval(this.intervalId);
          this.modalTimer = 0;
          this.onStageStart();
        }
      }, 1000);

    });
  }

  public uploadPicture() {

    // avoid duplicated processing
    if (this.isWaiting === true) { return; }

    this.message = '';
    this.isWaiting = true;
    this.alertify.message('Working on it...');

    const pictureInfo = {
      game_id: this.gameId,
      stage_id: this.stageId,
      base64Image: this.webcamImage.imageAsBase64
    };

    this.stageService.uploadPicture(pictureInfo).subscribe((stageScore: StageScore) => {

      this.isWaiting = false;

      const element: HTMLElement = document.getElementById(stageScore.object_name) as HTMLElement;
      if (element) {
        this.audioFound.play();

        element.style.backgroundColor = 'grey';

        this.objectsScore += stageScore.object_score;
        this.totalScore += stageScore.object_score;
        this.foundObjectCount++;

        this.message = 'Great!';
        if (this.foundObjectCount === this.totalObjectCount) {
          this.clearTimer();
          this.gameStarted = false;

          this.clearScore = this.stageId * 300;
          this.timeScore = Math.round(this.seconds * 100);
          this.totalScore += this.clearScore;
          this.totalScore += this.timeScore;
          this.stageScore = this.objectsScore + this.clearScore + this.timeScore;
          this.stageIsCompleted = 'Y';

          this.updateStageLog();

          // show stage clear modal dialog
          this.displayStageClearModal = 'block';
          this.audioStageClear.play();
        }
      } else {
        this.audioNotFound.play();

        this.message = 'Try again!';
      }

    }, error => {
      this.isWaiting = false;
      this.alertify.error('Something wrong. Try again.');
    });
  }

  public addStageLog() {

    const stageLog = {
      game_id: this.gameId,
      stage_id: this.stageId
    };

    this.stageLogService.addStageLog(stageLog).subscribe(response => {
      console.log(response);
    }, error => {
      console.log('addStageLog failed.');
    });
  }

  public updateStageLog() {

    const stageLog = {
      game_id: this.gameId,
      stage_id: this.stageId,
      found_objects: this.foundObjectCount,
      objects_score: this.objectsScore,
      time_score: this.timeScore,
      clear_score: this.clearScore,
      stage_score: this.stageScore,
      total_score: this.totalScore,
      completed_yn : this.stageIsCompleted
    };

    this.stageLogService.updateStageLog(stageLog).subscribe(response => {
      console.log(response);
    }, error => {
      console.log('updateStageLog failed.');
    });
  }

  private clearTimer() {
    this.audioClock.pause();
    clearInterval(this.intervalId);
  }

  public runTimer() {
    this.clearTimer();

    this.audioClock.play();

    this.intervalId = window.setInterval(() => {
      this.seconds -= 0.1;

      if (this.seconds === 0 || this.seconds < 0) {
        this.clearTimer();
        this.seconds = 0;

        this.isWaiting = false;
        this.gameStarted = false;

        this.clearScore = 0;
        this.timeScore = 0;
        this.stageScore = this.objectsScore;
        this.stageIsCompleted = 'N';

        this.alertify.success('Time over!');

        this.updateStageLog();

        // show stage failed modal dialog
        this.displayStageFailedModal = 'block';
        this.audioStageFailed.play();
      }
    }, 100);
  }

  public triggerSnapshot(): void {
    this.trigger.next();

    this.audioShutter.play();

    this.uploadPicture();
  }

  public toggleWebcam(): void {
    this.showWebcam = !this.showWebcam;
  }

  public handleInitError(error: WebcamInitError): void {
    this.errors.push(error);
  }

  public showNextWebcam(directionOrDeviceId: boolean|string): void {
    // true => move forward through devices
    // false => move backwards through devices
    // string => move to device with given deviceId
    this.nextWebcam.next(directionOrDeviceId);
  }

  public handleImage(webcamImage: WebcamImage): void {
    console.log('received webcam image', webcamImage);
    this.webcamImage = webcamImage;
  }

  public cameraWasSwitched(deviceId: string): void {
    console.log('active device: ' + deviceId);
    this.deviceId = deviceId;
  }

  public loadAudio() {
    this.audioClock.src = '../../../assets/audios/clock-ticking.mp3';
    this.audioClock.loop = true;
    this.audioClock.load();

    this.audioShutter.src = '../../../assets/audios/camera-shutter-click.mp3';
    this.audioShutter.load();

    this.audioFound.src = '../../../assets/audios/found.mp3';
    this.audioFound.load();

    this.audioNotFound.src = '../../../assets/audios/not-found.mp3';
    this.audioNotFound.load();

    this.audioStageClear.src = '../../../assets/audios/stage-clear.mp3';
    this.audioStageClear.load();

    this.audioStageFailed.src = '../../../assets/audios/stage-fail.mp3';
    this.audioStageFailed.load();
  }

}
