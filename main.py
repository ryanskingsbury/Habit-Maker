from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.textinput import TextInput
from database import DataBase
import random
import fileinput


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
                        db.add_watcher(self.email.text, self.watcher.text)
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
            HabitWindow.current = self.email.text
            WatchlistWindow.current = self.email.text
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
    user_habits = []
    habit_1 = ObjectProperty(None)
    habit_2 = ObjectProperty(None)
    habit_3 = ObjectProperty(None)
    
    def habitGenBtn(self):
        file = open('habits.txt')
        all_habits = file.readlines()
        habit_index = random.randint(0, len(all_habits)-1)
        rand_habit = all_habits[habit_index]

        user_habits = db.get_habits(self.current)
        while rand_habit in user_habits:
            habit_index = random.randint(0, len(all_habits)-1)
            rand_habit = all_habits[habit_index]
        for idx,element in enumerate(user_habits):
            if element == 'none':
                db.update_habit(self.current, idx, rand_habit)
                break
                
        print (user_habits)
        self.on_enter()

    def pendingBtn(self, indx):
        db.update_status(self.current, indx, 'Pending')
        self.on_enter()

    def reset_button(self):
        db.reset_habits(self.current)
        self.on_enter()
        
    def on_enter(self, *args):
        self.habit_1.text = ""
        self.habit_2.text = ""
        self.habit_3.text = ""
        habit1, val1, habit2, val2, habit3, val3 = db.get_habits(self.current)
        if habit1 != "none":
            self.habit_1.text = "Habit #1: " + habit1 + ":" + val1
        if habit2 != "none":
            self.habit_2.text = "Habit #2: " + habit2 + ":" + val2
        if habit3 != "none":
            self.habit_3.text = "Habit #3: " + habit3 + ":" + val3
                        


class WatchlistWindow(Screen):
    habit_1 = ObjectProperty(None)
    habit_2 = ObjectProperty(None)
    habit_3 = ObjectProperty(None)

    def acceptBtn(self, indx):
        watching = db.get_watching(self.current)
        db.update_status(watching, indx, 'Completed')
        self.on_enter()

    def declineBtn(self, indx):
        watching = db.get_watching(self.current)
        db.update_status(watching, indx, 'Declined')   
        self.on_enter()
    
    def on_enter(self, *args):
        self.habit_1.text = ""
        self.habit_2.text = ""
        self.habit_3.text = ""
        watching = db.get_watching(self.current)
        print(watching)
        if watching != "none":
            habit1, val1, habit2, val2, habit3, val3 = db.get_habits(watching)
            if habit1 != "none":
                self.habit_1.text = "Habit #1: " + habit1 + ":" + val1
            if habit2 != "none":
                self.habit_2.text = "Habit #2: " + habit2 + ":" + val2
            if habit3 != "none":
                self.habit_3.text = "Habit #3: " + habit3 + ":" + val3


class ProfileWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    watcher = ObjectProperty(None)
    donated = ObjectProperty(None)
    
    def on_enter(self, *args):
        password, name, created, watcher, watching, donated = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created
        self.watcher.text = "Watcher: " + watcher
        self.donated.text = "Donated: $" + donated


class WindowManager(ScreenManager):
    pass

def clearMem(self):
    user_habits = []


def invalidForm(error):
    pop = Popup(title='Invalid Form',
                  content=Label(text=error),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt", "users_habits.txt")

screens = [LoginWindow(name="login"),CreateAccountWindow(name="create"),HabitWindow(name="habit"),WatchlistWindow(name="watchlist"),ProfileWindow(name="profile")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()