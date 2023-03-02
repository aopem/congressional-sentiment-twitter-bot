using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Hosting;
using Azure.Identity;
using Common.Brokers.Azure;
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