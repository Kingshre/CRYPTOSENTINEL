import json
import os
from prices import get_prices

PORTFOLIO_FILE = os.path.join(os.path.dirname(__file__), "..", "portfolio.json")

def load_portfolio() -> dict:
    """Load portfolio from JSON file."""
    if not os.path.exists(PORTFOLIO_FILE):
        # Default starter portfolio
        default = {
            "holdings": {
                "bitcoin": 0.5,
                "ethereum": 2.0,
                "solana": 10.0
            },
            "cost_basis": {
                "bitcoin": 60000,
                "ethereum": 2000,
                "solana": 70
            }
        }
        save_portfolio(default)
        return default
    with open(PORTFOLIO_FILE, "r") as f:
        return json.load(f)

def save_portfolio(portfolio: dict):
    """Save portfolio to JSON file."""
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f, indent=2)

def get_portfolio_value() -> dict:
    """Calculate current portfolio value and P&L."""
    portfolio = load_portfolio()
    holdings = portfolio["holdings"]
    cost_basis = portfolio.get("cost_basis", {})

    coins = list(holdings.keys())
    prices = get_prices(coins)

    total_value = 0
    total_cost = 0
    positions = []

    for coin, amount in holdings.items():
        price_data = prices.get(coin, {})
        current_price = price_data.get("usd", 0)
        change_24h = price_data.get("usd_24h_change", 0)

        current_value = current_price * amount
        avg_cost = cost_basis.get(coin, current_price)
        cost_value = avg_cost * amount
        pnl = current_value - cost_value
        pnl_pct = ((current_value - cost_value) / cost_value * 100) if cost_value else 0

        total_value += current_value
        total_cost += cost_value

        positions.append({
            "coin": coin,
            "amount": amount,
            "current_price": current_price,
            "current_value": round(current_value, 2),
            "avg_cost": avg_cost,
            "cost_value": round(cost_value, 2),
            "pnl": round(pnl, 2),
            "pnl_pct": round(pnl_pct, 2),
            "change_24h": round(change_24h, 2),
        })

    total_pnl = total_value - total_cost
    total_pnl_pct = ((total_value - total_cost) / total_cost * 100) if total_cost else 0

    return {
        "positions": positions,
        "total_value": round(total_value, 2),
        "total_cost": round(total_cost, 2),
        "total_pnl": round(total_pnl, 2),
        "total_pnl_pct": round(total_pnl_pct, 2),
    }

if __name__ == "__main__":
    data = get_portfolio_value()
    print(f"\n{'='*50}")
    print(f"  PORTFOLIO SUMMARY")
    print(f"{'='*50}")
    for pos in data["positions"]:
        pnl_sign = "+" if pos["pnl"] >= 0 else ""
        print(f"\n  {pos['coin'].upper()}")
        print(f"  Holdings : {pos['amount']} coins")
        print(f"  Price    : ${pos['current_price']:,.2f} ({pos['change_24h']:+.2f}% 24h)")
        print(f"  Value    : ${pos['current_value']:,.2f}")
        print(f"  P&L      : {pnl_sign}${pos['pnl']:,.2f} ({pnl_sign}{pos['pnl_pct']:.2f}%)")
    print(f"\n{'='*50}")
    pnl_sign = "+" if data["total_pnl"] >= 0 else ""
    print(f"  Total Value : ${data['total_value']:,.2f}")
    print(f"  Total P&L   : {pnl_sign}${data['total_pnl']:,.2f} ({pnl_sign}{data['total_pnl_pct']:.2f}%)")
    print(f"{'='*50}\n")