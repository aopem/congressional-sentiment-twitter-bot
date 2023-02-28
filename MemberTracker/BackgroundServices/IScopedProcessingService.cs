namespace MemberTracker.BackgroundServices
{
    public interface IScopedProcessingService
    {
        public ValueTask DoWork(CancellationToken cancellationToken);
    }
}