using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.DependencyInjection;

namespace MemberTracker.BackgroundServices
{
    public class ScheduledMemberTrackerTask : IHostedService, IDisposable
    {
        private readonly ILogger<ScheduledMemberTrackerTask> _logger;
        private readonly IServiceProvider _serviceProvider;
        private Timer? _timer;
        private readonly int _daysBetweenExecution = 15;

        public ScheduledMemberTrackerTask(
            ILogger<ScheduledMemberTrackerTask> logger,
            IServiceProvider serviceProvider)
        {
            _logger = logger;
            _serviceProvider = serviceProvider;
        }

        public Task StartAsync(CancellationToken cancellationToken)
        {
            var message = "Starting scheduled MemberTracker task...";
            _logger.LogInformation(message);

            _timer = new Timer(async _ => await DoWork(cancellationToken),
                null,
                GetMsBetweenExecutions(),
                Timeout.Infinite);

            return Task.CompletedTask;
        }

        public Task StopAsync(CancellationToken cancellationToken)
        {
            var message = "Stopping scheduled MemberTracker task...";
            _logger.LogInformation(message);

            // clean up
            Dispose();
            return Task.CompletedTask;
        }

        public void Dispose()
        {
            _timer?.Dispose();
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

        private int GetMsBetweenExecutions()
        {
            var msBetweenExecutions = (int)(DateTime.Now.AddMinutes(3) - DateTime.Now).TotalMilliseconds;
            _logger.LogInformation($"Time until next execution: {msBetweenExecutions} ms");
            return msBetweenExecutions;
        }
    }
}