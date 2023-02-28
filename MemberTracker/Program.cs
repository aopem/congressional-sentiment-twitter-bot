using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using MemberTracker.Brokers;
using Common.Brokers.Azure;
using Common.Models;

namespace MemberTracker
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            // get secrets and add to configuration
            var keyVaultName = builder.Configuration.GetValue<string>("Azure:KeyVault:Name");
            var azureBroker = new AzureBroker(builder.Configuration);
            builder.Configuration.AddAzureKeyVault(
                new Uri ($"https://{keyVaultName}.vault.azure.net"),
                azureBroker.GetCredential());



            Console.WriteLine("Task Complete. All Congress Member info updated");
        }

        private static void AddBrokers(IServiceCollection services)
        {
            services.AddScoped<CongressMemberApiBroker>();
            services.AddScoped<ProPublicaApiBroker>();
        }

        private static void AddServices(IServiceCollection services)
        {
        }
    }
}