/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { GameSplashComponent } from './game-splash.component';

describe('GameSplashComponent', () => {
  let component: GameSplashComponent;
  let fixture: ComponentFixture<GameSplashComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GameSplashComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GameSplashComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
