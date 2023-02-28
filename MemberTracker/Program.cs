using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Configuration;
using MemberTracker.Clients;
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
            Console.WriteLine($"keyvaultname: {keyVaultName}");
            while (true) {}
            // builder.Configuration.AddAzureKeyVault(
            //     new Uri ($"https://{keyVaultName}.vault.azure.net"),
            //     azureBroker.GetCredential());

            // // call API and get congressional data
            // var proPublicaClient = new ProPublicaClient(builder.Configuration);
            // var houseMembers = await proPublicaClient.GetHouseMembersAsync();
            // var senateMembers = await proPublicaClient.GetSenateMembersAsync();

            // // join lists to add to database, then update
            // var congressMemberClient = new CongressMemberClient(builder.Configuration);
            // var congressMembers = houseMembers.Concat<CongressMember>(senateMembers);

            // // add all members to database
            // foreach (var member in congressMembers)
            // {
            //     try
            //     {
            //         await congressMemberClient.CreateOrUpdateMember(member);
            //     }
            //     catch (Exception e)
            //     {
            //         // handle exceptions when member already exists
            //         Console.WriteLine(e.ToString());
            //     }
            // }

            // Console.WriteLine("Task Complete. All Congress Member info updated");
        }
    }
}