using Common.Models;

namespace MemberTracker.Services
{
    public interface IProPublicaService
    {
        ValueTask<IEnumerable<CongressMember>> RetrieveAllHouseMembersAsync();
        ValueTask<IEnumerable<CongressMember>> RetrieveAllSenateMembersAsync();
    }
}