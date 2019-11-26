/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { GameresultService } from './gameresult.service';

describe('Service: Gameresult', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [GameresultService]
    });
  });

  it('should ...', inject([GameresultService], (service: GameresultService) => {
    expect(service).toBeTruthy();
  }));
});
