import requests
import json

BASE_URL = "http://localhost:8000/api/v1/recruiter"
LOGIN_URL = f"{BASE_URL}/auth/login/"
METADATA_URL = f"{BASE_URL}/jobs/metadata/"

email = "recruiter@inaworks.com"
password = "password123"

# 1. Login
print(f"Logging in as {email}...")
login_payload = {"email": email, "password": password}
try:
    response = requests.post(LOGIN_URL, json=login_payload)
    response.raise_for_status()
    data = response.json()
    access_token = data.get("access_token") or data.get("token") or data.get("access")
    
    if not access_token:
        print("Login failed: No access token found in response.")
        print(data)
        exit(1)
        
    print("Login successful. Token acquired.")
except Exception as e:
    print(f"Login error: {e}")
    if response:
        print(response.text)
    exit(1)

# 2. Fetch Metadata
print(f"Fetching metadata from {METADATA_URL}...")
headers = {"Authorization": f"Bearer {access_token}"}
try:
    response = requests.get(METADATA_URL, headers=headers)
    
    if response.status_code == 200:
        print("Metadata fetch successful!")
        data = response.json()
        # Print a summary of the data keys
        print("Keys:", list(data.keys()))
        # Check if critical fields exist
        print(f"Industries count: {len(data.get('industries', []))}")
        print(f"Skills count: {len(data.get('skills', []))}")
    else:
        print(f"Metadata fetch failed with status: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Metadata fetch error: {e}")
