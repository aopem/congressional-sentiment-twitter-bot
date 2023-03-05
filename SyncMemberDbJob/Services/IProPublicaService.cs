using Common.Models;

namespace SyncMemberDbJob.Services
{
    public interface IProPublicaService
    {
        ValueTask<IEnumerable<CongressMember>> RetrieveAllHouseMembersAsync();
        ValueTask<IEnumerable<CongressMember>> RetrieveAllSenateMembersAsync();
    }
}