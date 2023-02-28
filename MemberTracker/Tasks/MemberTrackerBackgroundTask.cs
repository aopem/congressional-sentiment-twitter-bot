using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Configuration;
using Common.Models;
using MemberTracker.Services;

namespace MemberTracker.Tasks
{
    public class MemberTrackerTask : BackgroundService
    {
        private readonly ILogger<MemberTrackerTask> _logger;
        private readonly IConfiguration _configuration;
        private readonly CongressMemberApiService _congressMemberApiService;
        private readonly ProPublicaApiService _proPublicaApiService;

        public MemberTrackerTask(
            ILogger<MemberTrackerTask> logger,
            IConfiguration configuration,
            CongressMemberApiService congressMemberApiService,
            ProPublicaApiService proPublicaApiService)
        {
            _logger = logger;
            _configuration = configuration;
            _congressMemberApiService = congressMemberApiService;
            _proPublicaApiService = proPublicaApiService;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            // call API and get congressional data
            var houseMembers = await _proPublicaApiService.RetrieveAllHouseMembersAsync();
            var senateMembers = await _proPublicaApiService.RetrieveAllSenateMembersAsync();

            // join lists to add to database, then update
            var congressMembers = houseMembers.Concat<CongressMember>(senateMembers);

            // add all members to database
            foreach (var member in congressMembers)
            {
                try
                {
                    await _congressMemberApiService.CreateOrUpdateCongressMemberAsync(member);
                }
                catch (Exception e)
                {
                    // handle exceptions when member already exists
                    _logger.LogError(e.ToString());
                }
            }
        }
    }
}