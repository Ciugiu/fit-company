import requests
import os

MONOLITH_URL = os.environ.get("MONOLITH_URL", "http://localhost:5000")
ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", "your_admin_api_key_here")

def trigger_wod_jobs():
    url = f"{MONOLITH_URL}/wod/jobs"
    headers = {
        "Authorization": f"Bearer {ADMIN_API_KEY}"
    }
    response = requests.post(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    trigger_wod_jobs()

# 0 6 * * * /usr/bin/python3 /home/ciugiu/Documents/UNI/S4/MicroServices/fit-company/src/fit/cron_job.py