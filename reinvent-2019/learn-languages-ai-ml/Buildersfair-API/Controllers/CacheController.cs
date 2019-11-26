using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
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
    public class CacheController : ControllerBase
    {
        private DataContext _context;

        public CacheController(DataContext context)
        {
            _context = context;
        }

        // GET api/cache/reload
        [HttpGet("reload")]
        public ActionResult<int> ReloadCache()
        {
            int gameResultCount = 0;

            var games = _context.Game.ToList();
            foreach (Game game in games)
            {
                var gameResults = _context.GameResult.Where(x => x.game_id == game.game_id).ToList();
                foreach (GameResult gameResult in gameResults)
                {
                    //Console.WriteLine("cache loading game result for game_id : " + game.game_id);
                    RedisUtil.AddGameResultToRedis(gameResult);
                    gameResultCount++;
                }
            }
            return gameResultCount;
        }

        // GET api/cache/clear
        [HttpGet("clear")]
        public ActionResult<bool> ClearCache()
        {
            // TODO: need to test
            // RedisUtil.ClearAll();

            return true;
        }
    }            
}