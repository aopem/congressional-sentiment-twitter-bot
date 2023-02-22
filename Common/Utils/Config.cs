using Newtonsoft.Json;

namespace Common.Utils
{
    public class Config
    {
        public dynamic Properties { get; }

        public Config(string configFilePath)
        {
            var configJson = File.ReadAllText(configFilePath);
            var properties = JsonConvert.DeserializeObject<dynamic>(configJson);
            if (properties is null)
            {
                throw new Exception();
            }

            Properties = properties;
        }
    }
}