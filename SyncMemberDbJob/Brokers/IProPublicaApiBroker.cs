using Common.Models;

namespace SyncMemberDbJob.Brokers
{
    public interface IProPublicaApiBroker
    {
        ValueTask<IEnumerable<CongressMember>> GetAllHouseMembersAsync();
        ValueTask<IEnumerable<CongressMember>> GetAllSenateMembersAsync();
    }
}