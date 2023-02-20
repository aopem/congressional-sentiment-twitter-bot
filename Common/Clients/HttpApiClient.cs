namespace Common.Clients
{
    public class HttpApiClient
    {
        protected readonly HttpClient _client;

        public HttpApiClient()
        {
            this._client = new HttpClient();
        }
    }
}