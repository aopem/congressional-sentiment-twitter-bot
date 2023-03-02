using Microsoft.AspNetCore.WebUtilities;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Hosting;
using Azure.Identity;
using Common.Clients;
using Common.ResponseTypes;

namespace Common.Brokers.Azure
{
    public class AzureBroker : HttpApiClient
    {
        protected readonly ILogger<AzureBroker> _logger;
        protected readonly IConfiguration _configuration;
        protected readonly string? _subscriptionId;
        protected readonly string? _resourceGroup;
        private readonly string? _msiName;
        private readonly string? _apiVersion;

        public AzureBroker(
            ILogger<AzureBroker> logger,
            IConfiguration configuration)
        {
            if (configuration is null)
            {
                var error = "[ERROR] Configuration is null";
                throw new Exception(error);
            }

            _logger = logger;
            _configuration = configuration;
            _subscriptionId = _configuration.GetValue<string>("Azure:SubscriptionId");
            _resourceGroup = _configuration.GetValue<string>("ResourceGroupName");
            _msiName = _configuration.GetValue<string>("ManagedIdentity:Name");
            _apiVersion = _configuration.GetValue<string>("ManagedIdentity:RestApiVersion");
        }

        public DefaultAzureCredential GetDevelopmentCredential()
        {
            _logger.LogInformation($"Retrieving Azure credential...");

            DefaultAzureCredential? credential = null;
            try
            {
                _logger.LogInformation("Using default Azure credential...");
                credential = new DefaultAzureCredential();
            }
            catch (Exception e)
            {
                _logger.LogError(e.ToString());
            }

            if (credential is null)
            {
                throw new Exception("[ERROR] Azure credential is null");
            }

            _logger.LogInformation("Azure credential acquired");
            return credential;
        }

        public DefaultAzureCredential GetProductionCredential()
        {
            _logger.LogInformation($"Retrieving Azure credential...");

            DefaultAzureCredential? credential = null;
            try
            {
                // if using a production/cloud environment, use MSI
                _logger.LogInformation($"Credential attempting to use MSI client ID...");
                var msiClientId = GetMsiClientId();

                _logger.LogInformation($"Obtained MSI client ID: {msiClientId}");
                credential = new DefaultAzureCredential(new DefaultAzureCredentialOptions
                {
                    ManagedIdentityClientId = msiClientId
                });
            }
            catch (Exception e)
            {
                _logger.LogError(e.ToString());
            }

            if (credential is null)
            {
                throw new Exception("[ERROR] Azure credential is null");
            }

            _logger.LogInformation("Azure credential acquired");
            return credential;
        }

        private string GetMsiClientId()
        {
            // build MSI resource ID, auth URI
            var msiResourceId = String.Join(
                $"/subscriptions/{_subscriptionId}/resourcegroups",
                $"/{_resourceGroup}/providers",
                $"/Microsoft.ManagedIdentity/userAssignedIdentities/{_msiName}");

            var endpoint = Environment.GetEnvironmentVariable("IDENTITY_ENDPOINT");
            if (endpoint is null)
            {
                var error = "[ERROR] 'IDENTITY_ENDPOINT' for IMDS is null";
                _logger.LogError(error);
                throw new Exception(error);
            }

            var authUri = QueryHelpers.AddQueryString(endpoint, new Dictionary<string, string?>
            {
                {"resource", "https://vault.azure.net"},
                {"api-version", _apiVersion},
                {"mi_res_id", msiResourceId}
            });

            _httpClient.DefaultRequestHeaders.Add("X-IDENTITY-HEADER", Environment.GetEnvironmentVariable("IDENTITY_HEADER"));

            // make GET request to managed identity REST endpoint
            // this does not need to be async, so running synchronously for simplicity
            var getTask = Task.Run(() => _httpClient.GetAsync(authUri));
            getTask.Wait();
            var response = getTask.Result;
            if (!response.IsSuccessStatusCode)
            {
                var error = String.Join(
                    $"[ERROR] Status code = {response.StatusCode}, could not retrieve MSI client ID from endpoint\n",
                    $"Request URI: {authUri}");
                _logger.LogError(error);
                throw new Exception(error);
            }

            // read response and get client ID
            var readTask = Task.Run(() => response.Content.ReadAsAsync<ManagedIdentityResponse>());
            readTask.Wait();

            var clientId = readTask.Result.ClientId;
            if (clientId is null)
            {
                var error = String.Join(
                    $"[ERROR] Managed identity client ID is null",
                    $"Response: {response.ToString()}"
                );
                _logger.LogError(error);
                throw new Exception(error);
            }

            return clientId;
        }
    }
}