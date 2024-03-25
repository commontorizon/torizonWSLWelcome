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

win.Run();
