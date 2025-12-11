import requests, time

base = 'http://127.0.0.1:8000'
# create a test user
email = f'test_login_{int(time.time())}@example.com'
user_payload = {
    'email': email,
    'password': 'TestPass1234!',
    'full_name': 'Auth Tester',
    'profile_image_url': None,
    'role_id': 1
}
print('Creating user', email)
r = requests.post(base + '/users/', json=user_payload)
print('Create status:', r.status_code)
try:
    print('Create json:', r.json())
except Exception:
    print('Create text:', r.text)

# now try to login
print('Attempting login')
login_data = {'username': email, 'password': user_payload['password']}
r2 = requests.post(base + '/auth/login', data=login_data)
print('Login status:', r2.status_code)
try:
    print('Login json:', r2.json())
except Exception:
    print('Login text:', r2.text)
