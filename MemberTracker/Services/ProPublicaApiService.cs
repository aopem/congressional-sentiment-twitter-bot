using Microsoft.Extensions.Logging;
using Common.Models;
using MemberTracker.Brokers;

namespace MemberTracker.Services
{
    public class ProPublicaApiService : IProPublicaService
    {
        private readonly ILogger<ProPublicaApiService> _logger;
        private readonly IProPublicaApiBroker _proPublicaApiBroker;

        public ProPublicaApiService(
            ILogger<ProPublicaApiService> logger,
            IProPublicaApiBroker proPublicaApiBroker)
        {
            _logger = logger;
            _proPublicaApiBroker = proPublicaApiBroker;
        }

        public async ValueTask<IEnumerable<CongressMember>> RetrieveAllHouseMembersAsync()
        {
            return await _proPublicaApiBroker.GetAllHouseMembersAsync();
        }

        public async ValueTask<IEnumerable<CongressMember>> RetrieveAllSenateMembersAsync()
        {
            return await _proPublicaApiBroker.GetAllSenateMembersAsync();
        }
    }
}