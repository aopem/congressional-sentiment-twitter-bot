using CongressTracker.Library;

namespace CongressTracker
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var apiKey = "";
            var proPublicaClient = new ProPublicaAPI(apiKey);
            var houseMembers = await proPublicaClient.GetHouseMembersAsync();
            var senateMembers = await proPublicaClient.GetSenateMembersAsync();
        }
    }
}