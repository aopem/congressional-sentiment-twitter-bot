using Microsoft.AspNetCore.WebUtilities;
using Microsoft.Extensions.Configuration;
using Azure.Identity;
using Common.Utils;
using Common.Clients;
using Common.ResponseTypes;

namespace Common.Brokers.Azure
{
    public class AzureBroker : HttpApiClient
    {
        protected readonly IConfiguration _configuration;
        protected readonly string _subscriptionId;
        protected readonly string _resourceGroup;
        private readonly string _msiName;
        private readonly string _apiVersion;
        private readonly string _msiClientId;

        public AzureBroker(IConfiguration configuration)
        {
            if (configuration is null)
            {
                var exception = "[ERROR] Configuration is null";
                throw new Exception(exception);
            }

            _configuration = configuration;
            _subscriptionId = _configuration.GetValue<string>("Azure:SubscriptionId");
            _resourceGroup = _configuration.GetValue<string>("ResourceGroupName");
            _msiName = _configuration.GetValue<string>("ManagedIdentity:Name");
            _apiVersion = _configuration.GetValue<string>("ManagedIdentity:RestApiVersion");
            _msiClientId = GetMsiClientId();
        }

        public DefaultAzureCredential GetCredential()
        {
            Console.WriteLine($"Retrieving Azure credential...");

            // local configuration does not use MSI
            var credential = new DefaultAzureCredential();
            if (!Constants.LOCAL_EXECUTION)
            {
                Console.WriteLine($"Credential is using MSI client ID: {_msiClientId}...");
                credential = new DefaultAzureCredential(new DefaultAzureCredentialOptions
                {
                    ManagedIdentityClientId = _msiClientId
                });
            }

            Console.WriteLine("Azure credential acquired");
            return credential;
        }

        private string GetMsiClientId()
        {
            // use local secrets file when possible
            if (Constants.LOCAL_EXECUTION)
            {
                var secrets = new Config(Constants.SECRETS_FILEPATH);
                return secrets.Properties.msiClientId;
            }

            // build MSI resource ID, auth URI
            var msiResourceId = String.Join(
                $"/subscriptions/{_subscriptionId}/resourcegroups",
                $"/{_resourceGroup}/providers",
                $"/Microsoft.ManagedIdentity/userAssignedIdentities/{_msiName}");

            var endpoint = Environment.GetEnvironmentVariable("IDENTITY_ENDPOINT");
            var authUri = QueryHelpers.AddQueryString(endpoint, new Dictionary<string, string>
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
                var exception = String.Join(
                    $"[ERROR] Status code = {response.StatusCode}, could not retrieve MSI client ID from endpoint\n",
                    $"Request URI: {authUri}");
                throw new Exception(exception);
            }

            // read response and get client ID
            var readTask = Task.Run(() => response.Content.ReadAsAsync<ManagedIdentityResponse>());
            readTask.Wait();

            var clientId = readTask.Result.ClientId;
            if (clientId is null)
            {
                var exception = String.Join(
                    $"[ERROR] Managed identity client ID is null",
                    $"Response: {response.ToString()}"
                );
                throw new Exception(exception);
            }

            return clientId;
        }
    }
}