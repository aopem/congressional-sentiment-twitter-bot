using Common.Clients;

namespace MemberTracker.Clients
{
    public class CongressMemberClient : HttpApiClient
    {
        public CongressMemberClient()
        {
            this._client.BaseAddress = new Uri("");
        }
    }
}