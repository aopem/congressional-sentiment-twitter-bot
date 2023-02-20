using Microsoft.EntityFrameworkCore;
using Common.Brokers;
using Common.Contexts;
using CongressMemberAPI.Services;

namespace CongressMemberAPI
{
    public class Startup
    {
        public IConfiguration Configuration { get; }

        public Startup(IConfiguration configuration)
        {
            this.Configuration = configuration;
        }

        public static void Configure(IApplicationBuilder app, IWebHostEnvironment environment)
        {
            // Configure the HTTP request pipeline.
            if (environment.IsDevelopment())
            {
                app.UseSwagger();
                app.UseSwaggerUI();
            }

            app.UseAuthorization();
        }

        public void ConfigureServices(IServiceCollection services)
        {
            services.AddDbContext<CongressMemberSqlDbContext>(options =>
                options.UseSqlServer(Configuration.GetConnectionString("DefaultConnection")));

            // Add services to the container.
            AddBrokers(services);
            AddServices(services);

            services.AddControllers();
            // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
            services.AddEndpointsApiExplorer();
            services.AddSwaggerGen();
        }

        private static void AddBrokers(IServiceCollection services)
        {
            services.AddScoped<CongressMemberDbBroker>();
        }

        private static void AddServices(IServiceCollection services)
        {
            services.AddScoped<CongressMemberService>();
        }
    }
}
