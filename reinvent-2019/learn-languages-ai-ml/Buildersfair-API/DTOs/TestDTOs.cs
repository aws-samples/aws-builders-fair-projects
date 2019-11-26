namespace BuildersFair_API.DTOs
{
    public class RekognitionTestDTO
    {
        public string base64Image { get; set; }
    }

    public class TextractTestDTO
    {
        public string base64Image { get; set; }
    }

    public class PollyTestDTO
    {
        public string text { get; set; }
    }

    public class PollyLanguageDTO
    {
        public string language_code { get; set; }
        public string language_name { get; set; }
    }

    public class PollyVoiceDTO
    {
        public string voice_name { get; set; }
        public string gender { get; set; }
    }    

    public class PollyResultDTO
    {
        public string mediaUri { get; set; }
    }

    public class TranscribeTestDTO
    {
        public string mediaUri { get; set; }
    }

    public class TranscribeLanguageDTO
    {
        public string language { get; set; }
        public string language_code { get; set; }

        public TranscribeLanguageDTO(string language, string language_code)
        {
            this.language = language;
            this.language_code = language_code;
        }     
    }
}