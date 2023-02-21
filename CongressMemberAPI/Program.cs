using Microsoft.EntityFrameworkCore;
using Common.Brokers;
using Common.Contexts;
using CongressMemberAPI.Services;

namespace CongressMemberAPI
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);
            builder.Services.AddDbContext<CongressMemberSqlDbContext>(options =>
                options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

            // Add builder.Services to the container.
            AddBrokers(builder.Services);
            AddServices(builder.Services);
            builder.Services.AddControllers();

            // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen();

            var app = builder.Build();

            // Configure the HTTP request pipeline.
            if (builder.Environment.IsDevelopment())
            {
                app.UseSwagger();
                app.UseSwaggerUI();
            }

            app.UseAuthorization();
            app.MapControllers();
            app.Run();
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