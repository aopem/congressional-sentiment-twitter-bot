using MemberTracker.Clients;
using Common.Utils;

namespace MemberTracker
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            // get secrets
            var secrets = new Config(Constants.SECRETS_FILEPATH);
            string apiKey = secrets.Properties.proPublicaApiKey;

            // call API and get congressional data
            var proPublicaClient = new ProPublicaClient(apiKey);
            var houseMembers = await proPublicaClient.GetHouseMembersAsync();
            var senateMembers = await proPublicaClient.GetSenateMembersAsync();
        }
    }
}