using Common.Clients;

namespace MemberTracker.Clients
{
    public class CongressMemberClient : HttpApiClient
    {
        public CongressMemberClient()
        {
            _httpClient.BaseAddress = new Uri("");
        }
    }
}