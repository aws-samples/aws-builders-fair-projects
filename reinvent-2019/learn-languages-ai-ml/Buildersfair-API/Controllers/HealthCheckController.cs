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
    public class HealthCheckController : ControllerBase
    {
        public HealthCheckController()
        {
        }

        // GET api/healthcheck
        [HttpGet]
        public ActionResult<string> Get()
        {
            return "I'm healthy.";
        }
    }            
}