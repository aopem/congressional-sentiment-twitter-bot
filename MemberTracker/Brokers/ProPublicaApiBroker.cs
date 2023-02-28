using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Common.Models;
using Common.Enums;
using Common.Clients;
using MemberTracker.ResponseTypes;

namespace MemberTracker.Brokers
{
    public class ProPublicaApiBroker : HttpApiClient, IProPublicaApiBroker
    {
        private readonly ILogger<ProPublicaApiBroker> _logger;
        private readonly IConfiguration _configuration;
        private readonly int congress = 117;

        public ProPublicaApiBroker(
            ILogger<ProPublicaApiBroker> logger,
            IConfiguration configuration)
        {
            _logger = logger;
            _configuration = configuration;
            _httpClient.BaseAddress = new Uri($"https://api.propublica.org/congress/v1/{congress}/");
            _httpClient.DefaultRequestHeaders.Add("X-API-Key", configuration.GetValue<string>("ProPublicaApiKey"));
        }

        public async ValueTask<IEnumerable<CongressMember>> GetAllHouseMembersAsync()
        {
            _logger.LogInformation("Retrieving all current House member information...");

            var path = "house/members.json";
            HttpResponseMessage response = await _httpClient.GetAsync(path);

            // handle any errors
            ProPublicaResponse responseContent = new ProPublicaResponse();
            if (!response.IsSuccessStatusCode)
            {
                var error = await response.Content.ReadAsStringAsync();
                _logger.LogError(error);
                return Enumerable.Empty<CongressMember>();
            }

            // deserialize list and return
            responseContent = await response.Content.ReadAsAsync<ProPublicaResponse>();
            return DeserializeProPublicaResponse(responseContent, Chamber.House);
        }

        public async ValueTask<IEnumerable<CongressMember>> GetAllSenateMembersAsync()
        {
            _logger.LogInformation("Retrieving all current Senate member information...");

            var path = "senate/members.json";
            HttpResponseMessage response = await _httpClient.GetAsync(path);

            // handle any errors
            var responseContent = new ProPublicaResponse();
            if (!response.IsSuccessStatusCode)
            {
                var error = await response.Content.ReadAsStringAsync();
                _logger.LogError(error);
                return Enumerable.Empty<CongressMember>();
            }

            // deserialize list and return
            responseContent = await response.Content.ReadAsAsync<ProPublicaResponse>();
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