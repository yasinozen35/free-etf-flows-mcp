# ETF Flows MCP Server — Spot Bitcoin & Ethereum ETF Flows for AI Assistants

[![Website](https://img.shields.io/badge/Website-yasinozen.com%2Fetf--flows-3b5bfd?style=for-the-badge)](https://yasinozen.com/etf-flows/)
[![Remote MCP](https://img.shields.io/badge/MCP-Remote%20%2B%20stdio-10b981?style=for-the-badge)](https://yasinozen.com/etf-flows/mcp-server/)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-06b6d4?style=for-the-badge&logo=openapi-initiative)](https://yasinozen.com/etf-flows/openapi.json)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

Give Claude, ChatGPT, Cursor, VS Code or any MCP client **daily net flows for every US spot Bitcoin and Ethereum ETF** — IBIT, FBTC, GBTC, ARKB, ETHA, FETH, ETHE and more.

- 🌐 **Live data pages:** [Bitcoin ETF flows today](https://yasinozen.com/etf-flows/bitcoin/) · [Ethereum ETF flows today](https://yasinozen.com/etf-flows/ethereum/) · [IBIT flows](https://yasinozen.com/etf-flows/bitcoin/ibit/)
- 🔌 **Remote MCP server (no install):** `https://yasinozen.com/etf-flows/mcp`
- 📄 **REST API docs:** [yasinozen.com/etf-flows/api](https://yasinozen.com/etf-flows/api/)

---

## Quick start: remote server (recommended)

**Claude** → Settings → Connectors → *Add custom connector* → `https://yasinozen.com/etf-flows/mcp`

**Claude Code**

```bash
claude mcp add --transport http etf-flows https://yasinozen.com/etf-flows/mcp
```

**Cursor / Windsurf / VS Code** (`mcp.json`)

```json
{
  "mcpServers": {
    "etf-flows": {
      "url": "https://yasinozen.com/etf-flows/mcp",
      "headers": { "X-API-Key": "YOUR_KEY" }
    }
  }
}
```

The key is optional. Clients that cannot send headers can use `https://yasinozen.com/etf-flows/mcp?api_key=YOUR_KEY`.
One-click install links for Cursor and VS Code are on the [setup page](https://yasinozen.com/etf-flows/mcp-server/).

## Tools

| Tool | Description |
|---|---|
| `get_etf_flow_summary` | Latest day, 7/30-day, month-to-date, YTD and cumulative flows, streaks and top funds (remote server) |
| `get_latest_etf_flows` | Daily totals for the most recent trading days, optional per-fund breakdown |
| `get_etf_flows_by_date_range` / `query_etf_flows_by_date_range` | Daily totals between two dates |
| `get_fund_flows` | Daily flows and cumulative total for one ETF (e.g. IBIT) |
| `get_pro_access_info` | Plans and how to get a key |

Example prompts: *“Summarize spot Bitcoin ETF flows this week”*, *“Did IBIT have outflows in the last 10 days?”*, *“Compare Ethereum ETF flows in August and September.”*

## Run locally (stdio)

Requires [uv](https://astral.sh/uv/).

```json
{
  "mcpServers": {
    "etf-flows": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/free-etf-flows-mcp", "run", "python", "mcp_server.py"],
      "env": { "ETF_FLOWS_API_KEY": "YOUR_KEY" }
    }
  }
}
```

## Plans

| | Preview (no key) | Free key | Pro ($9.99/mo) |
|---|---|---|---|
| History | 7 trading days | 90 trading days | Full, since Jan 2024 |
| Delay | 1 day | 1 day | Same day |
| Per-fund data | – | ✓ | ✓ |
| CSV export | – | – | ✓ |
| Rate limit | 10/min | 30/min | 120/min |

👉 [Get a free key](https://yasinozen.com/etf-flows/get-api-key/) · [Upgrade to Pro](https://www.shopier.com/ysnzn/49360250)

## Data

Daily figures are sourced from the public ETF flow tables of [Farside Investors](https://farside.co.uk/) and normalized to US dollars (parenthesized values become negative). See the [methodology](https://yasinozen.com/etf-flows/methodology/). This project is independent and not affiliated with Farside Investors or any ETF issuer. Not investment advice.

---

Built by [Yasin Özen](https://yasinozen.com/) · <!-- mcp-name: com.yasinozen/etf-flows -->
