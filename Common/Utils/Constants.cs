namespace Common.Utils
{
    public class Constants
    {
        public static string ROOT_DIR = Path.GetFullPath(Path.Combine(GetInitialDir(), "../../../../"));
        public static string SECRETS_FILEPATH = Path.Combine(ROOT_DIR, "secrets.json");
        public static string AZURE_CONFIG_FILEPATH = Path.Combine(ROOT_DIR, "config.azure.json");
        public static bool LOCAL_EXECUTION = File.Exists(SECRETS_FILEPATH);

        private static string GetInitialDir()
        {
            var initialDir = Path.GetDirectoryName(System.AppDomain.CurrentDomain.BaseDirectory);
            return initialDir is null ? String.Empty : initialDir;
        }
    }
}