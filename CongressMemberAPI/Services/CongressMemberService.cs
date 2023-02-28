using Microsoft.EntityFrameworkCore;
using Common.Models;
using Common.Brokers;
using Common.Services;

namespace CongressMemberAPI.Services
{
    public class CongressMemberService : ICongressMemberService
    {
        private readonly ICongressMemberDbBroker _congressMemberDbBroker;

        public CongressMemberService(ICongressMemberDbBroker congressMemberDbBroker)
        {
            _congressMemberDbBroker = congressMemberDbBroker;
        }

        public async ValueTask<CongressMember?> CreateOrUpdateCongressMemberAsync(CongressMember congressMember)
        {
            var existingCongressMember = await RetrieveCongressMemberAsync(congressMember.ID);
            if (existingCongressMember is not null)
            {
                return await _congressMemberDbBroker.UpdateAsync(congressMember);
            }

            return await _congressMemberDbBroker.InsertAsync(congressMember);
        }

        public async ValueTask<CongressMember?> RetrieveCongressMemberAsync(string id)
        {
            return await _congressMemberDbBroker.SelectByIdAsync(id);
        }

        public async ValueTask<IEnumerable<CongressMember>> RetrieveAllCongressMembersAsync()
        {
            return await _congressMemberDbBroker.SelectAll().ToListAsync<CongressMember>();
        }

        public async ValueTask<CongressMember?> DeleteCongressMemberAsync(string id)
        {
            return await _congressMemberDbBroker.DeleteByIdAsync(id);
        }
    }
}