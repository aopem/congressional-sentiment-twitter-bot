using Common.Models;

namespace MemberTracker.Brokers
{
    public interface IProPublicaApiBroker
    {
        ValueTask<IEnumerable<CongressMember>> GetAllHouseMembersAsync();
        ValueTask<IEnumerable<CongressMember>> GetAllSenateMembersAsync();
    }
}