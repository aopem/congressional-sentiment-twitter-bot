using MemberTracker.Clients;
using Common.Utils;
using Common.Config;

namespace MemberTracker
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var secrets = new Config(Constants.SECRETS_FILEPATH);
            var proPublicaClient = new ProPublicaClient(secrets.Properties["proPublicaApiKey"]);
            var houseMembers = await proPublicaClient.GetHouseMembersAsync();
            var senateMembers = await proPublicaClient.GetSenateMembersAsync();
        }
    }
}