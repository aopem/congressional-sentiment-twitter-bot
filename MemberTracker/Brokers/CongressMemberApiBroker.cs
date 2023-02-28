using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Common.Clients;
using Common.Models;

namespace MemberTracker.Brokers
{
    public class CongressMemberApiBroker : HttpApiClient
    {
        private readonly ILogger<CongressMemberApiBroker> _logger;
        private readonly IConfiguration _configuration;

        public CongressMemberApiBroker(
            ILogger<CongressMemberApiBroker> logger,
            IConfiguration configuration)
        {
            _logger = logger;
            _configuration = configuration;
            _httpClient.BaseAddress = new Uri($"http://localhost:{_configuration.GetValue<string>("CongressMemberApi:Port")}/api/");
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

        public async ValueTask<List<CongressMember>> GetAllAsync()
        {
            var path = $"CongressMember";
            var response = await _httpClient.GetAsync(path);

            if (!response.IsSuccessStatusCode)
            {
                var error = await response.Content.ReadAsStringAsync();
                _logger.LogError(error);
                return new List<CongressMember>();
            }

            return await response.Content.ReadAsAsync<List<CongressMember>>();
        }

        public async ValueTask<CongressMember?> DeleteById(string id)
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