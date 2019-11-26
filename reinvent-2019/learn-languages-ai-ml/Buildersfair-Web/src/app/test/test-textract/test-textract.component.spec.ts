/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { TestTextractComponent } from './test-textract.component';

describe('TestTextractComponent', () => {
  let component: TestTextractComponent;
  let fixture: ComponentFixture<TestTextractComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TestTextractComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TestTextractComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
