import requests
import csv
import datetime as dt
import time
import os

API_URL = "http://127.0.0.1:8000/api/get-crypto-data/"

# -----------------------------
# Date range
# -----------------------------
start = dt.date(2021, 2, 6)
end   = dt.date(2021, 2, 20)

# -----------------------------
# Output folder
# -----------------------------
OUTPUT_FOLDER = "data_snapshots"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------------
# Loop through each day
# -----------------------------
current = start

while current <= end:
    date_str = current.strftime("%Y-%m-%d")
    filename_str = current.strftime("%Y%m%d")
    output_path = os.path.join(OUTPUT_FOLDER, f"snapshot_{filename_str}.csv")

    print(f"Fetching {date_str} ...")

    try:
        response = requests.post(API_URL, json={"date": date_str})
        response.raise_for_status()
        data = response.json()

        # Skip if error key is present
        if isinstance(data, dict) and "error" in data:
            print(f"Error fetching data for {date_str}: {data['error']}")
            current += dt.timedelta(days=1)
            continue

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "index", "name", "ticker", "market_cap"])

            for coin in data:
                # Print coin for debug
                print(coin)
                writer.writerow([
                    date_str,
                    coin.get("index"),
                    coin.get("name"),
                    coin.get("ticker"),
                    coin.get("market_cap")
                ])

        print(f"Saved snapshot to: {output_path}")

    except requests.RequestException as e:
        print(f"Request failed for {date_str}: {e}")

    time.sleep(2)
    current += dt.timedelta(days=1)

print("Done.")
