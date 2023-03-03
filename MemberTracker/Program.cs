using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Azure.Identity;
using Common.Services;
using MemberTracker.Brokers;
using MemberTracker.Services;
using MemberTracker.BackgroundServices;

namespace MemberTracker
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
            var logger = loggerFactory.CreateLogger<Program>();

            // get Azure credential
            logger.LogInformation("Retrieving Azure credential...");
            var credential = new DefaultAzureCredential();

            // get secrets and add to configuration
            var keyVaultName = builder.Configuration.GetValue<string>("Azure:KeyVault:Name");
            builder.Configuration.AddAzureKeyVault(
                new Uri ($"https://{keyVaultName}.vault.azure.net"),
                credential);

            logger.LogInformation("Successfully authenticated to Azure and retrieved secrets");

            // dependency injection
            AddBrokers(builder.Services);
            AddServices(builder.Services);
            builder.Services.AddHostedService<ScheduledMemberTrackerTask>();
            builder.Services.AddScoped<IScopedProcessingService, MemberTrackerProcessingService>();

            builder.Build().Run();
        }

        private static void AddBrokers(IServiceCollection services)
        {
            services.AddScoped<ICongressMemberApiBroker, CongressMemberApiBroker>();
            services.AddScoped<IProPublicaApiBroker, ProPublicaApiBroker>();
        }

        private static void AddServices(IServiceCollection services)
        {
            services.AddScoped<ICongressMemberService, CongressMemberApiService>();
            services.AddScoped<IProPublicaService, ProPublicaApiService>();
        }
    }
}