import requests

resp = requests.post("http://localhost:8000/post_data", json={"something": "this"})

print(resp.status_code)

print(resp.text)