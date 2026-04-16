# messy_code.py
#
# Issues in this one
# Global mutable state (cache)
# No separation between API, processing, and storage
# No retries / poor error handling
# Hardcoded URL
# No classes, no interfaces
# No docstrings or typing
# Blocking loop with sleep

import json,requests,time

URL = "https://api.example.com/data"
cache = {}

def getData(id):
if id in cache:
return cache[id]

```
try:
    r = requests.get(URL + "/" + str(id))
    if r.status_code == 200:
        d = r.json()
        cache[id] = d
        return d
    else:
        print("error", r.status_code)
        return None
except:
    print("request failed")
    return None
```

def processData(d):
res = {}
if not d:
return res

```
for k in d:
    v = d[k]
    if type(v) == int:
        res[k] = v * 10
    elif type(v) == str:
        res[k] = v.lower()
    elif type(v) == list:
        tmp = []
        for i in v:
            if type(i) == int:
                tmp.append(i + 1)
            else:
                tmp.append(i)
        res[k] = tmp
    else:
        res[k] = v

return res
```

def saveToFile(data, name):
f = open(name, "w")
f.write(json.dumps(data))
f.close()

def run():
for i in range(5):
d = getData(i)
p = processData(d)
saveToFile(p, "output_" + str(i) + ".json")
time.sleep(1)

run()
