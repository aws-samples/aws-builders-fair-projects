/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { TestRekognitionComponent } from './test-rekognition.component';

describe('TestRekognitionComponent', () => {
  let component: TestRekognitionComponent;
  let fixture: ComponentFixture<TestRekognitionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TestRekognitionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TestRekognitionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
