from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.textinput import TextInput
from database import DataBase


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    watcher = ObjectProperty(None)

    def submit(self):
        if db.get_user(self.email.text) == -1:
            if self.password.text != "":
                if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
                    if self.watcher.text == "":
                        db.add_user(self.email.text, self.password.text, self.namee.text, 'none', str(0))
                        self.reset()
                        sm.current = "login"
                    elif self.watcher.text != "" and self.watcher.text.count("@") == 1 and self.watcher.text.count(".") > 0:
                        db.add_user(self.email.text, self.password.text, self.namee.text, self.watcher.text, str(0))
                        self.reset()
                        sm.current = "login"
                    else:
                        invalidForm('Watcher email invalid')
                else:
                    invalidForm('User email invalid')
            else:
                invalidForm('Password cannot be empty')
        else:
            invalidForm('User email exists')

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""
        self.watcher.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            ProfileWindow.current = self.email.text
            self.reset()
            sm.current = "habit"
        else:
            invalidForm('Invalid login')

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""

class HabitWindow(Screen):

    def logOut(self):
        sm.current = "login"

    def watchlistBtn(self):
        sm.current = "watchlist"

    def profileBtn(self):
        ProfileWindow.current = self.email.text
        sm.current = "profile"


class WatchlistWindow(Screen):

    def logOut(self):
        sm.current = "login"

    def habitBtn(self):
        sm.current = "habit"

    def profileBtn(self):
        sm.current = "profile"


class ProfileWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    watcher = ObjectProperty(None)
    donated = ObjectProperty(None)
    
    def on_enter(self, *args):
        password, name, created, watcher, donated = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created
        self.watcher.text = "Watcher: " + watcher
        self.donated.text = "Donated: $" + donated

    
    def logOut(self):
        sm.current = "login"

    def habitBtn(self):
        sm.current = "habit"

    def watchlistBtn(self):
        sm.current = "watchlist"


class WindowManager(ScreenManager):
    pass


def invalidForm(error):
    pop = Popup(title='Invalid Form',
                  content=Label(text=error),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"),CreateAccountWindow(name="create"),HabitWindow(name="habit"),WatchlistWindow(name="watchlist"),ProfileWindow(name="profile")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()