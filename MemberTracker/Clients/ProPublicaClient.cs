using Common.Models;
using Common.Enums;
using Common.Clients;
using MemberTracker.ResponseTypes;

namespace MemberTracker.Clients
{
    public class ProPublicaClient : HttpApiClient
    {
        private readonly int congress = 117;

        public ProPublicaClient(string apiKey)
        {
            this._client.BaseAddress = new Uri($"https://api.propublica.org/congress/v1/{congress}/");
            this._client.DefaultRequestHeaders.Add("X-API-Key", apiKey);
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
            else
            {
                throw new Exception();
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
            else
            {
                throw new Exception();
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