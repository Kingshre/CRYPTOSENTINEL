from notifier import notify_if_needed
from prices import get_prices
from sentiment import analyze_coin

# Default alert rules
DEFAULT_RULES = {
    "price_drop_pct": -5.0,    # Alert if 24h change drops below this %
    "price_rise_pct": 5.0,     # Alert if 24h change rises above this %
    "bearish_threshold": -0.15, # Alert if sentiment score below this
    "bullish_threshold": 0.15,  # Alert if sentiment score above this
}

def check_alerts(coins: list[str], rules: dict = DEFAULT_RULES) -> list[dict]:
    """Check prices and sentiment for coins and return triggered alerts."""
    alerts = []
    prices = get_prices(coins)

    for coin in coins:
        triggered = []
        price_data = prices.get(coin, {})
        sentiment_data = analyze_coin(coin)

        price = price_data.get("usd", 0)
        change_24h = price_data.get("usd_24h_change", 0)
        sentiment_score = sentiment_data.get("score", 0)
        sentiment_label = sentiment_data.get("label", "neutral")

        # Price alerts
        if change_24h <= rules["price_drop_pct"]:
            triggered.append({
                "type": "PRICE_DROP",
                "message": f"{coin.upper()} dropped {change_24h:.2f}% in 24h",
                "severity": "high"
            })
        elif change_24h >= rules["price_rise_pct"]:
            triggered.append({
                "type": "PRICE_SURGE",
                "message": f"{coin.upper()} surged {change_24h:.2f}% in 24h",
                "severity": "medium"
            })

        # Sentiment alerts
        if sentiment_score <= rules["bearish_threshold"]:
            triggered.append({
                "type": "BEARISH_SENTIMENT",
                "message": f"{coin.upper()} sentiment is strongly bearish (score: {sentiment_score})",
                "severity": "medium"
            })
        elif sentiment_score >= rules["bullish_threshold"]:
            triggered.append({
                "type": "BULLISH_SENTIMENT",
                "message": f"{coin.upper()} sentiment is strongly bullish (score: {sentiment_score})",
                "severity": "low"
            })

        # Combined signal — both price drop AND bearish sentiment
        if change_24h <= rules["price_drop_pct"] and sentiment_score <= rules["bearish_threshold"]:
            triggered.append({
                "type": "DANGER_ZONE",
                "message": f"{coin.upper()} is in DANGER ZONE — price down + bearish sentiment",
                "severity": "critical"
            })

        alerts.append({
            "coin": coin,
            "price": price,
            "change_24h": round(change_24h, 2),
            "sentiment": sentiment_label,
            "sentiment_score": sentiment_score,
            "alerts": triggered,
        })
    notify_if_needed(alerts)
    return alerts


if __name__ == "__main__":
    coins = ["bitcoin", "ethereum", "solana"]
    print("🔍 Running CryptoSentinel alert check...\n")
    results = check_alerts(coins)

    for result in results:
        print(f"{result['coin'].upper()} — ${result['price']:,.2f} "
              f"({result['change_24h']:+.2f}%) | "
              f"Sentiment: {result['sentiment'].upper()} ({result['sentiment_score']})")

        if result["alerts"]:
            for alert in result["alerts"]:
                icon = {"critical": "🚨", "high": "🔴", "medium": "🟡", "low": "🟢"}.get(alert["severity"], "⚪")
                print(f"  {icon} [{alert['severity'].upper()}] {alert['message']}")
        else:
            print("  ✅ No alerts triggered")
        print()