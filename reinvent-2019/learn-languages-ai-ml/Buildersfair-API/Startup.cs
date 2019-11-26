using Amazon.S3;
using Amazon.Rekognition;
using Amazon.Textract;
using Amazon.Polly;
using Amazon.TranscribeService;
using BuildersFair_API.Data;
using BuildersFair_API.Models;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using BuildersFair_API.Utils;

namespace BuildersFair_API
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            string connectionString = Helpers.GetRDSConnectionString(this.Configuration);
            services.AddDbContext<DataContext>(x => x.UseMySql(connectionString));

            RedisUtil.REDIS_SERVERNAME = Helpers.GetRedisHostname(this.Configuration);

            services.AddDefaultAWSOptions(this.Configuration.GetAWSOptions());
            services.AddAWSService<IAmazonS3>();
            services.AddAWSService<IAmazonRekognition>();
            services.AddAWSService<IAmazonTextract>();
            services.AddAWSService<IAmazonPolly>();
            services.AddAWSService<IAmazonTranscribeService>();

            services.AddMvc().SetCompatibilityVersion(CompatibilityVersion.Version_2_1);
            services.AddCors();
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            else
            {
                //app.UseHsts();
            }

           //app.UseHttpsRedirection();
           app.UseCors(x => x.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader());
           app.UseMvc();
        }
    }
}
