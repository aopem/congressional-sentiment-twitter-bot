using Microsoft.EntityFrameworkCore;
using Common.Models;

namespace Common.Contexts
{
    public interface ICongressMemberDbContext
    {
        public DbSet<CongressMember> CongressMembers { get; set; }
    }
}