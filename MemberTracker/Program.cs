using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Configuration;
using MemberTracker.Clients;
using Common.Brokers.Azure;

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

            // call API and get congressional data
            var proPublicaClient = new ProPublicaClient(builder.Configuration.GetValue<string>("ProPublicaApiKey"));
            var houseMembers = await proPublicaClient.GetHouseMembersAsync();
            var senateMembers = await proPublicaClient.GetSenateMembersAsync();

            Console.WriteLine("Task Complete. All Congress Member info updated");
        }
    }
}