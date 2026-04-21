import { useEffect, useState } from "react";

const API = "http://127.0.0.1:5000";
const COINS = ["bitcoin", "ethereum", "solana"];

type AlertItem = { type: string; message: string; severity: string };
type CoinAlert = {
  coin: string; price: number; change_24h: number;
  sentiment: string; sentiment_score: number; alerts: AlertItem[];
};
type Position = {
  coin: string; amount: number; current_price: number;
  current_value: number; pnl: number; pnl_pct: number; change_24h: number;
};
type Portfolio = {
  positions: Position[]; total_value: number;
  total_cost: number; total_pnl: number; total_pnl_pct: number;
};

const severityColor: Record<string, string> = {
  critical: "#ff4444", high: "#ff6b35", medium: "#ffd166", low: "#06d6a0",
};
const sentimentEmoji: Record<string, string> = {
  bullish: "🟢", bearish: "🔴", neutral: "🟡",
};

export default function App() {
  const [alerts, setAlerts] = useState<CoinAlert[]>([]);
  const [top, setTop] = useState<any[]>([]);
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState("");

  const fetchData = async () => {
    setLoading(true);
    try {
      const [alertRes, topRes, portfolioRes] = await Promise.all([
        fetch(`${API}/alerts?coins=${COINS.join(",")}`),
        fetch(`${API}/top?limit=5`),
        fetch(`${API}/portfolio`),
      ]);
      setAlerts(await alertRes.json());
      setTop(await topRes.json());
      setPortfolio(await portfolioRes.json());
      setLastUpdated(new Date().toLocaleTimeString());
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ fontFamily: "monospace", background: "#0d1117", minHeight: "100vh", color: "#e6edf3", padding: "24px" }}>
      {/* Header */}
      <div style={{ borderBottom: "1px solid #30363d", paddingBottom: "16px", marginBottom: "24px" }}>
        <h1 style={{ margin: 0, fontSize: "24px", color: "#58a6ff" }}>⚡ CryptoSentinel</h1>
        <p style={{ margin: "4px 0 0", color: "#8b949e", fontSize: "13px" }}>
          Real-time crypto price + sentiment alerts
          {lastUpdated && ` · Last updated: ${lastUpdated}`}
          {loading && " · Refreshing..."}
        </p>
      </div>

      {/* Market Overview */}
      <h2 style={{ fontSize: "14px", color: "#8b949e", textTransform: "uppercase", letterSpacing: "1px" }}>Market Overview</h2>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "12px", marginBottom: "32px" }}>
        {top.map((coin) => {
          const change = coin.price_change_percentage_24h;
          const up = change >= 0;
          return (
            <div key={coin.id} style={{ background: "#161b22", border: "1px solid #30363d", borderRadius: "8px", padding: "16px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "8px" }}>
                <img src={coin.image} alt={coin.name} width={20} height={20} />
                <span style={{ fontWeight: "bold", fontSize: "13px" }}>{coin.symbol.toUpperCase()}</span>
              </div>
              <div style={{ fontSize: "16px", fontWeight: "bold" }}>${coin.current_price.toLocaleString()}</div>
              <div style={{ fontSize: "12px", color: up ? "#3fb950" : "#f85149", marginTop: "4px" }}>
                {up ? "▲" : "▼"} {Math.abs(change).toFixed(2)}%
              </div>
            </div>
          );
        })}
      </div>

      {/* Portfolio */}
      {portfolio && (
        <>
          <h2 style={{ fontSize: "14px", color: "#8b949e", textTransform: "uppercase", letterSpacing: "1px" }}>My Portfolio</h2>
          <div style={{ background: "#161b22", border: "1px solid #30363d", borderRadius: "8px", padding: "20px", marginBottom: "32px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
              <div>
                <div style={{ fontSize: "28px", fontWeight: "bold" }}>${portfolio.total_value.toLocaleString()}</div>
                <div style={{ fontSize: "13px", color: "#8b949e" }}>Total Portfolio Value</div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontSize: "20px", fontWeight: "bold", color: portfolio.total_pnl >= 0 ? "#3fb950" : "#f85149" }}>
                  {portfolio.total_pnl >= 0 ? "+" : ""}${portfolio.total_pnl.toLocaleString()} ({portfolio.total_pnl >= 0 ? "+" : ""}{portfolio.total_pnl_pct.toFixed(2)}%)
                </div>
                <div style={{ fontSize: "13px", color: "#8b949e" }}>Total P&L</div>
              </div>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "12px" }}>
              {portfolio.positions.map((pos) => (
                <div key={pos.coin} style={{ background: "#0d1117", borderRadius: "6px", padding: "14px" }}>
                  <div style={{ fontWeight: "bold", fontSize: "14px", marginBottom: "8px", color: "#58a6ff" }}>
                    {pos.coin.toUpperCase()}
                  </div>
                  <div style={{ fontSize: "13px", color: "#8b949e" }}>{pos.amount} coins</div>
                  <div style={{ fontSize: "15px", fontWeight: "bold", margin: "4px 0" }}>${pos.current_value.toLocaleString()}</div>
                  <div style={{ fontSize: "12px", color: pos.pnl >= 0 ? "#3fb950" : "#f85149" }}>
                    {pos.pnl >= 0 ? "+" : ""}${pos.pnl.toLocaleString()} ({pos.pnl >= 0 ? "+" : ""}{pos.pnl_pct.toFixed(2)}%)
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}

      {/* Sentiment & Alerts */}
      <h2 style={{ fontSize: "14px", color: "#8b949e", textTransform: "uppercase", letterSpacing: "1px" }}>Sentiment & Alerts</h2>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px" }}>
        {alerts.map((result) => (
          <div key={result.coin} style={{ background: "#161b22", border: "1px solid #30363d", borderRadius: "8px", padding: "20px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
              <h3 style={{ margin: 0, fontSize: "16px", color: "#58a6ff" }}>{result.coin.toUpperCase()}</h3>
              <span style={{ fontSize: "12px", color: "#8b949e" }}>
                {sentimentEmoji[result.sentiment]} {result.sentiment.toUpperCase()}
              </span>
            </div>
            <div style={{ fontSize: "22px", fontWeight: "bold", marginBottom: "4px" }}>${result.price.toLocaleString()}</div>
            <div style={{ fontSize: "13px", color: result.change_24h >= 0 ? "#3fb950" : "#f85149", marginBottom: "16px" }}>
              {result.change_24h >= 0 ? "▲" : "▼"} {Math.abs(result.change_24h).toFixed(2)}% (24h)
            </div>
            <div style={{ fontSize: "12px", color: "#8b949e", marginBottom: "8px" }}>Sentiment Score: {result.sentiment_score}</div>
            {result.alerts.length === 0 ? (
              <div style={{ fontSize: "13px", color: "#3fb950" }}>✅ No alerts triggered</div>
            ) : (
              result.alerts.map((a, i) => (
                <div key={i} style={{
                  background: "#0d1117", borderLeft: `3px solid ${severityColor[a.severity]}`,
                  padding: "8px 12px", borderRadius: "4px", marginTop: "8px", fontSize: "12px"
                }}>
                  <span style={{ color: severityColor[a.severity], fontWeight: "bold" }}>[{a.severity.toUpperCase()}]</span>{" "}
                  {a.message}
                </div>
              ))
            )}
          </div>
        ))}
      </div>

      <div style={{ marginTop: "32px", textAlign: "center", color: "#8b949e", fontSize: "12px" }}>
        Auto-refreshes every 30s · Built with Flask + TypeScript + React
      </div>
    </div>
  );
}