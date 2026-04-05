import requests
import json

url = "http://localhost:8000/signup"
data = {
    "email": "quicktest@example.com",
    "username": "Quick Test",
    "password": "test123"
}

print("Testing signup...")
print(f"URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")

try:
    response = requests.post(url, json=data, timeout=10)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"\nError: {str(e)}")
