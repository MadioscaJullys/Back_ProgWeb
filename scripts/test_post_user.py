import requests
import time

url = "http://127.0.0.1:8000/users/"
payload = {
    "email": f"test_user_{int(time.time())}@example.com",
    "password": "VeryLongPassword123!",
    "full_name": "Test User",
    "profile_image_url": None,
    "role_id": 1
}

print('Posting to', url)
resp = requests.post(url, json=payload)
print('Status:', resp.status_code)
try:
    print('JSON:', resp.json())
except Exception:
    print('Text:', resp.text)
