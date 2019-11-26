using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace BuildersFair_API.Models
{
    [Table("tb_stage_object")]
    public class StageObject
    {
        public int game_id { get; set; }
        public int stage_id { get; set; }
        public string object_name { get; set; }
        public int object_score { get; set; }
        public string found_yn { get; set; } // Y/N
        public string file_loc { get; set; } 
        public DateTime log_date { get; set; } 
    }
}