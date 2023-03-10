using Azure.Identity;
using Common.Brokers;
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

            // create a logger for main
            var loggerFactory = LoggerFactory.Create(builder =>
            {
                builder.SetMinimumLevel(LogLevel.Information);
                builder.AddConsole();
            });
            var logger = loggerFactory.CreateLogger<Program>();

            // get Azure credential
            logger.LogInformation("Retrieving Azure credential...");
            var credential = new DefaultAzureCredential();

            // get secrets and add to configuration
            var keyVaultName = builder.Configuration.GetValue<string>("Azure:KeyVault:Name");
            logger.LogInformation($"Attempting to connect to Key Vault: {keyVaultName}");
            builder.Configuration.AddAzureKeyVault(
                new Uri ($"https://{keyVaultName}.vault.azure.net"),
                credential);
            logger.LogInformation("Successfully authenticated to Azure and retrieved secrets");

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

            // set URL endpoint
            builder.WebHost.ConfigureKestrel(serverOptions =>
            {
                serverOptions.ListenAnyIP(builder.Configuration.GetValue<int>("CongressMemberApi:Port"));
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