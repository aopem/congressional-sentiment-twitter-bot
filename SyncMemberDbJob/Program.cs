using Azure.Identity;
using Common.Services;
using SyncMemberDbJob.Brokers;
using SyncMemberDbJob.Services;
using SyncMemberDbJob.BackgroundServices;

namespace SyncMemberDbJob
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var builder = Host.CreateApplicationBuilder(args);

            // create a logger for AzureBroker, then broker itself
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

            // dependency injection
            AddBrokers(builder.Services);
            AddServices(builder.Services);
            builder.Services.AddHostedService<SyncMemberDbBackgroundService>();

            await builder.Build().RunAsync();
        }

        private static void AddBrokers(IServiceCollection services)
        {
            services.AddTransient<ICongressMemberApiBroker, CongressMemberApiBroker>();
            services.AddTransient<IProPublicaApiBroker, ProPublicaApiBroker>();
        }

        private static void AddServices(IServiceCollection services)
        {
            services.AddTransient<ICongressMemberService, CongressMemberApiService>();
            services.AddTransient<IProPublicaService, ProPublicaApiService>();
        }
    }
}