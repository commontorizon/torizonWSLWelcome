
import os
import subprocess
import threading
import slint # type: ignore
from slint import Timer, TimerMode
from datetime import timedelta

# static var
_process_status = -1
_process_out = ""

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
        self.loading = False
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

    def __create_login(self, login_name, login_rep_psswd):
        global _process_status
        global _process_out

        try:
            # create the user
            subprocess.run(
                f"useradd -m {login_name} -p $(openssl passwd -1 {login_rep_psswd})",
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # run the specific init with the new user
            subprocess.run(
                f"su -c '/opt/specific_init.sh' {login_name}",
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            _process_status = 0

        except subprocess.CalledProcessError as e:
            print(e.stdout)
            print(f"Command failed with error:")
            print(e.stderr)
            _process_status = e.returncode
            _process_out = e.stderr


    def __update_status(self):
        global _process_status
        global _process_out

        # update the UI status
        if _process_status != -1:
            self.cmdResult = _process_out
            self.cmdResultError = _process_status != 0
            self.loading = False

            # and then exit
            self.timer.start(
                TimerMode.SingleShot,
                timedelta(milliseconds=(15000 if self.cmdResultError == False else 5000)),
                self.__close
            )


    @slint.callback
    def createLogin(self):
        # call in a different thread
        threading.Thread(
            target=self.__create_login,
            args=(self.loginName, self.loginRepPsswd)
        ).start()

        # and check the status from time to time
        self.timer.start(
            TimerMode.Repeated,
            timedelta(milliseconds=500),
            self.__update_status
        )


# instantiate the app and start the event loop
app = App()
app.run()
