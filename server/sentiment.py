import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

FEEDS = {
    "bitcoin": "https://cointelegraph.com/rss/tag/bitcoin",
    "ethereum": "https://cointelegraph.com/rss/tag/ethereum",
    "solana": "https://cointelegraph.com/rss/tag/altcoin",
    "general": "https://cointelegraph.com/rss",
}

def get_headlines(coin: str, limit: int = 10) -> list[str]:
    """Fetch recent headlines for a coin from RSS feed."""
    feed_url = FEEDS.get(coin.lower(), FEEDS["general"])
    feed = feedparser.parse(feed_url)
    return [entry.title for entry in feed.entries[:limit]]

def score_sentiment(headlines: list[str]) -> dict:
    """Score a list of headlines and return aggregated sentiment."""
    if not headlines:
        return {"score": 0, "label": "neutral", "headlines": []}

    scored = []
    total = 0
    for headline in headlines:
        score = analyzer.polarity_scores(headline)["compound"]
        total += score
        scored.append({"headline": headline, "score": round(score, 3)})

    avg = total / len(scored)
    label = "bullish" if avg >= 0.05 else "bearish" if avg <= -0.05 else "neutral"

    return {
        "score": round(avg, 3),
        "label": label,
        "headlines": scored,
    }

def analyze_coin(coin: str) -> dict:
    """Full sentiment analysis for a given coin."""
    headlines = get_headlines(coin)
    result = score_sentiment(headlines)
    result["coin"] = coin
    return result

if __name__ == "__main__":
    for coin in ["bitcoin", "ethereum", "solana"]:
        result = analyze_coin(coin)
        print(f"\n{coin.upper()} — Sentiment: {result['label'].upper()} (score: {result['score']})")
        for h in result["headlines"][:3]:
            print(f"  {h['score']:+.3f}  {h['headline']}")