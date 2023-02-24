using Microsoft.Extensions.Configuration;
using Common.Clients;
using Common.Models;

namespace MemberTracker.Clients
{
    public class CongressMemberClient : HttpApiClient
    {
        public CongressMemberClient(IConfiguration configuration)
        {
            _httpClient.BaseAddress = new Uri($"http://localhost:{configuration.GetValue<string>("CongressMemberApi:Port")}/api/");
        }

        public async ValueTask CreateOrUpdateMember(CongressMember congressMember)
        {
            var path = "CongressMember";
            var response = await _httpClient.PostAsJsonAsync<CongressMember>(path, congressMember);

            if (!response.IsSuccessStatusCode)
            {
                throw new Exception(await response.Content.ReadAsStringAsync());
            }
        }
    }
}