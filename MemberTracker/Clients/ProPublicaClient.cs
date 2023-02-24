using Microsoft.Extensions.Configuration;
using Common.Models;
using Common.Enums;
using Common.Clients;
using MemberTracker.ResponseTypes;

namespace MemberTracker.Clients
{
    public class ProPublicaClient : HttpApiClient
    {
        private readonly int congress = 117;

        public ProPublicaClient(IConfiguration configuration)
        {
            _httpClient.BaseAddress = new Uri($"https://api.propublica.org/congress/v1/{congress}/");
            _httpClient.DefaultRequestHeaders.Add("X-API-Key", configuration.GetValue<string>("ProPublicaApiKey"));
        }

        public async Task<List<CongressMember>> GetHouseMembersAsync()
        {
            Console.WriteLine("Retrieving all current House member information...");

            var path = "house/members.json";
            HttpResponseMessage response = await _httpClient.GetAsync(path);

            ProPublicaResponse responseContent = new ProPublicaResponse();
            if (response.IsSuccessStatusCode)
            {
                responseContent = await response.Content.ReadAsAsync<ProPublicaResponse>();
            }
            else
            {
                throw new Exception();
            }

            return DeserializeProPublicaResponse(responseContent, Chamber.House);
        }

        public async Task<List<CongressMember>> GetSenateMembersAsync()
        {
            Console.WriteLine("Retrieving all current Senate member information...");

            var path = "senate/members.json";
            HttpResponseMessage response = await _httpClient.GetAsync(path);

            var responseContent = new ProPublicaResponse();
            if (response.IsSuccessStatusCode)
            {
                responseContent = await response.Content.ReadAsAsync<ProPublicaResponse>();
            }
            else
            {
                throw new Exception();
            }

            return DeserializeProPublicaResponse(responseContent, Chamber.Senate);
        }

        private List<CongressMember> DeserializeProPublicaResponse(ProPublicaResponse response, Chamber chamber)
        {
            var congressMembers = new List<CongressMember>();
            foreach (var member in response.Results[0].Members)
            {
                var deserializedMember = new CongressMember
                {
                    ID = member.Id,
                    FirstName = member.FirstName,
                    LastName = member.LastName,
                    Gender = member.Gender,
                    Party = member.Party,
                    State = member.State,
                    TwitterAccountName = member.TwitterAccount,
                    Chamber = chamber
                };

                if (member.MiddleName is not null)
                {
                    deserializedMember.MiddleName = member.MiddleName.ToString();
                }

                congressMembers.Add(deserializedMember);
            }

            return congressMembers;
        }
    }
}