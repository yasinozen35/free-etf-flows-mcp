# Free Spot ETF Flows MCP Server

[![API Status](https://img.shields.io/badge/API-Active%20%26%20Live-10b981?style=for-the-badge&logo=supabase)](https://yasinozen35.github.io/free-etf-flows-mcp/)
[![MCP Support](https://img.shields.io/badge/MCP-Native%20Support-6366f1?style=for-the-badge&logo=python)](https://github.com/yasinozen35/free-etf-flows-mcp)
[![OpenAPI Spec](https://img.shields.io/badge/OpenAPI-3.0-06b6d4?style=for-the-badge&logo=openapi-initiative)](openapi.json)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

🌐 **Live Documentation & Website:** [https://yasinozen35.github.io/free-etf-flows-mcp/](https://yasinozen35.github.io/free-etf-flows-mcp/)  
📄 **OpenAPI 3.0 Specification:** [openapi.json](openapi.json)  
📦 **Smithery MCP Registry:** [https://smithery.ai/servers/yasinozen35/free-etf-flows-mcp](https://smithery.ai/servers/yasinozen35/free-etf-flows-mcp)  
🦎 **Glama MCP Registry:** [https://glama.ai/mcp/servers/yasinozen35/free-etf-flows-mcp](https://glama.ai/mcp/servers/yasinozen35/free-etf-flows-mcp)

This is an open-source Model Context Protocol (MCP) server that connects your AI assistants (like Claude Desktop, Cursor, Windsurf) to Spot Bitcoin (BTC) and Ethereum (ETH) institutional net flow data. 

It fetches clean, normalized data directly from the consolidated institutional data feeds, bypassing messy scrape formats.

---

## ✨ Features

- **Native AI Integration:** Adds `get_latest_etf_flows` and `query_etf_flows_by_date_range` tools to your LLM context.
- **Normalized Values:** Institutional formatting (like brackets for negative values `(219.4)`) are automatically converted to standard USD floats (`-219400000.00`).
- **Free/Preview Fallback:** Works out-of-the-box without an API key in **Limited Preview Mode** (returns 3 latest records with a 1-day delay).
- **Pro Tier support:** Full, real-time historical queries with higher rate limits when configured with an API key.

---

## 🚀 Setup Instructions

### Prerequisites
You need [uv](https://astral.sh/uv/) installed on your machine to run this server easily without managing virtual environments manually.

```bash
# Install uv (Mac/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 1. Configure Claude Desktop
Add the following block to your `claude_desktop_config.json` (located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "etf-flows": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/free-etf-flows-mcp",
        "run",
        "python",
        "mcp_server.py"
      ],
      "env": {
        "ETF_FLOWS_API_KEY": "YOUR_PRO_API_KEY_HERE"
      }
    }
  }
}
```
*Note: If you don't have an API key yet, you can leave the `ETF_FLOWS_API_KEY` empty (or omit it) to run in **Free Preview Mode**.*

### 2. Configure Cursor
1. Open Cursor Settings (**Settings > Features > MCP**).
2. Click **+ Add New MCP Server**.
3. Fill in the details:
   - **Name:** `etf-flows`
   - **Type:** `command`
   - **Command:** `uv --directory /absolute/path/to/free-etf-flows-mcp run python mcp_server.py`
4. Set the environment variable in your terminal/system or configure it directly in Cursor:
   - Key: `ETF_FLOWS_API_KEY`
   - Value: `YOUR_PRO_API_KEY_HERE`

---

## 🛠️ MCP Tools Provided

Once connected, your AI assistant will have access to the following tools:

### 1. `get_latest_etf_flows`
*   **Description:** Get the most recent Spot ETF flow records for a given ticker.
*   **Arguments:**
    *   `ticker` (string, optional): `'BTC'` or `'ETH'`. Defaults to `'BTC'`.

### 2. `query_etf_flows_by_date_range`
*   **Description:** Query historical ETF flows within a specific date range.
*   **Arguments:**
    *   `start_date` (string, required): YYYY-MM-DD format.
    *   `end_date` (string, required): YYYY-MM-DD format.
    *   `ticker` (string, optional): `'BTC'` or `'ETH'`.

---

## 💳 Get a Pro API Key
To unlock unlimited historical data, real-time updates (0-day delay), and higher rate limits, purchase a Pro Developer key from our website:

👉 **[Get Pro API Key](https://www.shopier.com/ysnzn/49360250)** or visit our website **[https://yasinozen35.github.io/free-etf-flows-mcp/](https://yasinozen35.github.io/free-etf-flows-mcp/)**.
