using CongressMemberTrackingService.Models;
using Common.Brokers;

namespace CongressMemberTrackingService.Services
{
    public class CongressMemberService
    {
        private readonly DatabaseBroker _databaseBroker;

        public CongressMemberService(DatabaseBroker databaseBroker)
        {
            this._databaseBroker = databaseBroker;
        }

        public async ValueTask<CongressMember> CreateCongressMemberAsync(CongressMember congressMember)
        {
            return await this._databaseBroker.InsertAsync<CongressMember>(congressMember);
        }

        public async ValueTask<CongressMember> RetrieveCongressMemberAsync(Guid id)
        {
            return await this._databaseBroker.SelectByIdAsync<CongressMember>(id);
        }

        public IQueryable<CongressMember> RetrieveAllCongressMembersAsync()
        {
            return this._databaseBroker.SelectAllAsync<CongressMember>();
        }

        public async ValueTask<CongressMember> UpdateCongressMemberAsync(CongressMember congressMember)
        {
            return await this._databaseBroker.UpdateAsync<CongressMember>(congressMember);
        }

        public async ValueTask<CongressMember> DeleteCongressMemberAsync(Guid id)
        {
            return await this._databaseBroker.DeleteByIdAsync<CongressMember>(id);
        }
    }
}