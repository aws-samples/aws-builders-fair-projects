/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { StageService } from './stage.service';

describe('Service: Stage', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [StageService]
    });
  });

  it('should ...', inject([StageService], (service: StageService) => {
    expect(service).toBeTruthy();
  }));
});
