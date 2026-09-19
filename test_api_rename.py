import requests
import json

url = "http://localhost:8000/api/rename/single"

# Test 1: Dry run
print("Test 1: Dry run rename")
payload = {
    "source_path": r"C:\Users\nites\Desktop\flow\FileFlow-AI\sample_files\test_rename.txt",
    "new_name": "renamed_test.txt",
    "dry_run": True
}
try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Actual rename
print("\nTest 2: Actual rename")
payload = {
    "source_path": r"C:\Users\nites\Desktop\flow\FileFlow-AI\sample_files\test_rename.txt",
    "new_name": "renamed_test.txt",
    "dry_run": False
}
try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Rename to existing file
print("\nTest 3: Rename to existing file")
payload = {
    "source_path": r"C:\Users\nites\Desktop\flow\FileFlow-AI\sample_files\test_document.txt",
    "new_name": "renamed_test.txt",
    "dry_run": False
}
try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
