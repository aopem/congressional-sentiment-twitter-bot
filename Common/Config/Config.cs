using System.Text.Json;

namespace Common.Config
{
    public class Config
    {
        public readonly Dictionary<string, string> Properties;

        public Config(string configFilePath)
        {
            string configJson = File.ReadAllText(configFilePath);
            var properties = JsonSerializer.Deserialize<Dictionary<string, string>>(configJson);
            if (properties is null)
            {
                throw new Exception();
            }

            this.Properties = properties;
        }
    }
}