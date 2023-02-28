using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.DependencyInjection;

namespace MemberTracker.BackgroundServices
{
    public class MemberTrackerTask : BackgroundService
    {
        private readonly ILogger<MemberTrackerTask> _logger;
        private readonly IServiceProvider _serviceProvider;

        public MemberTrackerTask(
            ILogger<MemberTrackerTask> logger,
            IServiceProvider serviceProvider)
        {
            _logger = logger;
            _serviceProvider = serviceProvider;
        }

        protected override async Task ExecuteAsync(CancellationToken cancellationToken)
        {
            var message = "Beginning background service execution...";
            _logger.LogInformation(message);

            await DoWork(cancellationToken);
        }

        private async Task DoWork(CancellationToken cancellationToken)
        {
            var message = "Executing scoped processing service...";
            _logger.LogInformation(message);

            using (var scope = _serviceProvider.CreateScope())
            {
                var scopedProcessingService = scope
                    .ServiceProvider
                    .GetRequiredService<IScopedProcessingService>();

                await scopedProcessingService.DoWork(cancellationToken);
            }
        }
    }
}