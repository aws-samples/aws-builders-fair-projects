/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { StagelogService } from './stagelog.service';

describe('Service: Stagelog', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [StagelogService]
    });
  });

  it('should ...', inject([StagelogService], (service: StagelogService) => {
    expect(service).toBeTruthy();
  }));
});
