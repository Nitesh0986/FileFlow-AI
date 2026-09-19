import requests
import json

url = "http://localhost:8000/api/organize"
payload = {
    "source": r"C:\Users\nites\Desktop\flow\FileFlow-AI\sample_files\incoming",
    "target": r"C:\Users\nites\Desktop\flow\FileFlow-AI\sample_files\organized",
    "dry_run": True,
    "recursive": True
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
