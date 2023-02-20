using Common.Models;
using Common.Brokers;

namespace CongressMemberAPI.Services
{
    public class CongressMemberService
    {
        private readonly CongressMemberDbBroker _congressMemberDbBroker;

        public CongressMemberService(CongressMemberDbBroker congressMemberDbBroker)
        {
            this._congressMemberDbBroker = congressMemberDbBroker;
        }

        public async ValueTask<CongressMember> CreateCongressMemberAsync(CongressMember congressMember)
        {
            return await this._congressMemberDbBroker.InsertAsync(congressMember);
        }

        public async ValueTask<CongressMember?> RetrieveCongressMemberAsync(int id)
        {
            return await this._congressMemberDbBroker.SelectByIdAsync(id);
        }

        public IQueryable<CongressMember> RetrieveAllCongressMembers()
        {
            return this._congressMemberDbBroker.SelectAll();
        }

        public async ValueTask<CongressMember> UpdateCongressMemberAsync(CongressMember congressMember)
        {
            return await this._congressMemberDbBroker.UpdateAsync(congressMember);
        }

        public async ValueTask<CongressMember> DeleteCongressMemberAsync(int id)
        {
            return await this._congressMemberDbBroker.DeleteByIdAsync(id);
        }
    }
}