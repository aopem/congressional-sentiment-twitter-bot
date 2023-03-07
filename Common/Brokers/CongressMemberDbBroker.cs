using Microsoft.Extensions.Configuration;
using Microsoft.EntityFrameworkCore;
using Common.Contexts;
using Common.Models;

namespace Common.Brokers
{
    public class CongressMemberDbBroker : ICongressMemberDbBroker
    {
        private readonly IConfiguration _configuration;

        public CongressMemberDbBroker(IConfiguration configuration)
        {
            _configuration = configuration;
        }

        public async ValueTask<CongressMember?> InsertAsync(CongressMember congressMember)
        {
            var dbContext = CreateCongressMemberSqlDbContext();
            var entry = await dbContext.CongressMembers.AddAsync(congressMember);

            await dbContext.SaveChangesAsync();
            return entry.Entity;
        }

        public async ValueTask<CongressMember?> UpdateAsync(CongressMember congressMember)
        {
            var dbContext = CreateCongressMemberSqlDbContext();
            var entry = dbContext.CongressMembers.Update(congressMember);

            await dbContext.SaveChangesAsync();
            return entry.Entity;
        }

        public async ValueTask<CongressMember?> SelectByIdAsync(string id)
        {
            var dbContext = CreateCongressMemberSqlDbContext();
            return await dbContext.CongressMembers.FindAsync(id);
        }

        public IQueryable<CongressMember> SelectAll()
        {
            var dbContext = CreateCongressMemberSqlDbContext();
            return dbContext.CongressMembers.AsQueryable();
        }

        public async ValueTask<CongressMember?> DeleteByIdAsync(string id)
        {
            var congressMember = await SelectByIdAsync(id);
            if (congressMember is null)
            {
                throw new Exception();
            }

            var dbContext = CreateCongressMemberSqlDbContext();
            var entry = dbContext.CongressMembers.Remove(congressMember);

            await dbContext.SaveChangesAsync();
            return entry.Entity;
        }

        private CongressMemberSqlDbContext CreateCongressMemberSqlDbContext()
        {
            return new CongressMemberSqlDbContext(
                new DbContextOptionsBuilder<CongressMemberSqlDbContext>().Options,
                _configuration
            );
        }
    }
}