using Common.Contexts;
using Common.Models;

namespace Common.Brokers
{
    public class CongressMemberDbBroker
    {
        private readonly CongressMemberSqlDbContext _congressMemberDbContext;

        public CongressMemberDbBroker(CongressMemberSqlDbContext congressMemberDbContext)
        {
            this._congressMemberDbContext = congressMemberDbContext;
        }

        public async ValueTask<CongressMember> InsertAsync(CongressMember congressMember)
        {
            var entry = await this._congressMemberDbContext.CongressMembers.AddAsync(congressMember);

            await this._congressMemberDbContext.SaveChangesAsync();
            return entry.Entity;
        }

        public async ValueTask<CongressMember> UpdateAsync(CongressMember congressMember)
        {
            var entry = this._congressMemberDbContext.CongressMembers.Update(congressMember);

            await this._congressMemberDbContext.SaveChangesAsync();
            return entry.Entity;
        }

        public async ValueTask<CongressMember?> SelectByIdAsync(int id)
        {
            return await this._congressMemberDbContext.CongressMembers.FindAsync(id);
        }

        public IQueryable<CongressMember> SelectAll()
        {
            return this._congressMemberDbContext.CongressMembers;
        }

        public async ValueTask<CongressMember> DeleteByIdAsync(int id)
        {
            var congressMember = await this.SelectByIdAsync(id);
            if (congressMember is null)
            {
                throw new Exception();
            }

            var entry = this._congressMemberDbContext.CongressMembers.Remove(congressMember);

            await this._congressMemberDbContext.SaveChangesAsync();
            return entry.Entity;
        }
    }
}