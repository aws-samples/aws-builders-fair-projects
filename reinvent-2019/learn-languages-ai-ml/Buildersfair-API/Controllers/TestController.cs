using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Amazon.Polly;
using Amazon.Rekognition;
using Amazon.Rekognition.Model;
using Amazon.S3;
using Amazon.Textract;
using Amazon.Textract.Model;
using Amazon.TranscribeService;
using Buildersfair_API.Utils;
using BuildersFair_API.Data;
using BuildersFair_API.DTOs;
using BuildersFair_API.Utils;
using Microsoft.AspNetCore.Mvc;

namespace BuildersFair_API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class TestController : ControllerBase
    {
        private DataContext _context;
        IAmazonS3 S3Client { get; set; }
        IAmazonRekognition RekognitionClient { get; set; }
        IAmazonTextract TextractClient { get; set; }
        IAmazonPolly PollyClient { get; set; }
        IAmazonTranscribeService TranscribeClient { get; set; }

        public TestController(DataContext context, IAmazonS3 s3Client,
            IAmazonRekognition rekognitionClient, IAmazonTextract textractClient,
            IAmazonPolly pollyClient, IAmazonTranscribeService transcribeClient)
        {
            _context = context;
            this.S3Client = s3Client;
            this.RekognitionClient = rekognitionClient;
            this.TextractClient = textractClient;
            this.PollyClient = pollyClient;
            this.TranscribeClient = transcribeClient;
        }

        // POST api/test/rekognition
        [Route("rekognition")]
        [HttpPost]
        public async Task<IActionResult> RekognitionTest([FromBody] RekognitionTestDTO dto)
        {
            List<Label> labels = null;

            Guid g = Guid.NewGuid();
            string guidString = Convert.ToBase64String(g.ToByteArray());
            guidString = guidString.Replace("=", "");
            guidString = guidString.Replace("+", "");
            guidString = guidString.Replace("/", "");

            // Retrieving image data
            string keyName = string.Format("test/{0}.jpg", guidString);
            byte[] imageByteArray = Convert.FromBase64String(dto.base64Image);
            if (imageByteArray.Length == 0)
                return BadRequest("Image length is 0.");

            using (MemoryStream ms = new MemoryStream(imageByteArray))
            {
                // call Rekonition API
                labels = await RekognitionUtil.GetObjectDetailFromStream(this.RekognitionClient, ms);

                // Upload image to S3 bucket
                // await Task.Run(() => S3Util.UploadToS3(this.S3Client, "S3_BUCKET_NAME_HERE", "KEY_NAME_HERE", ms));
            }

            return Ok(labels);
        }

        // POST api/test/textract
        [Route("textract")]
        [HttpPost]
        public async Task<IActionResult> TextractTest([FromBody] TextractTestDTO dto)
        {
            List<Block> blocks = null;

            Guid g = Guid.NewGuid();
            string guidString = Convert.ToBase64String(g.ToByteArray());
            guidString = guidString.Replace("=", "");
            guidString = guidString.Replace("+", "");
            guidString = guidString.Replace("/", "");

            // Retrieving image data
            string keyName = string.Format("test/{0}.jpg", guidString);
            byte[] imageByteArray = Convert.FromBase64String(dto.base64Image);
            if (imageByteArray.Length == 0)
                return BadRequest("Image length is 0.");

            using (MemoryStream ms = new MemoryStream(imageByteArray))
            {
                // call Textract API
                blocks = await TextractUtil.GetTextFromStream(this.TextractClient, ms);

                // Upload image to S3 bucket
                // await Task.Run(() => S3Util.UploadToS3(this.S3Client, "S3_BUCKET_NAME_HERE", "KEY_NAME_HERE", ms));
            }

            return Ok(blocks);
        }

        // POST api/test/polly
        [Route("polly")]
        [HttpPost]
        public async Task<IActionResult> PollyTest([FromBody] PollyTestDTO dto)
        {
            PollyResultDTO result = new PollyResultDTO();

            Guid g = Guid.NewGuid();
            string guidString = Convert.ToBase64String(g.ToByteArray());
            guidString = guidString.Replace("=", "");
            guidString = guidString.Replace("+", "");
            guidString = guidString.Replace("/", "");

            // Validation check
            if (string.IsNullOrWhiteSpace(dto.language_code) == true)
                return BadRequest("Language code is empty.");

            if (string.IsNullOrWhiteSpace(dto.text) == true)
                return BadRequest("Text is empty.");

            if (string.IsNullOrWhiteSpace(dto.voice_name) == true)
                return BadRequest("Voice name is empty.");                

            // Console.WriteLine(dto.voice_name);

            // call Polly API
            result.mediaUri = await PollyUtil.PollyDemo(this.PollyClient, this.S3Client, dto.language_code, dto.text, dto.voice_name);

            return Ok(result);
        }

        // GET api/test/polly/languages
        [Route("polly/languages")]
        [HttpGet]
        public async Task<IActionResult> GetPollyLanguages()
        {
            var languages = await PollyUtil.GetLanguageList(this.PollyClient);
            return Ok(languages);
        }

        // GET api/test/polly/voices
        [Route("polly/voices")]
        [HttpGet]
        public async Task<IActionResult> GetPollyVoices(string languageCode)
        {
            var voices = await PollyUtil.GetVoiceList(this.PollyClient, languageCode);
            return Ok(voices);
        }

        // POST api/test/transcribe
        [Route("transcribe")]
        [HttpPost]
        //public async Task<IActionResult> TranscribeTest([FromBody] TranscribeTestDTO dto)
        public async Task<IActionResult> TranscribeTest([FromForm] TranscribeTestDTO dto)
        {
            string transcriptionUri = null;

            Guid g = Guid.NewGuid();
            string guidString = Convert.ToBase64String(g.ToByteArray());
            guidString = guidString.Replace("=", "");
            guidString = guidString.Replace("+", "");
            guidString = guidString.Replace("/", "");

            // Validation check
            if (string.IsNullOrWhiteSpace(dto.language_code) == true)
                return BadRequest("language_code is empty.");

            if (dto.WAVblob == null || dto.WAVblob.Length <= 0)
                return BadRequest("WAVblob is empty.");

            using (MemoryStream ms = new MemoryStream())
            {
                dto.WAVblob.CopyTo(ms);

                // Upload image to S3 bucket
                await Task.Run(() => S3Util.UploadToS3(this.S3Client, "reinvent-indiamazones", "transcribe_test/mytest.wav", ms));
            }

            string mediaUri = "https://reinvent-indiamazones.s3-us-west-2.amazonaws.com/transcribe_test/mytest.wav";

            // call Transcribe API
            transcriptionUri = await TranscribeUtil.TranscribeDemo(this.TranscribeClient, dto.language_code, mediaUri);

            return Ok(transcriptionUri);
        }

        // GET api/test/transcribe/languages
        [Route("transcribe/languages")]
        [HttpGet]
        public IActionResult GetTranscribeLanguages()
        {
            var languages = TranscribeUtil.GetLanguageList(this.TranscribeClient);
            return Ok(languages);
        }
    }
}