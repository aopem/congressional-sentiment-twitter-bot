using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Common.Brokers.Azure;
using Common.Services;
using MemberTracker.Brokers;
using MemberTracker.Services;

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

            Console.WriteLine("Task Complete. All Congress Member info updated");
        }

        private static void AddBrokers(IServiceCollection services)
        {
            services.AddScoped<ICongressMemberApiBroker>();
            services.AddScoped<IProPublicaApiBroker>();
        }

        private static void AddServices(IServiceCollection services)
        {
            services.AddScoped<ICongressMemberService>();
            services.AddScoped<IProPublicaService>();
        }
    }
}