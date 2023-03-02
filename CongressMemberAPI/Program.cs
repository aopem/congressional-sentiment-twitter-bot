using Azure.Identity;
using Common.Brokers;
using Common.Brokers.Azure;
using Common.Contexts;
using Common.Services;
using CongressMemberAPI.Services;

namespace CongressMemberAPI
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            // create a logger for AzureBroker, then broker itself
            var loggerFactory = LoggerFactory.Create(builder =>
            {
                builder.SetMinimumLevel(LogLevel.Information);
                builder.AddConsole();
            });
            var logger = loggerFactory.CreateLogger<AzureBroker>();
            var azureBroker = new AzureBroker(logger, builder.Configuration);

            // authenticate to Azure depending on environment
            DefaultAzureCredential? credential = null;
            if (builder.Environment.IsDevelopment())
            {
                credential = azureBroker.GetDevelopmentCredential();
            }
            else
            {
                credential = azureBroker.GetProductionCredential();
            }

            // get secrets and add to configuration
            var keyVaultName = builder.Configuration.GetValue<string>("Azure:KeyVault:Name");
            builder.Configuration.AddAzureKeyVault(
                new Uri ($"https://{keyVaultName}.vault.azure.net"),
                credential);

            builder.Services.AddDbContext<CongressMemberSqlDbContext>();

            // Add builder.Services to the container.
            AddBrokers(builder.Services);
            AddServices(builder.Services);
            builder.Services.AddControllers();

            // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen();

            // make sure async suffix is not removed for routing
            builder.Services.AddMvc(options =>
            {
                options.SuppressAsyncSuffixInActionNames = false;
            });

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
            services.AddScoped<ICongressMemberDbBroker, CongressMemberDbBroker>();
        }

        private static void AddServices(IServiceCollection services)
        {
            services.AddScoped<ICongressMemberService, CongressMemberService>();
        }
    }
}