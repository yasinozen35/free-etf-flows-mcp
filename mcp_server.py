import os
import sys
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("etf-flows")

# Fetch API configurations
API_KEY = os.environ.get("ETF_FLOWS_API_KEY")
API_URL = "https://ubzimdhjaqeirdhhwzug.supabase.co/functions/v1/smooth-handler"

@mcp.tool()
def get_latest_etf_flows(ticker: str = "BTC") -> str:
    """
    Fetch the most recent Spot ETF flow records for a given ticker (BTC or ETH).
    
    Args:
        ticker: The asset ticker, either 'BTC' or 'ETH' (default 'BTC')
    """
    api_key_to_use = API_KEY or "demo-key-99999"
        
    try:
        params = {
            "api_key": api_key_to_use, 
            "ticker": ticker.upper(), 
            "limit": 10
        }
        
        response = httpx.get(API_URL, params=params, timeout=12.0)
        
        if response.status_code == 429:
            return "Error 429: Rate limit exceeded. Please wait a minute before making another request."
        elif response.status_code != 200:
            return f"Error from API (Status {response.status_code}): {response.text}"
            
        data = response.json()
        if not data.get("success") or not data.get("data"):
            meta = data.get("meta", {})
            msg = meta.get("message", "No data returned.")
            return f"API Response: {msg}"
            
        flows = data["data"]
        lines = [f"Latest ETF Flows for {ticker.upper()}:"]
        for row in flows:
            formatted_flow = f"${row['net_flow_usd']:,.2f}" if row['net_flow_usd'] >= 0 else f"-${abs(row['net_flow_usd']):,.2f}"
            lines.append(f"- {row['flow_date']}: {formatted_flow}")
            
        if data.get("meta", {}).get("restricted_mode"):
            lines.append("\n[Notice] Running in Limited Preview Mode (1-day delay, max 3 records). Upgrade to Pro to unlock real-time history: https://yasinozen35.github.io/free-etf-flows-mcp/#pricing")
            
        return "\n".join(lines)
    except Exception as e:
        return f"Error connecting to ETF Flows API: {e}"

@mcp.tool()
def query_etf_flows_by_date_range(
    start_date: str, 
    end_date: str, 
    ticker: str = None
) -> str:
    """
    Query historical ETF flows within a specific date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        ticker: Optional asset ticker ('BTC' or 'ETH') to filter the query
    """
    api_key_to_use = API_KEY or "demo-key-99999"
        
    try:
        params = {
            "api_key": api_key_to_use, 
            "limit": 100
        }
        if ticker:
            params["ticker"] = ticker.upper()
            
        response = httpx.get(API_URL, params=params, timeout=12.0)
        
        if response.status_code == 429:
            return "Error 429: Rate limit exceeded."
        elif response.status_code != 200:
            return f"Error: {response.text}"
            
        data = response.json()
        if not data.get("success") or not data.get("data"):
            return "No records found or API key restricted."
            
        flows = data["data"]
        
        filtered_flows = [
            f for f in flows 
            if start_date <= f["flow_date"] <= end_date
        ]
        
        if not filtered_flows:
            return f"No records found between {start_date} and {end_date}."
            
        lines = [f"ETF Flows from {start_date} to {end_date}:"]
        for row in filtered_flows:
            formatted_flow = f"${row['net_flow_usd']:,.2f}" if row['net_flow_usd'] >= 0 else f"-${abs(row['net_flow_usd']):,.2f}"
            lines.append(f"- {row['flow_date']} [{row['ticker']}]: {formatted_flow}")
            
        if data.get("meta", {}).get("restricted_mode"):
            lines.append("\n[Notice] Running in Limited Preview Mode. Upgrade to Pro for complete historical date range results: https://yasinozen35.github.io/free-etf-flows-mcp/#pricing")
            
        return "\n".join(lines)
    except Exception as e:
        return f"Error querying flows: {e}"

@mcp.tool()
def get_pro_access_info() -> str:
    """
    Get information on how to upgrade to a Pro API Key for unlimited real-time Spot ETF flow queries.
    """
    return """ETF Flow Pro API Key Upgrade Options:
- Unlimited historical queries (0-day delay) for Spot BTC & ETH ETF net flows.
- Higher rate limits & priority API bandwidth.

Get Pro Key Here: https://yasinozen35.github.io/free-etf-flows-mcp/#pricing
Or Purchase Directly: https://www.shopier.com/ysnzn/49360250

Once purchased, set your environment variable:
ETF_FLOWS_API_KEY=your_key_here"""

if __name__ == "__main__":
    mcp.run()
