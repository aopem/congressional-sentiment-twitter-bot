using Microsoft.AspNetCore.WebUtilities;
using Azure.Identity;
using Azure.Core;
using Common.Utils;
using Common.Clients;
using Common.ResponseTypes;

namespace Common.Brokers.Azure
{
    public class AzureBroker : HttpApiClient
    {
        protected Config _config;
        protected string _subscriptionId;
        protected string _resourceGroup;
        private string _msiName;
        private string _apiVersion;
        private string _msiClientId;

        public AzureBroker()
        {
            this._config = new Config(Constants.AZURE_CONFIG_FILEPATH);
            this._subscriptionId = this._config.Properties._subscriptionId;
            this._resourceGroup = this._config.Properties.resourceGroup.name;
            this._msiName = this._config.Properties.resourceGroup.managedIdentity.name;
            this._apiVersion = this._config.Properties.resourceGroup.managedIdentity.restApiVersion;
            this._msiClientId = this.GetMsiClientId();
        }

        public AccessToken GetAccessToken(string authUrl)
        {
            Console.WriteLine($"Retrieving Azure access...");

            // local configuration does not use MSI
            var credential = new DefaultAzureCredential();
            if (!Constants.LOCAL_EXECUTION)
            {
                Console.WriteLine($"Credential is using MSI client ID: {this._msiClientId}...");
                credential = new DefaultAzureCredential(new DefaultAzureCredentialOptions
                {
                    ManagedIdentityClientId = this._msiClientId
                });
            }

            // obtain Azure access token
            AccessToken accessToken = new AccessToken();
            try
            {
                accessToken = credential.GetToken(new TokenRequestContext(new[]
                {
                    authUrl
                }));
            }
            catch (AuthenticationFailedException e)
            {
                Console.WriteLine($"[ERROR] Could not retrieve Azure access token: {e}");
            }

            Console.WriteLine("Azure access token acquired");
            return accessToken;
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
                $"/subscriptions/{this._subscriptionId}/resourcegroups",
                $"/{this._resourceGroup}/providers",
                $"/Microsoft.ManagedIdentity/userAssignedIdentities/{this._msiName}");

            var endpoint = Environment.GetEnvironmentVariable("IDENTITY_ENDPOINT");
            var authUri = QueryHelpers.AddQueryString(endpoint, new Dictionary<string, string>
            {
                {"resource", "https://vault.azure.net"},
                {"api-version", this._apiVersion},
                {"mi_res_id", msiResourceId}
            });

            this._client.DefaultRequestHeaders.Add("X-IDENTITY-HEADER", Environment.GetEnvironmentVariable("IDENTITY_HEADER"));

            // make GET request to managed identity REST endpoint
            // this does not need to be async, so running synchronously for simplicity
            var getTask = Task.Run(() => this._client.GetAsync(authUri));
            getTask.Wait();
            var response = getTask.Result;
            if (!response.IsSuccessStatusCode)
            {
                var exception = String.Join(
                    $"Status code = {response.StatusCode}, could not retrieve MSI client ID from endpoint\n",
                    $"Request URI: {authUri}");
                throw new Exception(exception);
            }

            // read response and get client ID
            var readTask = Task.Run(() => response.Content.ReadAsAsync<ManagedIdentityResponse>());
            readTask.Wait();
            return readTask.Result.ClientId;
        }
    }
}