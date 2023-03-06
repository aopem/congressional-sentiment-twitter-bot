using Newtonsoft.Json;
using Common.Services;
using Common.Models;
using SyncMemberDbJob.Services;

namespace SyncMemberDbJob.BackgroundServices
{
    public class SyncMemberDbBackgroundService : BackgroundService
    {
        private readonly ILogger<SyncMemberDbBackgroundService> _logger;
        private readonly IConfiguration _configuration;
        private readonly ICongressMemberService _congressMemberApiService;
        private readonly IProPublicaService _proPublicaApiService;

        public SyncMemberDbBackgroundService(
            ILogger<SyncMemberDbBackgroundService> logger,
            IConfiguration configuration,
            ICongressMemberService congressMemberApiService,
            IProPublicaService proPublicaApiService)
        {
            _logger = logger;
            _configuration = configuration;
            _congressMemberApiService = congressMemberApiService;
            _proPublicaApiService = proPublicaApiService;
        }

        protected override async Task ExecuteAsync(CancellationToken cancellationToken)
        {
            _logger.LogInformation("Retrieving all congress members...");
            var congressMembers = await GetAllCongressMembers();

            _logger.LogInformation("Updating congress member database...");
            await UpdateCongressMemberDatabase(cancellationToken, congressMembers);

            _logger.LogInformation("SyncMemberDbBackgroundService execution complete");
        }

        private async ValueTask UpdateCongressMemberDatabase(
            CancellationToken cancellationToken,
            IEnumerable<CongressMember> congressMembers)
        {
            // add all members to database using API
            foreach (var member in congressMembers)
            {
                // if task is cancelled stop processing Congress members
                if (cancellationToken.IsCancellationRequested)
                {
                    return;
                }

                try
                {
                    var addedMember = await _congressMemberApiService.CreateOrUpdateCongressMemberAsync(member);
                    _logger.LogInformation($"Successfully created or updated: {JsonConvert.SerializeObject(addedMember)}");
                }
                catch (Exception e)
                {
                    // handle exceptions when member already exists
                    _logger.LogError(e.ToString());
                }
            }
        }

        private async ValueTask<IEnumerable<CongressMember>> GetAllCongressMembers()
        {
            // call ProPublica API and get congressional data
            var houseMembers = await _proPublicaApiService.RetrieveAllHouseMembersAsync();
            var senateMembers = await _proPublicaApiService.RetrieveAllSenateMembersAsync();

            // join lists, then return
            return houseMembers.Concat<CongressMember>(senateMembers);
        }
    }
}