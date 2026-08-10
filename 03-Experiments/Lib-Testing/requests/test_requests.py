import requests

response = requests.get("https://httpbin.org/get")

print("Status:", response.status_code)
print("Content type:", response.headers.get("content-type"))
