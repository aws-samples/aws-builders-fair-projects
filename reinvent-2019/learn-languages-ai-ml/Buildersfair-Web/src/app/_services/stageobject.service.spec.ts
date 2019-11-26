/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { StageobjectService } from './stageobject.service';

describe('Service: Stageobject', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [StageobjectService]
    });
  });

  it('should ...', inject([StageobjectService], (service: StageobjectService) => {
    expect(service).toBeTruthy();
  }));
});
