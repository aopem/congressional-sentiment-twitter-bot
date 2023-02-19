using Microsoft.EntityFrameworkCore;
using Common.Models;

namespace Common.Contexts
{
    public class CongressMemberSqlDbContext : DbContext, ICongressMemberDbContext
    {
        public CongressMemberSqlDbContext(DbContextOptions<CongressMemberSqlDbContext> options) : base(options)
        {
        }

        public DbSet<CongressMember> CongressMembers { get; set; } = null!;
    }
}