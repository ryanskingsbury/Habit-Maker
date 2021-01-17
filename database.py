import datetime


class DataBase:
    def __init__(self, filename, habitsfile):
        self.filename = filename
        self.habitsfile = habitsfile
        self.users = None
        self.habits = None
        self.file = None
        self.load()
        self.load_habits()

    def load(self):
        self.file = open(self.filename, "r")
        self.users = {}

        for line in self.file:
            email, password, name, created, watcher, watching, donated = line.strip().split(";")
            self.users[email] = [password, name, created, watcher, watching, donated]

        self.file.close()

    def load_habits(self):
        self.file = open(self.habitsfile, "r")
        self.habits = {}

        for line in self.file:
            email, habit1, val1, habit2, val2, habit3, val3 = line.strip().split(";")
            self.habits[email] = [habit1, val1, habit2, val2, habit3, val3]

        self.file.close()

    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    def add_user(self, email, password, name, watcher, donated):
        if email.strip() not in self.users:
            self.users[email.strip()] = [password.strip(), name.strip(), DataBase.get_date(), watcher.strip(), "none", donated.strip()]
            self.habits[email.strip()] = ["none", "Not completed", "none", "Not completed", "none", "Not completed"]
            self.save()
            self.save_habits()
            return 1
        else:
            return -1

    def get_habits(self, email):
        if email in self.habits:
            return self.habits[email]
        else:
            return -1

    def add_donated(self, email, donation):
        donated = donation + int(self.users[email][4])
        self.users[email][4] = str(donated)
        self.save()

    def add_watcher(self, email, watcher):
        self.users[email][3] = watcher.strip()
        self.users[watcher.strip()][4] = email
        self.save()

    def get_watching(self, email):
        if email in self.users:
            watching = self.users[email][4]
            return watching
        else:
            return -1

    def update_habit(self, email, i, habit):
        if email in self.users:
            self.habits[email][i] = habit.strip()
            self.save_habits()
            return 1
        else:
            return -1

    def update_status(self, email, i, completion_val):
        if email in self.users:
            self.habits[email][i+1] = completion_val.strip()
            self.save_habits()
            return 1
        else:
            return -1

    def reset_habits(self, email):
        self.habits[email][1] = 'Not completed'
        self.habits[email][3] = 'Not completed'
        self.habits[email][5] = 'Not completed'
        self.save_habits()

    def validate(self, email, password):
        if self.get_user(email) != -1:
            return self.users[email][0] == password
        else:
            return False

    def save(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(user + ";" + self.users[user][0] + ";" + self.users[user][1] + ";" + self.users[user][2] + ";" + self.users[user][3] + ";" + self.users[user][4] + ";" + self.users[user][5] + "\n")

    def save_habits(self):
        with open(self.habitsfile, "w") as f:
            for habit in self.habits:
                f.write(habit + ";" + self.habits[habit][0] + ";" + self.habits[habit][1] + ";" + self.habits[habit][2] + ";" + self.habits[habit][3] + ";" + self.habits[habit][4] + ";" + self.habits[habit][5] + "\n")

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]