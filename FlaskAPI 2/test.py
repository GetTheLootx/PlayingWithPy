import requests

BASE = "http://127.0.0.1:5080/"


response = requests.patch(
    BASE + "video/2", json={"views": 15258, "name": "zajímavý update"}
)
print(response.json())

input()
response = requests.get(
    BASE + "video/2",
)
print(response.json())
