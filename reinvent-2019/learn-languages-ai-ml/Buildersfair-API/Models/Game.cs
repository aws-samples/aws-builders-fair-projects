using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace BuildersFair_API.Models
{
    [Table("tb_game")]
    public class Game
    {
        [Key]
        public int game_id { get; set; }
        public string name { get; set; }
        public DateTime start_date { get; set; }
        public DateTime? end_date { get; set; }      
    }
}