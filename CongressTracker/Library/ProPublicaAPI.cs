using System.ComponentModel;
using Common.Models;
using Common.Enums;
using CongressTracker.ResponseTypes;

namespace CongressTracker.Library
{
    public class ProPublicaAPI
    {
        private readonly HttpClient _client;
        private readonly int congress = 117;

        public ProPublicaAPI(string apiKey)
        {
            this._client = new HttpClient();
            this._client.DefaultRequestHeaders.Add("X-API-Key", apiKey);
            this._client.BaseAddress = new Uri($"https://api.propublica.org/congress/v1/{congress}/");
        }

        public async Task<List<CongressMember>> GetHouseMembersAsync()
        {
            var path = "house/members.json";
            HttpResponseMessage response = await this._client.GetAsync(path);

            ProPublicaResponse responseContent = new ProPublicaResponse();
            if (response.IsSuccessStatusCode)
            {
                responseContent = await response.Content.ReadAsAsync<ProPublicaResponse>();
            }

            return this.DeserializeProPublicaResponse(responseContent, Chamber.House);
        }

        public async Task<List<CongressMember>> GetSenateMembersAsync()
        {
            var path = "senate/members.json";
            HttpResponseMessage response = await this._client.GetAsync(path);

            var responseContent = new ProPublicaResponse();
            if (response.IsSuccessStatusCode)
            {
                responseContent = await response.Content.ReadAsAsync<ProPublicaResponse>();
            }

            return this.DeserializeProPublicaResponse(responseContent, Chamber.Senate);
        }

        private List<CongressMember> DeserializeProPublicaResponse(ProPublicaResponse response, Chamber chamber)
        {
            var congressMembers = new List<CongressMember>();
            foreach (var member in response.Results[0].Members)
            {
                var deserializedMember = new CongressMember(
                    firstName: member.FirstName,
                    lastName: member.LastName,
                    gender: member.Gender,
                    party: member.Party,
                    state: member.State,
                    twitterAccountName: member.TwitterAccount,
                    chamber: chamber
                );

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