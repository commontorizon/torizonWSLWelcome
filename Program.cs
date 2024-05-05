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
});

win.Run();
