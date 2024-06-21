using Slint;
using Torizon.Shell;
using AppWindow;

var win = new Window();

// create the login
win.CreateLogin = () =>
{
    // create the login
    var _ret = Exec.Bash(
        $"useradd -m {win.loginName} -p $(openssl passwd -1 {win.loginRepPsswd})"
    );

    // close the process
    Environment.Exit(0);
};

// for some reason, the window size is not being respected
// so we set it after a delay
Slint.Timer.Start(TimerMode.SingleShot, 1000, () =>
{
    win.RunOnUiThread(() => {
        win.Width = 800;
        win.Height = 700;
    });

    // check if we are in the test environment
    if (System.IO.File.Exists("/mnt/c/Users/Public/.torizon/password.txt"))
    {
        // read the file
        // the pattern is loginName:loginRepPsswd
        var _file = System.IO.File.ReadAllText(
            "/mnt/c/Users/Public/.torizon/password.txt"
        );

        var _split = _file.Split(':');
        var _loginName = _split[0];
        var _loginRepPsswd = _split[1];

        // set the login name
        win.RunOnUiThread(() => {
            win.loginName = _loginName;
            win.loginPsswd = _loginRepPsswd;
            win.loginRepPsswd = _loginRepPsswd;
            win.createLoginShow = true;
            win.welcomeShow = false;
        });

        Slint.Timer.Start(TimerMode.SingleShot, 2000, () =>
        {
            win.CreateLogin.Invoke();
        });
    }
});

win.Run();
