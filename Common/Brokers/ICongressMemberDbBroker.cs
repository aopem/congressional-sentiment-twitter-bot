using Common.Models;

namespace Common.Brokers
{
    public interface ICongressMemberDbBroker
    {
        ValueTask<CongressMember?> InsertAsync(CongressMember congressMember);
        ValueTask<CongressMember?> UpdateAsync(CongressMember congressMember);
        ValueTask<CongressMember?> SelectByIdAsync(string id);
        IQueryable<CongressMember> SelectAll();
        ValueTask<CongressMember?> DeleteByIdAsync(string id);
    }
}