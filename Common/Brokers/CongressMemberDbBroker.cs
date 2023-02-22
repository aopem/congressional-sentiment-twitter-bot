using Microsoft.Extensions.Configuration;
using Microsoft.EntityFrameworkCore;
using Common.Contexts;
using Common.Models;

namespace Common.Brokers
{
    public class CongressMemberDbBroker
    {
        private readonly IConfiguration _configuration;

        public CongressMemberDbBroker(
            IConfiguration configuration)
        {
            this._configuration = configuration;
        }

        public async ValueTask<CongressMember> InsertAsync(CongressMember congressMember)
        {
            var dbContext = CreateCongressMemberSqlDbContext();
            var entry = await dbContext.CongressMembers.AddAsync(congressMember);

            await dbContext.SaveChangesAsync();
            return entry.Entity;
        }

        public async ValueTask<CongressMember> UpdateAsync(CongressMember congressMember)
        {
            var dbContext = CreateCongressMemberSqlDbContext();
            var entry = dbContext.CongressMembers.Update(congressMember);

            await dbContext.SaveChangesAsync();
            return entry.Entity;
        }

        public async ValueTask<CongressMember?> SelectByIdAsync(int id)
        {
            var dbContext = CreateCongressMemberSqlDbContext();
            return await dbContext.CongressMembers.FindAsync(id);
        }

        public IQueryable<CongressMember> SelectAll()
        {
            var dbContext = CreateCongressMemberSqlDbContext();
            return dbContext.CongressMembers;
        }

        public async ValueTask<CongressMember> DeleteByIdAsync(int id)
        {
            var congressMember = await this.SelectByIdAsync(id);
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
                new DbContextOptionsBuilder<CongressMemberSqlDbContext>()
                    .UseSqlServer(this._configuration.GetConnectionString("CongressMemberDb"))
                    .Options,
                this._configuration
            );
        }
    }
}