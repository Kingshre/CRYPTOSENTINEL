import argparse
import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

def print_header():
    print("""
 ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗ 
██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗
██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║
██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║
╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝
 ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝ 
        CryptoSentinel — Real-time Crypto Alerts
    """)

def cmd_prices(args):
    coins = args.coins or "bitcoin,ethereum,solana"
    r = requests.get(f"{BASE_URL}/prices?coins={coins}")
    data = r.json()
    print(f"\n{'Coin':<15} {'Price (USD)':>12} {'24h Change':>12}")
    print("-" * 42)
    for coin, info in data.items():
        change = info.get("usd_24h_change", 0)
        direction = "▲" if change >= 0 else "▼"
        print(f"{coin:<15} ${info['usd']:>11,.2f} {direction} {abs(change):.2f}%")

def cmd_sentiment(args):
    coin = args.coin or "bitcoin"
    r = requests.get(f"{BASE_URL}/sentiment/{coin}")
    data = r.json()
    label = data["label"].upper()
    score = data["score"]
    emoji = "🟢" if label == "BULLISH" else "🔴" if label == "BEARISH" else "🟡"
    print(f"\n{emoji}  {coin.upper()} Sentiment: {label} (score: {score})\n")
    print("Recent Headlines:")
    for h in data["headlines"][:5]:
        bar = "+" if h["score"] >= 0 else "-"
        print(f"  [{bar}{abs(h['score']):.2f}] {h['headline']}")

def cmd_alerts(args):
    coins = args.coins or "bitcoin,ethereum,solana"
    r = requests.get(f"{BASE_URL}/alerts?coins={coins}")
    data = r.json()
    print(f"\n🔍 Alert scan for: {coins}\n")
    for result in data:
        print(f"{result['coin'].upper():<12} ${result['price']:>10,.2f}  "
              f"({result['change_24h']:+.2f}%)  |  "
              f"Sentiment: {result['sentiment'].upper()}")
        if result["alerts"]:
            for alert in result["alerts"]:
                icons = {"critical": "🚨", "high": "🔴", "medium": "🟡", "low": "🟢"}
                icon = icons.get(alert["severity"], "⚪")
                print(f"  {icon} {alert['message']}")
        else:
            print("  ✅ No alerts")
        print()

def cmd_top(args):
    limit = args.limit or 10
    r = requests.get(f"{BASE_URL}/top?limit={limit}")
    data = r.json()
    print(f"\n{'#':<4} {'Coin':<15} {'Price':>12} {'24h':>10} {'Market Cap':>18}")
    print("-" * 62)
    for i, coin in enumerate(data, 1):
        change = coin.get("price_change_percentage_24h", 0)
        direction = "▲" if change >= 0 else "▼"
        mcap = f"${coin['market_cap']:,.0f}"
        print(f"{i:<4} {coin['name']:<15} ${coin['current_price']:>11,.2f} "
              f"{direction}{abs(change):>6.2f}% {mcap:>18}")

def main():
    print_header()
    parser = argparse.ArgumentParser(prog="sentinel", description="CryptoSentinel CLI")
    sub = parser.add_subparsers(dest="command")

    # prices
    p_prices = sub.add_parser("prices", help="Get current prices")
    p_prices.add_argument("--coins", help="Comma-separated coin ids (default: bitcoin,ethereum,solana)")

    # sentiment
    p_sent = sub.add_parser("sentiment", help="Get sentiment for a coin")
    p_sent.add_argument("--coin", help="Coin id (default: bitcoin)")

    # alerts
    p_alerts = sub.add_parser("alerts", help="Run alert check")
    p_alerts.add_argument("--coins", help="Comma-separated coin ids")

    # top
    p_top = sub.add_parser("top", help="Top coins by market cap")
    p_top.add_argument("--limit", type=int, help="Number of coins (default: 10)")

    args = parser.parse_args()

    if args.command == "prices":
        cmd_prices(args)
    elif args.command == "sentiment":
        cmd_sentiment(args)
    elif args.command == "alerts":
        cmd_alerts(args)
    elif args.command == "top":
        cmd_top(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()