using Common.Brokers;
using Common.Brokers.Azure;
using Common.Contexts;
using CongressMemberAPI.Services;

namespace CongressMemberAPI
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            // get secrets and add to configuration
            var keyVaultName = builder.Configuration.GetValue<string>("Azure:KeyVault:Name");
            var azureBroker = new AzureBroker(builder.Configuration);
            builder.Configuration.AddAzureKeyVault(
                new Uri ($"https://{keyVaultName}.vault.azure.net"),
                azureBroker.GetCredential());

            builder.Services.AddDbContext<CongressMemberSqlDbContext>();

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