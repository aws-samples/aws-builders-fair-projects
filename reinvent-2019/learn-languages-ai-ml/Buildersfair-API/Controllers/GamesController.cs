using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BuildersFair_API.Data;
using BuildersFair_API.DTOs;
using BuildersFair_API.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace BuildersFair_API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class GamesController : ControllerBase
    {
        private DataContext _context;

        public GamesController(DataContext context)
        {
            _context = context;
        }

        // GET api/games
        [HttpGet]
        public async Task<IActionResult> GetGames()
        {
            var values = await _context.Game.ToListAsync();
            return Ok(values);
        }

        // GET api/games/5
        [HttpGet("{game_id}")]
        public async Task<IActionResult> GetUserScore(int game_id)
        {
            var value = await _context.Game.FirstOrDefaultAsync(x => x.game_id == game_id);
            return Ok(value);
        }

        // POST api/games
        [HttpPost]
        public async Task<IActionResult> AddNewGame([FromBody] GameCreateDTO game)
        {
            Game newGame = new Game{
                name = game.userName,
                start_date = DateTime.Now
            };

            var value = _context.Game.Add(newGame);
            await _context.SaveChangesAsync();

            return Ok(newGame.game_id);            
        }

        // PUT api/games/5
        [HttpPut("{game_id}")]
        public async Task<IActionResult> Put(int game_id, [FromForm] string shareYN)
        {
            Game game = await _context.Game.FirstOrDefaultAsync(x => x.game_id == game_id);
            if (game != null)
            {
                game.end_date = DateTime.Now;
            }

            var value = _context.Game.Update(game);
            await _context.SaveChangesAsync();

            return Ok(game);       
        }

        // DELETE api/games/5
        [HttpDelete("{game_id}")]
        public void Delete(int game_id)
        {
        }
    }            
}