using System.Diagnostics;

namespace Torizon.Shell
{
    public static class Exec
    {
        public class Result
        {
            public string? output;
            public int exitCode;
        }

        public static Result Bash(this string cmd)
        {
            var escapedArgs = cmd.Replace("\"", "\\\"");

            var process = new Process()
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "/bin/bash",
                    Arguments = $"-c \"{escapedArgs}\"",
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                }
            };
            process.Start();
            string result = process.StandardOutput.ReadToEnd();
            process.WaitForExit();

            return new Result
            {
                output = result,
                exitCode = process.ExitCode
            };
        }
    }
}
