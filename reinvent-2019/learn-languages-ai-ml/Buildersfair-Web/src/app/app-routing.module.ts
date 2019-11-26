import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LeaderboardComponent } from './leaderboard/leaderboard.component';
import { GameComponent } from './game/game.component';
import { DebugComponent } from './debug/debug.component';
import { TestComponent } from './test/test.component';
import { TrailerComponent } from './trailer/trailer.component';

const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'leaderboard', component: LeaderboardComponent },
  { path: 'game', component: GameComponent },
  { path: 'debug', component: DebugComponent },
  { path: 'playdemo', component: TestComponent },
  { path: 'trailer', component: TrailerComponent },
  { path: '**', redirectTo: 'home', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
