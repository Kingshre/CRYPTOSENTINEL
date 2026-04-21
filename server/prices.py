import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("COINGECKO_BASE_URL", "https://api.coingecko.com/api/v3")

def get_prices(coin_ids: list[str], currency: str = "usd", retries: int = 3) -> dict:
    """Fetch current prices for a list of coin IDs from CoinGecko."""
    url = f"{BASE_URL}/simple/price"
    params = {
        "ids": ",".join(coin_ids),
        "vs_currencies": currency,
        "include_24hr_change": "true",
        "include_market_cap": "true",
    }
    for attempt in range(retries):
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 429:
            wait = 30 * (attempt + 1)
            print(f"Rate limited. Waiting {wait}s before retry...")
            time.sleep(wait)
            continue
        response.raise_for_status()
        return response.json()
    return {}

def get_top_coins(limit: int = 10, currency: str = "usd") -> list[dict]:
    """Fetch top N coins by market cap."""
    url = f"{BASE_URL}/coins/markets"
    params = {
        "vs_currency": currency,
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": "false",
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    print("--- Top 5 Coins ---")
    coins = get_top_coins(5)
    for coin in coins:
        change = coin['price_change_percentage_24h']
        direction = "▲" if change >= 0 else "▼"
        print(f"{coin['name']:12} ${coin['current_price']:>10,.2f}  {direction} {abs(change):.2f}%")

    print("\n--- Custom Lookup ---")
    prices = get_prices(["bitcoin", "ethereum", "solana"])
    for coin, data in prices.items():
        print(f"{coin:12} ${data['usd']:>10,.2f}  24h: {data['usd_24h_change']:+.2f}%")