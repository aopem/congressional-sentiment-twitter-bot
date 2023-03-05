using Common.Clients;
using Common.Models;

namespace SyncMemberDbJob.Brokers
{
    public class CongressMemberApiBroker : HttpApiClient, ICongressMemberApiBroker
    {
        private readonly ILogger<CongressMemberApiBroker> _logger;
        private readonly IConfiguration _configuration;

        public CongressMemberApiBroker(
            ILogger<CongressMemberApiBroker> logger,
            IConfiguration configuration)
        {
            _logger = logger;
            _configuration = configuration;

            // set HTTP client for API calls
            var port = _configuration.GetValue<string>("CongressMemberApi:Port");
            var host = _configuration.GetValue<string>("CongressMemberApi:Host");
            _httpClient.BaseAddress = new Uri($"http://{host}:{port}/api/");
        }

        public async ValueTask<CongressMember?> CreateOrUpdateAsync(CongressMember congressMember)
        {
            var path = "CongressMember";
            var response = await _httpClient.PostAsJsonAsync<CongressMember>(path, congressMember);

            if (!response.IsSuccessStatusCode)
            {
                var error = await response.Content.ReadAsStringAsync();
                _logger.LogError(error);
                return null;
            }

            return await response.Content.ReadAsAsync<CongressMember>();
        }

        public async ValueTask<CongressMember?> GetByIdAsync(string id)
        {
            var path = $"CongressMember/{id}";
            var response = await _httpClient.GetAsync(path);

            if (!response.IsSuccessStatusCode)
            {
                var error = await response.Content.ReadAsStringAsync();
                _logger.LogError(error);
                return null;
            }

            return await response.Content.ReadAsAsync<CongressMember>();
        }

        public async ValueTask<IEnumerable<CongressMember>> GetAllAsync()
        {
            var path = $"CongressMember";
            var response = await _httpClient.GetAsync(path);

            if (!response.IsSuccessStatusCode)
            {
                var error = await response.Content.ReadAsStringAsync();
                _logger.LogError(error);
                return Enumerable.Empty<CongressMember>();
            }

            return await response.Content.ReadAsAsync<IEnumerable<CongressMember>>();
        }

        public async ValueTask<CongressMember?> DeleteByIdAsync(string id)
        {
            var path = $"CongressMember/{id}";
            var response = await _httpClient.DeleteAsync(path);

            if (!response.IsSuccessStatusCode)
            {
                var error = await response.Content.ReadAsStringAsync();
                _logger.LogError(error);
                return null;
            }

            return await response.Content.ReadAsAsync<CongressMember>();
        }
    }
}