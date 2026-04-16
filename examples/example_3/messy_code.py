# messy_code_3.py

class Manager:
def **init**(self):
self.users = []
self.logs = []

```
def addUser(self, name, age):
    if age > 0:
        self.users.append({"name": name, "age": age})
    else:
        print("invalid age")

def removeUser(self, name):
    for u in self.users:
        if u["name"] == name:
            self.users.remove(u)

def printUsers(self):
    for u in self.users:
        print(u["name"], u["age"])

def save(self, file):
    f = open(file, "w")
    for u in self.users:
        f.write(u["name"] + "," + str(u["age"]) + "\n")
    f.close()

def load(self, file):
    try:
        f = open(file, "r")
        lines = f.readlines()
        for l in lines:
            parts = l.split(",")
            self.users.append({"name": parts[0], "age": int(parts[1])})
        f.close()
    except:
        print("error loading file")

def log(self, msg):
    self.logs.append(msg)

def showLogs(self):
    for l in self.logs:
        print(l)

def doEverything(self):
    self.addUser("Alice", 25)
    self.addUser("Bob", -1)
    self.printUsers()
    self.save("users.txt")
    self.load("users.txt")
    self.showLogs()
```

m = Manager()
m.doEverything()
