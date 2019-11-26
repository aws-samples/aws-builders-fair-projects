using System.Configuration;
using Microsoft.Extensions.Configuration;

namespace BuildersFair_API.Models
{
    public class Helpers
    {
        public static string GetRDSConnectionString(IConfiguration configuration)
        {
            string dbname = configuration.GetConnectionString("RDS_DB_NAME");

            if (string.IsNullOrEmpty(dbname)) return null;

            string username = configuration.GetConnectionString("RDS_USERNAME");
            string password = configuration.GetConnectionString("RDS_PASSWORD");
            string hostname = configuration.GetConnectionString("RDS_HOSTNAME");
            string port = configuration.GetConnectionString("RDS_PORT");

            return "Data Source=" + hostname + ";Initial Catalog=" + dbname + ";User ID=" + username + ";Password=" + password + ";";
        }

        public static string GetRedisHostname(IConfiguration configuration)
        {
            string hostname = configuration.GetSection("ElastiCache").GetValue("REDIS_HOST_NAME", "localhost");

            return hostname;
        }
    }
}