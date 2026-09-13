import os
from typing import Optional

import httpx
from mcp.server.fastmcp import FastMCP

# Local (stdio) MCP server. The same tools are also available without installation as a remote
# MCP server at https://yasinozen.com/etf-flows/mcp
mcp = FastMCP("etf-flows")

API_KEY = os.environ.get("ETF_FLOWS_API_KEY")
API_URL = os.environ.get("ETF_FLOWS_API_URL", "https://yasinozen.com/etf-flows/api/v1/flows")
SITE_URL = "https://yasinozen.com/etf-flows"


def _get(params: dict) -> dict:
    headers = {"X-API-Key": API_KEY} if API_KEY else {}
    response = httpx.get(API_URL, params=params, headers=headers, timeout=15.0)
    if response.status_code == 429:
        raise RuntimeError("Rate limit exceeded. Please wait a minute before making another request.")
    body = response.json()
    if response.status_code != 200 or not body.get("success"):
        raise RuntimeError(body.get("error") or f"API error (HTTP {response.status_code})")
    return body


def _usd(value: float) -> str:
    return f"{'-' if value < 0 else '+'}${abs(value) / 1e6:,.1f}M"


def _format(body: dict, title: str) -> str:
    rows = body.get("data") or []
    if not rows:
        return f"{title}\nNo records found."
    lines = [title]
    for row in rows:
        label = row["ticker"] + (f" {row['fund']}" if row.get("fund") else "")
        line = f"- {row['flow_date']} [{label}]: {_usd(row['net_flow_usd'])}"
        if isinstance(row.get("funds"), dict) and row["funds"]:
            line += " (" + ", ".join(f"{k} {_usd(v)}" for k, v in row["funds"].items()) + ")"
        lines.append(line)
    meta = body.get("meta", {})
    if meta.get("restricted_mode"):
        lines.append(f"\n[Notice] {meta.get('message', '')} Free key: {SITE_URL}/get-api-key/ · Pro: {SITE_URL}/#pricing")
    return "\n".join(lines)


@mcp.tool()
def get_latest_etf_flows(ticker: str = "BTC", days: int = 10, include_funds: bool = False) -> str:
    """
    Fetch the most recent daily net flows (USD) of US spot Bitcoin or Ethereum ETFs.

    Args:
        ticker: 'BTC' or 'ETH' (default 'BTC')
        days: number of most recent trading days (default 10)
        include_funds: include the per-fund breakdown such as IBIT, FBTC, GBTC (requires a free or Pro key)
    """
    try:
        body = _get({"asset": ticker.upper(), "limit": days, "include_funds": str(include_funds).lower()})
        return _format(body, f"Latest US spot {ticker.upper()} ETF net flows:")
    except Exception as e:
        return f"Error fetching ETF flows: {e}"


@mcp.tool()
def query_etf_flows_by_date_range(start_date: str, end_date: str, ticker: Optional[str] = None) -> str:
    """
    Query historical daily ETF net flows within a date range (inclusive).

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        ticker: Optional 'BTC' or 'ETH'; both when omitted
    """
    params = {"start": start_date, "end": end_date, "limit": 5000}
    if ticker:
        params["asset"] = ticker.upper()
    try:
        return _format(_get(params), f"ETF net flows from {start_date} to {end_date}:")
    except Exception as e:
        return f"Error querying flows: {e}"


@mcp.tool()
def get_fund_flows(fund: str, days: int = 10) -> str:
    """
    Daily net flows (USD) for a single ETF by ticker, e.g. IBIT, FBTC, GBTC, ARKB, ETHA, FETH. Requires a free or Pro key.

    Args:
        fund: ETF ticker
        days: number of most recent trading days (default 10)
    """
    try:
        return _format(_get({"fund": fund.upper(), "limit": days}), f"{fund.upper()} daily net flows:")
    except Exception as e:
        return f"Error fetching fund flows: {e}"


@mcp.tool()
def get_pro_access_info() -> str:
    """
    How to get a free API key or upgrade to Pro for full-history, same-day spot ETF flow data.
    """
    return f"""ETF Flows plans
- No key: latest 7 trading days, totals only, 1-day delay.
- Free key (email only): 90 trading days + per-fund breakdown. Get it: {SITE_URL}/get-api-key/
- Pro ($9.99/month): full history since January 2024, same-day data, CSV export, 120 requests/minute.
  Buy: https://www.shopier.com/ysnzn/49360250

Set your key with the environment variable ETF_FLOWS_API_KEY=your_key_here
No install needed: add {SITE_URL}/mcp as a remote MCP server in Claude, ChatGPT, Cursor or VS Code."""


if __name__ == "__main__":
    mcp.run()
