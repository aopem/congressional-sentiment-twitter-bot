using Common.Models;

namespace Common.Services
{
    public interface ICongressMemberService
    {
        ValueTask<CongressMember?> CreateOrUpdateCongressMemberAsync(CongressMember congressMember);
        ValueTask<CongressMember?> RetrieveCongressMemberAsync(string id);
        ValueTask<IEnumerable<CongressMember>> RetrieveAllCongressMembersAsync();
        ValueTask<CongressMember?> DeleteCongressMemberAsync(string id);
    }
}