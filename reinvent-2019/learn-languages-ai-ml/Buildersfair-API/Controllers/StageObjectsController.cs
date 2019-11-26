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
    public class StageObjectsController : ControllerBase
    {
        private DataContext _context;
        IAmazonS3 S3Client { get; set; }
        IAmazonRekognition RekognitionClient { get; set; }        

        public StageObjectsController(DataContext context, IAmazonS3 s3Client, IAmazonRekognition rekognitionClient)
        {
            _context = context;
            this.S3Client = s3Client;
            this.RekognitionClient = rekognitionClient;            
        }

        // GET api/stageobjects
        [HttpGet]
        public async Task<IActionResult> GetStageObjects()
        {
            var values = await _context.StageObject.ToListAsync();
            return Ok(values);
        }

        // GET api/stageobjects/5
        [HttpGet("{game_id}")]
        public async Task<IActionResult> GetStageObject(int game_id, int stage_id)
        {
            var values = await _context.StageObject.Where(x => x.game_id == game_id && x.stage_id == stage_id).ToListAsync();
            return Ok(values);
        }

        // PUT api/stageobjects/5
        [HttpPut("{game_id}")]
        public void Put(int id, [FromBody] string value)
        {
        }

        // DELETE api/stageobjects/5
        [HttpDelete("{game_id}")]
        public void Delete(int id)
        {
        }       
    }
}