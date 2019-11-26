using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Amazon.S3;
using BuildersFair_API.Data;
using BuildersFair_API.Models;
using BuildersFair_API.Utils;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StackExchange.Redis;

namespace BuildersFair_API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class GameResultsController : ControllerBase
    {
        private DataContext _context;
        IAmazonS3 S3Client { get; set; }

        public GameResultsController(DataContext context, IAmazonS3 s3Client)
        {
            _context = context;
            this.S3Client = s3Client;
        }

        // GET api/gameresults
        [HttpGet]
        public async Task<IActionResult> GetGameResults()
        {
            var values = await _context.GameResult.ToListAsync();
            return Ok(values);
        }

        // GET api/gameresults/5
        [HttpGet("{game_id}")]
        public async Task<IActionResult> GetGameResult(int game_id)
        {
            var value = await _context.GameResult.FirstOrDefaultAsync(x => x.game_id == game_id);
            return Ok(value);
        }

        // PUT api/gameresults/5
        [HttpPut("{game_id}")]
        public void Put(int game_id, [FromBody] string value)
        {
        }

        // DELETE api/gameresults/5
        [HttpDelete("{game_id}")]
        public async Task<IActionResult> Delete(int game_id)
        {
            GameResult gameResult = new GameResult() { game_id = game_id };
            _context.GameResult.Remove(gameResult);
            var result = await _context.SaveChangesAsync();

            return Ok(result);
        }
    }            
}