import os
import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_alert(coin: str, alerts: list[dict], price: float, change_24h: float, sentiment: str, sentiment_score: float):
    if not WEBHOOK_URL:
        print("No Discord webhook URL set")
        return

    severity_emoji = {"critical": "🚨", "high": "🔴", "medium": "🟡", "low": "🟢"}
    sentiment_emoji = {"bullish": "🟢", "bearish": "🔴", "neutral": "🟡"}

    # Build alert lines
    alert_lines = "\n".join([
        f"{severity_emoji.get(a['severity'], '⚪')} **[{a['severity'].upper()}]** {a['message']}"
        for a in alerts
    ])

    embed = {
        "embeds": [{
            "title": f"⚡ CryptoSentinel Alert — {coin.upper()}",
            "color": 0xff4444 if any(a["severity"] == "critical" for a in alerts) else 0xffd166,
            "fields": [
                {"name": "💰 Price", "value": f"${price:,.2f}", "inline": True},
                {"name": "📈 24h Change", "value": f"{change_24h:+.2f}%", "inline": True},
                {"name": "🧠 Sentiment", "value": f"{sentiment_emoji.get(sentiment, '⚪')} {sentiment.upper()} ({sentiment_score})", "inline": True},
                {"name": "🚨 Alerts Triggered", "value": alert_lines or "None", "inline": False},
            ],
            "footer": {"text": "CryptoSentinel · Real-time Crypto Monitoring"}
        }]
    }

    response = requests.post(WEBHOOK_URL, json=embed)
    if response.status_code == 204:
        print(f"✅ Discord alert sent for {coin.upper()}")
    else:
        print(f"❌ Failed to send Discord alert: {response.status_code}")


def notify_if_needed(alert_results: list[dict]):
    """Send Discord notifications for any coins with active alerts."""
    for result in alert_results:
        if result["alerts"]:
            send_discord_alert(
                coin=result["coin"],
                alerts=result["alerts"],
                price=result["price"],
                change_24h=result["change_24h"],
                sentiment=result["sentiment"],
                sentiment_score=result["sentiment_score"]
            )


if __name__ == "__main__":
    # Test the notifier directly
    test_results = [{
        "coin": "bitcoin",
        "price": 75000,
        "change_24h": -6.5,
        "sentiment": "bearish",
        "sentiment_score": -0.203,
        "alerts": [
            {"type": "DANGER_ZONE", "message": "BITCOIN is in DANGER ZONE — price down + bearish sentiment", "severity": "critical"}
        ]
    }]
    notify_if_needed(test_results)