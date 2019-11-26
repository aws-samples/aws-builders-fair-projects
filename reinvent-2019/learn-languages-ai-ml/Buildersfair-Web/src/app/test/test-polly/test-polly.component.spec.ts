/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { TestPollyComponent } from './test-polly.component';

describe('TestPollyComponent', () => {
  let component: TestPollyComponent;
  let fixture: ComponentFixture<TestPollyComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TestPollyComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TestPollyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
