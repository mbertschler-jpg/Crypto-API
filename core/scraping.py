import requests
from bs4 import BeautifulSoup
import time

def scrape_crypto_data(formatted_date, limit=25, max_retries=3):
    url = f"https://coincodex.com/historical-data/crypto/?date={formatted_date}T22:00:00Z"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    for attempt in range(1, max_retries + 1):

        response = requests.get(url, headers=headers, timeout=60)
        if response.status_code != 200:
            print(f"[{formatted_date}] HTTP {response.status_code}, retry {attempt}/{max_retries}")
            time.sleep(2 * attempt)
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.select('tr.coin')

        # NEW: retry if nothing is found
        if not rows:
            print(f"[{formatted_date}] no rows found, retry {attempt}/{max_retries}")
            time.sleep(2 * attempt)
            continue

        rows = rows[:limit]

        coins_data = []
        for row in rows:
            index = row.select_one('td.rank')
            name = row.select_one('td.name .full-name')
            ticker = row.select_one('td.name .ticker')
            market_cap = row.select_one('td.market-cap')

            coins_data.append({
                "index": index.text.strip() if index else None,
                "name": name.text.strip() if name else None,
                "ticker": ticker.text.strip() if ticker else None,
                "market_cap": market_cap.text.strip() if market_cap else None,
            })

        # success condition
        if any(coin["index"] is not None for coin in coins_data):
            return coins_data

        print(f"[{formatted_date}] empty values found, retry {attempt}/{max_retries}")
        time.sleep(2 * attempt)

    print(f"[{formatted_date}] failed after {max_retries} attempts, returning empty list")
    return []
