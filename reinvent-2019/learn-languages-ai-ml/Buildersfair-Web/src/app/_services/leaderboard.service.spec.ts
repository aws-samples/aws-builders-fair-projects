/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { LeaderboardService } from './leaderboard.service';

describe('Service: Leaderboard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [LeaderboardService]
    });
  });

  it('should ...', inject([LeaderboardService], (service: LeaderboardService) => {
    expect(service).toBeTruthy();
  }));
});
