namespace Common.Utils
{
    public class Constants
    {
        public static string ROOT_DIR = Path.GetFullPath(Path.Combine(GetInitialDir(), "../../../../"));

        private static string GetInitialDir()
        {
            var initialDir = Path.GetDirectoryName(System.AppDomain.CurrentDomain.BaseDirectory);
            return initialDir is null ? String.Empty : initialDir;
        }
    }
}