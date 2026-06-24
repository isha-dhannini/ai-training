import time
import requests

SERVER_URL = "http://127.0.0.1:5000/notifications"
last_seen_id = 0

print("Polling for notifications every 5 seconds...\n")

while True:
    try:
        response = requests.get(SERVER_URL, params={"after_id": last_seen_id}, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data:
            for item in data:
                print(f"[NEW] {item['id']} - {item['message']} ({item['time']})")
                last_seen_id = max(last_seen_id, item["id"])
        else:
            print("No new notifications.")

    except Exception as exc:
        print("Error while polling:", exc)

    time.sleep(5)
