namespace Common.Clients
{
    public class HttpApiClient
    {
        protected readonly HttpClient _httpClient;

        public HttpApiClient()
        {
            _httpClient = new HttpClient();
        }
    }
}