using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace BuildersFair_API.Models
{
    [Table("tb_stage_log")]
    public class StageLog
    {
        public int game_id { get; set; }
        public int stage_id { get; set; }
        public int objects_score { get; set; }
        public int time_score { get; set; }
        public int clear_score { get; set; }
        public int stage_score { get; set; }
        public int total_score { get; set; }
        public string completed_yn { get; set; } // Y/N
        public DateTime start_date { get; set; } 
        public DateTime? end_date { get; set; } 
    }
}