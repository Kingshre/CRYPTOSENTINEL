from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from prices import get_prices, get_top_coins
from sentiment import analyze_coin
from alerts import check_alerts
from portfolio import get_portfolio_value

app = Flask(__name__)
CORS(app)

DEFAULT_COINS = ["bitcoin", "ethereum", "solana"]

@app.route("/")
def index():
    return jsonify({
        "name": "CryptoSentinel API",
        "version": "1.0.0",
        "endpoints": ["/prices", "/sentiment", "/alerts", "/top", "/portfolio"]
    })

@app.route("/prices")
def prices():
    coins = request.args.get("coins", ",".join(DEFAULT_COINS)).split(",")
    data = get_prices([c.strip() for c in coins])
    return jsonify(data)

@app.route("/top")
def top_coins():
    limit = int(request.args.get("limit", 10))
    data = get_top_coins(limit)
    return jsonify(data)

@app.route("/sentiment/<coin>")
def sentiment(coin):
    data = analyze_coin(coin.lower())
    return jsonify(data)

@app.route("/alerts")
def alerts():
    coins = request.args.get("coins", ",".join(DEFAULT_COINS)).split(",")
    data = check_alerts([c.strip() for c in coins])
    return jsonify(data)

@app.route("/portfolio")
def portfolio():
    data = get_portfolio_value()
    return jsonify(data)

@app.route("/portfolio/update", methods=["POST"])
def update_portfolio():
    body = request.get_json()
    if not body or "holdings" not in body:
        return jsonify({"error": "Invalid payload"}), 400
    from portfolio import save_portfolio, load_portfolio
    current = load_portfolio()
    current["holdings"] = body["holdings"]
    if "cost_basis" in body:
        current["cost_basis"] = body["cost_basis"]
    save_portfolio(current)
    return jsonify({"status": "ok", "portfolio": current})

if __name__ == "__main__":
    print("🚀 CryptoSentinel API running on http://localhost:5000")
    app.run(debug=True, port=5000)