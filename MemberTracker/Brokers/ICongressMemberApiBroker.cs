using Common.Models;

namespace MemberTracker.Brokers
{
    public interface ICongressMemberApiBroker
    {
        ValueTask<CongressMember?> CreateOrUpdateAsync(CongressMember congressMember);
        ValueTask<CongressMember?> GetByIdAsync(string id);
        ValueTask<IEnumerable<CongressMember>> GetAllAsync();
        ValueTask<CongressMember?> DeleteByIdAsync(string id);
    }
}