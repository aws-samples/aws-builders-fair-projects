using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace BuildersFair_API.Models
{
    [Table("tb_game_result")]
    public class GameResult
    {
        [Key]
        public int game_id { get; set; }
        public string name { get; set; }
        public int total_score { get; set; }
        public int total_rank { get; set; }
        public int total_found_objects { get; set; }
        public int total_playtime { get; set; } // sec
    }
}