# ⚡ CryptoSentinel

Real-time crypto monitoring tool that combines live price data and NLP sentiment analysis to fire smart alerts via Discord, CLI, and a React dashboard.

## Features

- 📈 **Live Price Tracking** — fetches real-time prices from CoinGecko API
- 🧠 **Sentiment Analysis** — scores crypto news headlines using VADER NLP
- 🚨 **Smart Alerts** — fires alerts when price + sentiment signals combine
- 💬 **Discord Notifications** — sends formatted embeds to your Discord channel
- 💼 **Portfolio Tracker** — tracks your holdings and shows live P&L
- 🖥️ **React Dashboard** — auto-refreshing web UI built with TypeScript
- ⌨️ **CLI Tool** — full terminal interface with ASCII banner

## Tech Stack

- **Backend:** Python, Flask, Flask-CORS
- **NLP:** VADER Sentiment Analysis
- **Data:** CoinGecko API, RSS feeds (CoinTelegraph)
- **Frontend:** TypeScript, React, Vite
- **Notifications:** Discord Webhooks

## Project Structure

cryptosentinel/
├── server/
│   ├── app.py          # Flask REST API
│   ├── prices.py       # CoinGecko price fetching
│   ├── sentiment.py    # NLP sentiment analysis
│   ├── alerts.py       # Alert engine
│   ├── portfolio.py    # Portfolio tracker
│   └── notifier.py     # Discord webhook notifications
├── cli/
│   └── sentinel.py     # CLI tool
└── web/
└── src/
└── App.tsx     # React dashboard

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/Kingshre/CRYPTOSENTINEL.git
cd CRYPTOSENTINEL
```

### 2. Set up Python backend
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install flask flask-cors requests python-dotenv vaderSentiment feedparser
```

### 3. Configure environment
Create a `.env` file in the root:
### 4. Start the Flask API
```bash
python server/app.py
```

### 5. Set up and start the dashboard
```bash
cd web
npm install
npx vite
```
Visit `http://localhost:3000`

### 6. Use the CLI
```bash
python cli/sentinel.py top
python cli/sentinel.py prices --coins bitcoin,ethereum,solana
python cli/sentinel.py alerts
python cli/sentinel.py sentiment --coin bitcoin
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /prices?coins=bitcoin,ethereum` | Live prices |
| `GET /top?limit=10` | Top coins by market cap |
| `GET /sentiment/<coin>` | Sentiment analysis for a coin |
| `GET /alerts?coins=bitcoin,ethereum` | Smart alert check |
| `GET /portfolio` | Portfolio value and P&L |
| `POST /portfolio/update` | Update holdings |

## Alert Types

| Alert | Trigger |
|-------|---------|
| `PRICE_DROP` | 24h change below -5% |
| `PRICE_SURGE` | 24h change above +5% |
| `BEARISH_SENTIMENT` | Sentiment score below -0.15 |
| `BULLISH_SENTIMENT` | Sentiment score above +0.15 |
| `DANGER_ZONE` | Price drop AND bearish sentiment combined |