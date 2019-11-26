import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavComponent } from './nav/nav.component';
import { HomeComponent } from './home/home.component';
import { GameComponent } from './game/game.component';
import { LeaderboardComponent } from './leaderboard/leaderboard.component';
import { DebugComponent } from './debug/debug.component';
import { TestComponent } from './test/test.component';
import { GameService } from './_services/game.service';
import { StageLogService } from './_services/stagelog.service';
import { LeaderboardService } from './_services/leaderboard.service';
import { HttpClientModule } from '@angular/common/http';
import { StageService } from './_services/stage.service';
import { StageObjectService } from './_services/stageobject.service';
import { AlertifyService } from './_services/alertify.service';
import { GameResultService } from './_services/gameresult.service';
import { WebcamModule } from 'ngx-webcam';
import { TrailerComponent } from './trailer/trailer.component';
import { GameStageComponent } from './game/game-stage/game-stage.component';
import { GameSplashComponent } from './game/game-splash/game-splash.component';
import { GameStartComponent } from './game/game-start/game-start.component';
import { GameResultComponent } from './game/game-result/game-result.component';
import { ReactiveFormsModule } from '@angular/forms';
import { TestRekognitionComponent } from './test/test-rekognition/test-rekognition.component';
import { TestTextractComponent } from './test/test-textract/test-textract.component';
import { TestTranscribeComponent } from './test/test-transcribe/test-transcribe.component';
import { TestPollyComponent } from './test/test-polly/test-polly.component';

@NgModule({
   declarations: [
      AppComponent,
      NavComponent,
      HomeComponent,
      LeaderboardComponent,
      DebugComponent,
      TrailerComponent,
      GameComponent,
      GameStageComponent,
      GameSplashComponent,
      GameStartComponent,
      GameResultComponent,
      TestComponent,
      TestRekognitionComponent,
      TestTextractComponent,
      TestPollyComponent,
      TestTranscribeComponent
   ],
   imports: [
      BrowserModule,
      HttpClientModule,
      AppRoutingModule,
      WebcamModule,
      ReactiveFormsModule
   ],
   providers: [
      GameService,
      GameResultService,
      StageLogService,
      LeaderboardService,
      StageService,
      StageObjectService,
      AlertifyService
   ],
   bootstrap: [
      AppComponent
   ]
})
export class AppModule { }
