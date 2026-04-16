# messy_code.py

import os,sys

data = []

def process(d):
result=[]
for i in d:
if type(i)==int:
if i%2==0:
result.append(i*2)
else:
result.append(i*3)
elif type(i)==str:
result.append(i.strip().upper())
else:
result.append(None)
return result

def save(r,f):
file=open(f,"w")
for x in r:
file.write(str(x)+"\n")
file.close()

def load(f):
if not os.path.exists(f):
print("file not found")
return []
file=open(f,"r")
lines=file.readlines()
file.close()
return [l.strip() for l in lines]

def run():
if len(sys.argv)<2:
print("no file")
return

```
f=sys.argv[1]
d=load(f)

if len(d)==0:
    print("empty")
else:
    out=process(d)
    save(out,"out.txt")
```

class stuff:
def **init**(self,x):
self.x=x

```
def do(self):
    print("doing stuff with",self.x)

def calc(self):
    res=0
    for i in range(10):
        res+=i*self.x
    return res
```

def weird():
x = stuff(5)
x.do()
print(x.calc())

if **name**=="**main**":
run()
weird()
