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

namespace BuildersFair_API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class RankingsController : ControllerBase
    {
        private DataContext _context;
        IAmazonS3 S3Client { get; set; }

        public RankingsController(DataContext context, IAmazonS3 s3Client)
        {
            _context = context;
            this.S3Client = s3Client;
        }

        // GET api/rankings
        [HttpGet]
        public ActionResult<List<GameResult>> GetRankings()
        {
            var topRankings = RedisUtil.GetTopRankings(0, 9);

            return topRankings;
        }

        // GET api/rankings/5
        [HttpGet("{game_id}")]
        public int GetRankingsByGameId(int game_id)
        {
            int total_rank = RedisUtil.GetGameRanking(game_id) + 1;
            return total_rank;
        }

        // POST api/rankings
        [HttpPost]
        public void Post([FromBody] string value)
        {
        }

        // PUT api/rankings/5
        [HttpPut("{seqNum}")]
        public void Put(int id, [FromBody] string value)
        {
        }

        // DELETE api/rankings/5
        [HttpDelete("{seqNum}")]
        public void Delete(int id)
        {
        }
    }
}