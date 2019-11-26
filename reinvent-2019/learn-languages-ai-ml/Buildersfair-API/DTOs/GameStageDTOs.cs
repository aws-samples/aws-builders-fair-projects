using System.Collections.Generic;

namespace BuildersFair_API.DTOs
{
    public class StagePostImageDTO
    {
        public int game_id { get; set; }
        public int stage_id { get; set; }
        public string base64Image { get; set; }
    }

    public class StageObjectDTO
    {
        public string object_name { get; set; }
        public string object_display_name { get; set; }
        public string object_image_uri { get; set; }
    }

    public class StageInfoDTO
    {
        public int game_id { get; set; }
        public int stage_id { get; set; }
        public int stage_time { get; set; }
        public string stage_difficulty { get; set; }
        public List<StageObjectDTO> stage_objects { get; set; }
    }

    public class StageScoreDTO
    {
        public int game_id { get; set; }
        public int stage_id { get; set; }
        public string object_name { get; set; }
        public int object_score { get; set; }
        public int stage_score { get; set; }
    }
}