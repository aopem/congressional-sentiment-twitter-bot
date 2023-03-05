using Common.Models;
using Common.Services;
using SyncMemberDbJob.Brokers;

namespace SyncMemberDbJob.Services
{
    public class CongressMemberApiService : ICongressMemberService
    {
        private readonly ILogger<CongressMemberApiService> _logger;
        private readonly ICongressMemberApiBroker _congressMemberApiBroker;

        public CongressMemberApiService(
            ILogger<CongressMemberApiService> logger,
            ICongressMemberApiBroker congressMemberApiBroker)
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

        public async ValueTask<IEnumerable<CongressMember>> RetrieveAllCongressMembersAsync()
        {
            return await _congressMemberApiBroker.GetAllAsync();
        }

        public async ValueTask<CongressMember?> DeleteCongressMemberAsync(string id)
        {
            return await _congressMemberApiBroker.DeleteByIdAsync(id);
        }
    }
}