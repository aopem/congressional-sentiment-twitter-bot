namespace CongressMemberAPI
{
    public class Program
    {
        public static void Main(string[] args)
        {
            // initialization
            var builder = WebApplication.CreateBuilder(args);
            var startup = new Startup(builder.Configuration);
            startup.ConfigureServices(builder.Services);

            // build app
            var app = builder.Build();
            startup.Configure(app, builder.Environment);

            // run application
            app.Run();
        }
    }
}