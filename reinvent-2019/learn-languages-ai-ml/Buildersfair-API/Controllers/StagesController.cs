using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Amazon.Rekognition;
using Amazon.Rekognition.Model;
using Amazon.S3;
using Amazon.Textract;
using Amazon.Textract.Model;
using Buildersfair_API.Utils;
using BuildersFair_API.Data;
using BuildersFair_API.DTOs;
using BuildersFair_API.Models;
using BuildersFair_API.Utils;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace BuildersFair_API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class StagesController : ControllerBase
    {
        private DataContext _context;
        IAmazonS3 S3Client { get; set; }
        IAmazonRekognition RekognitionClient { get; set; }
        IAmazonTextract TextractClient { get; set; } 

        public StagesController(DataContext context, 
            IAmazonS3 s3Client, IAmazonRekognition rekognitionClient,
            IAmazonTextract textractClient)
        {
            _context = context;
            this.S3Client = s3Client;
            this.RekognitionClient = rekognitionClient;
            this.TextractClient = textractClient;        
        }

        [HttpGet]
        public async Task<IActionResult> GetStageInfo([FromQuery(Name="game_id")] int gameId, [FromQuery(Name="stage_id")] int stageId)
        {
            StageInfoDTO stageInfo = new StageInfoDTO();

            if (gameId == 0 || stageId == 0)
                return BadRequest("Invalid Parameter. Please check game_id and stage_id parameter values.");

            stageInfo.game_id = gameId;
            stageInfo.stage_id = stageId;

            // set gaming rule
            int difficulty = 0;
            int objectCount = 0;
            int objectScore = 0;
            switch (stageId)
            {
                case 1:
                    stageInfo.stage_time = 60;
                    stageInfo.stage_difficulty = "Easy";
                    difficulty = 1;
                    objectCount = 3;
                    objectScore = 50;
                    break;
                case 2:
                    stageInfo.stage_time = 60;
                    stageInfo.stage_difficulty = "Easy";
                    difficulty = 1;
                    objectCount = 3;
                    objectScore = 50;
                    break;
                // case 3:
                //     stageInfo.stage_time = 100;
                //     stageInfo.stage_difficulty = "Hard";
                //     difficulty = 2;
                //     objectCount = 10;
                //     objectScore = 100;
                //     break;
                default:
                    // need exception handling logic for bad stageId
                    break;
            }
            
            // get object list randomly
            //List<string> objectList = GetRandomStageObjectList(difficulty, objectCount);
            List<StageObjectDTO> objectList = GetRandomStageObjectList(difficulty, objectCount);
            stageInfo.stage_objects = objectList;

            // Add object list to StageObject table
            List<StageObject> stageObjectList = new List<StageObject>();
            //foreach (string item in objectList)
            foreach (StageObjectDTO item in objectList)
            {
                StageObject stageObject = new StageObject()
                {
                    game_id = gameId,
                    stage_id = stageId,
                    object_name = item.object_name,
                    object_score = objectScore,
                    found_yn = "N",
                    log_date = DateTime.Now
                };
                stageObjectList.Add(stageObject);
                _context.StageObject.Add(stageObject);
            }
            await _context.SaveChangesAsync();

            return Ok(stageInfo);
        }

        // POST api/stages
        [HttpPost]
        public async Task<IActionResult> Post([FromBody] StagePostImageDTO dto)
        {
            //Console.WriteLine("PostImage entered.");
            
            StageScoreDTO stageScore = new StageScoreDTO();
            stageScore.game_id = dto.game_id;
            stageScore.stage_id = dto.stage_id;
            
            Guid g = Guid.NewGuid();
            string guidString = Convert.ToBase64String(g.ToByteArray());
            guidString = guidString.Replace("=","");
            guidString = guidString.Replace("+","");
            guidString = guidString.Replace("/","");
            
            // Retrieving image data
            byte[] imageByteArray = Convert.FromBase64String(dto.base64Image);
            if (imageByteArray.Length == 0)
                return BadRequest("Image length is 0.");

            using (MemoryStream ms = new MemoryStream(imageByteArray))
            {

                if (dto.stage_id == 1)
                {
                    // call Rekonition API
                    List<Label> labels = await RekognitionUtil.GetObjectDetailFromStream(this.RekognitionClient, ms); 
                    List<string> labelNames = new List<string>();
                    foreach (Label label in labels)
                    {
                        labelNames.Add(label.Name);
                        Console.Write(label.Name + " ");
                    }
                    var matchedObject = _context.StageObject.Where(x => x.game_id == dto.game_id && 
                                            x.stage_id == dto.stage_id &&
                                            x.found_yn == "N" &&
                                            labelNames.Contains(x.object_name)).FirstOrDefault();
                    if (matchedObject != null)
                    {
                        //Console.WriteLine("Matched object: " + matchedObject.object_name);
                        stageScore.object_name = matchedObject.object_name;
                        stageScore.object_score = matchedObject.object_score;
                        matchedObject.found_yn = "Y";

                        _context.StageObject.Update(matchedObject);
                        await _context.SaveChangesAsync();
                    }
                    else
                    {
                        Console.WriteLine("no matched object");
                    }
                }
                else if (dto.stage_id == 2)
                {
                    // call Textract API
                    List<Block> blocks = await TextractUtil.GetTextFromStream(this.TextractClient, ms); 
                    List<string> texts = new List<string>();
                    foreach (Block block in blocks)
                    {
                        texts.Add(block.Text);
                        Console.Write(block.Text + " ");
                    }
                    var matchedObject = _context.StageObject.Where(x => x.game_id == dto.game_id && 
                                            x.stage_id == dto.stage_id &&
                                            x.found_yn == "N" &&
                                            texts.Contains(x.object_name)).FirstOrDefault();
                    if (matchedObject != null)
                    {
                        //Console.WriteLine("Matched object: " + matchedObject.object_name);
                        stageScore.object_name = matchedObject.object_name;
                        stageScore.object_score = matchedObject.object_score;
                        matchedObject.found_yn = "Y";

                        _context.StageObject.Update(matchedObject);
                        await _context.SaveChangesAsync();
                    }
                    else
                    {
                        Console.WriteLine("no matched object");
                    }
                }
            }
            
            return Ok(stageScore);            
        }  
    
        private List<StageObjectDTO> GetRandomStageObjectList(int difficulty, int objectCount, string language = "en")
        {
            List<string> nameList = new List<String>();
            List<StageObjectDTO> objectList = new List<StageObjectDTO>();

            int recordCount = _context.Object.Where(x => x.difficulty == difficulty).Count();
            var records = _context.Object.Where(x => x.difficulty == difficulty);

            for (int i = 0; i < objectCount && i < recordCount; i++)
            {
                bool loop = true;
                while (loop)
                {
                    int randomRecord = new Random().Next() % recordCount;
                    var record = records.Skip(randomRecord).Take(1).First();

                    if (nameList.Contains(record.object_name) == false)
                    {
                        nameList.Add(record.object_name);

                        StageObjectDTO stageObject = new StageObjectDTO();
                        stageObject.object_name = record.object_name;

                        switch (language)
                        {
                            case "ko":
                                stageObject.object_display_name = record.object_name_ko;
                                break;
                            case "ja":
                                stageObject.object_display_name = record.object_name_ja;
                                break;
                            case "cn":
                                stageObject.object_display_name = record.object_name_cn;
                                break;
                            case "es":
                                stageObject.object_display_name = record.object_name_es;
                                break;
                            default:
                                stageObject.object_display_name = record.object_name;
                                break;                                
                        }
                        stageObject.object_image_uri = "";

                        objectList.Add(stageObject);

                        loop = false;
                    }
                }
            }

            return objectList;
        }   
    }
}