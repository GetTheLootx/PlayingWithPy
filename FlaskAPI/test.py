import requests

BASE = "http://127.0.0.1:5080/"

data = [
    {"name": "Video 2", "views": 200, "likes": 102},
    {"name": "Video 1", "views": 100, "likes": 100},
    {"name": "Video 5", "views": 547, "likes": 77},
]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), json=data[i])
    print(response.json())

input()
response = requests.delete(BASE + "video/0")
print(response)
input()
response = requests.get(BASE + "video/2")
print(response.json())
