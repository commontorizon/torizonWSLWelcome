
import os
import subprocess
import slint # type: ignore
from slint import Timer, TimerMode
from datetime import timedelta

# load the components using load_file to set the style
app_components = slint.load_file("./ui/AppWindow.slint", style="fluent-dark")
class App(app_components.AppWindow): # type: ignore
    def __automated_invoke_login(self):
        self.createLoginShow = False
        self.createLogin()

    def __automated_login(self):
        _automated_ok = False
        _automated_login_path = "/mnt/c/Users/Public/.torizon/password.txt"

        # for WSL
        if os.path.exists("/mnt/c/Users/Public/.torizon/password.txt"):
            _automated_ok = True
        if os.path.exists("./.conf/password.txt"):
            _automated_ok = True
            _automated_login_path = "./.conf/password.txt"

        if _automated_ok:
            with open(_automated_login_path, "r") as file:
                content = file.read()
                login_name, login_rep_psswd = content.split(':')

            # update the UI status
            self.loginName = login_name
            self.loginPsswd = login_rep_psswd
            self.loginRepPsswd = login_rep_psswd
            self.createLoginShow = True
            self.welcomeShow = False

            # invoke the create button callback
            self.timer.start(
                TimerMode.SingleShot,
                timedelta(milliseconds=1000),
                self.__automated_invoke_login
            )


    def __force_resize(self):
        self.Width = 800
        self.Height = 900

        self.timer.start(
            TimerMode.SingleShot,
            timedelta(milliseconds=1000),
            self.__automated_login
        )

    def __close(self):
        self.hide()

    def __init__(self):
        super().__init__()

        # properties for intellisense
        self.cmdResult = ""
        self.cmdResultError = False
        self.createLoginShow = False
        self.welcomeShow = True
        self.Width = 780
        self.Height = 680
        self.labelDoNotMatch = "Repeat password:"
        self.loginName = ""
        self.loginPsswd = ""
        self.loginRepPsswd = ""
        self.backDeg = 0

        # timers
        self.timer = Timer()
        self.timer.start(
            TimerMode.SingleShot,
            timedelta(milliseconds=1000),
            self.__force_resize
        )

    @slint.callback
    def createLogin(self):
        try:
            subprocess.run(
                f"useradd -m {self.loginName} -p $(openssl passwd -1 {self.loginRepPsswd})",
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        except subprocess.CalledProcessError as e:
            print(e.stdout)
            print(f"Command failed with error:")
            print(e.stderr)
            self.cmdResult = e.stderr
            self.cmdResultError = True

        # and then exit
        self.timer.start(
            TimerMode.SingleShot,
            timedelta(milliseconds=(5000 if self.cmdResultError == False else 10000)),
            self.__close
        )


# instantiate the app and start the event loop
app = App()
app.run()
