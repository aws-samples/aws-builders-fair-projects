export interface StageLog {
    game_id: number;
    stage_id: number;
    objects_score: number;
    time_score: number;
    clear_score: number;
    stage_score: number;
    total_score: number;
    completed_yn: string;
    start_date: Date;
    end_date: Date;
}
