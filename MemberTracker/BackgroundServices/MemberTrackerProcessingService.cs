using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json;
using Common.Services;
using Common.Models;
using MemberTracker.Services;

namespace MemberTracker.BackgroundServices
{
    public class MemberTrackerProcessingService : IScopedProcessingService
    {
        private readonly ILogger<MemberTrackerProcessingService> _logger;
        private readonly IConfiguration _configuration;
        private readonly ICongressMemberService _congressMemberApiService;
        private readonly IProPublicaService _proPublicaApiService;

        public MemberTrackerProcessingService(
            ILogger<MemberTrackerProcessingService> logger,
            IConfiguration configuration,
            ICongressMemberService congressMemberApiService,
            IProPublicaService proPublicaApiService)
        {
            _logger = logger;
            _configuration = configuration;
            _congressMemberApiService = congressMemberApiService;
            _proPublicaApiService = proPublicaApiService;
        }

        public async ValueTask DoWork(CancellationToken cancellationToken)
        {
            while (!cancellationToken.IsCancellationRequested)
            {
                _logger.LogInformation("Retrieving all congress members...");
                var congressMembers = await GetAllCongressMembers();

                _logger.LogInformation("Updating congress member database");
                await UpdateCongressMemberDatabase(congressMembers);
            }
        }

        private async ValueTask UpdateCongressMemberDatabase(IEnumerable<CongressMember> congressMembers)
        {
            // add all members to database using API
            foreach (var member in congressMembers)
            {
                try
                {
                    var addedMember = await _congressMemberApiService.CreateOrUpdateCongressMemberAsync(member);

                    var message = $"Successfully created or updated: {JsonConvert.SerializeObject(addedMember)}";
                    _logger.LogInformation(message);
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