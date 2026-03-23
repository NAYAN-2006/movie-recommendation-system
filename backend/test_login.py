import json
import urllib.request
import urllib.error

url = "http://localhost:5000/api/login"
payload = {"email": "test@example.com", "password": "password"}

req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})

try:
    with urllib.request.urlopen(req) as res:
        print(res.status)
        print(res.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("HTTP", e.code)
    print(e.read().decode("utf-8"))
except Exception as e:
    print("ERROR", str(e))
