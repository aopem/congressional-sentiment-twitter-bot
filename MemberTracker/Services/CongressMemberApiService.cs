using Microsoft.Extensions.Logging;
using Common.Models;
using MemberTracker.Brokers;

namespace MemberTracker.Services
{
    public class CongressMemberApiService
    {
        private readonly ILogger<CongressMemberApiService> _logger;
        private readonly CongressMemberApiBroker _congressMemberApiBroker;

        public CongressMemberApiService(
            ILogger<CongressMemberApiService> logger,
            CongressMemberApiBroker congressMemberApiBroker)
        {
            _logger = logger;
            _congressMemberApiBroker = congressMemberApiBroker;
        }

        public async ValueTask<CongressMember?> CreateOrUpdateCongressMemberAsync(CongressMember congressMember)
        {
            return await _congressMemberApiBroker.CreateOrUpdateAsync(congressMember);
        }

        public async ValueTask<CongressMember?> RetrieveCongressMemberAsync(string id)
        {
            return await _congressMemberApiBroker.GetByIdAsync(id);
        }

        public async ValueTask<List<CongressMember>> RetrieveAllCongressMembersAsync()
        {
            return await _congressMemberApiBroker.GetAllAsync();
        }

        public async ValueTask<CongressMember?> DeleteCongressMemberAsync(string id)
        {
            return await _congressMemberApiBroker.DeleteById(id);
        }
    }
}