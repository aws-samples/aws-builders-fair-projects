import { CardObject } from './object';

export interface StageInfo {
    game_id: number;
    stage_id: number;
    stage_time: number;
    stage_difficulty: string;
    stage_objects: CardObject[];
}
