namespace Common.Clients
{
    public class HttpApiClient
    {
        protected readonly HttpClient _client;

        public HttpApiClient()
        {
            _client = new HttpClient();
        }
    }
}