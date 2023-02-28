using Microsoft.EntityFrameworkCore;
using Common.Models;

namespace Common.Contexts
{
    public interface ICongressMemberDbContext
    {
        DbSet<CongressMember> CongressMembers { get; set; }
    }
}