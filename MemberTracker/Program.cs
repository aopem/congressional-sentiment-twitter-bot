using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
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

            // get secrets and add to configuration
            var keyVaultName = builder.Configuration.GetValue<string>("Azure:KeyVault:Name");
            var azureBroker = new AzureBroker(builder.Configuration);
            builder.Configuration.AddAzureKeyVault(
                new Uri ($"https://{keyVaultName}.vault.azure.net"),
                azureBroker.GetCredential());

            // dependency injection
            AddBrokers(builder.Services);
            AddServices(builder.Services);
            builder.Services.AddHostedService<ScheduledMemberTrackerTask>();
            builder.Services.AddScoped<IScopedProcessingService, MemberTrackerProcessingService>();

            var app = builder.Build();
            app.Run();
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