# Meridian Edge — Agent Starter Kit

The fastest way to connect AI agents to live prediction market consensus data.

**For informational purposes only. Not investment advice.**

---

## What This Is

A collection of reference agent implementations demonstrating how to consume Meridian Edge's prediction market consensus API. Covers the most common agent patterns: monitoring, briefing, divergence detection, settlement tracking, and alerting.

All data is aggregated from multiple regulated prediction markets. These examples are for educational and informational purposes only and do not constitute investment advice.

---

## Prerequisites

```bash
pip install meridianedge
```

Get a free API key at [meridianedge.io/docs](https://meridianedge.io/docs).

Set your key:
```bash
export MERIDIAN_API_KEY=your_key_here
```

Or pass it directly:
```python
from meridianedge import MeridianEdge
me = MeridianEdge(api_key="your_key_here")
```

---

## Quick Start

```python
from meridianedge import MeridianEdge

me = MeridianEdge()

# Get consensus for all NBA events
events = me.consensus(sport="nba")
for e in events:
    print(f"{e['event_name']}: {e['consensus']*100:.1f}%")

# Get a narrative briefing for a specific event
briefing = me.briefing("nba-lakers-celtics-2026-03-26")
print(briefing["narrative"])

# Get all briefings for events settling today
today = me.briefings_today()
print(f"{today['count']} events settling today")
```

---

## Examples

| File | Description |
|------|-------------|
| `examples/divergence_detector.py` | Detects events where markets disagree significantly |
| `examples/consensus_monitor.py` | Watches for consensus movement above a threshold |
| `examples/daily_briefing.py` | Fetches and distributes morning briefing |
| `examples/settlement_tracker.py` | Tracks settlements and builds calibration database |
| `examples/slack_alerter.py` | Posts alerts to Slack when consensus shifts |

---

## API Reference

### `me.consensus(sport=None, limit=50)`

Returns list of current consensus snapshots.

```python
events = me.consensus(sport="nba")
# Returns: [{"event_key", "event_name", "sport", "consensus", "spread",
#             "confidence", "movement", "platforms_reporting", ...}, ...]
```

### `me.briefing(event_key)`

Returns narrative briefing for a specific event.

```python
b = me.briefing("nba-lakers-celtics")
# Returns: {"event_key", "narrative", "consensus", "spread", "movement", ...}
```

### `me.briefings_today()`

Returns briefings for all events with active data in the last 2 hours.

```python
today = me.briefings_today()
# Returns: {"briefings": [...], "count": N}
```

### `me.settlements(limit=20)`

Returns recently settled events.

```python
s = me.settlements(limit=10)
# Returns: [{"event_key", "sport", "outcome", "settled_at", ...}, ...]
```

---

## MCP Server

If you use Claude Desktop or Cursor, install the MCP server for native agent integration:

```json
{
  "mcpServers": {
    "meridianedge": {
      "command": "uvx",
      "args": ["meridianedge-mcp"],
      "env": {
        "MERIDIAN_API_KEY": "your_key_here"
      }
    }
  }
}
```

---

## LangChain Integration

```python
from meridianedge_langchain import MeridianEdgeTool

tool = MeridianEdgeTool()
result = tool.run("What is the consensus on the Lakers game tonight?")
```

See [langchain-tools/](../langchain-tools/) for full implementation.

---

## AI Platform Integrations

Use Meridian Edge consensus data directly inside major AI platforms — no code required:

| Platform | Link | Notes |
|----------|------|-------|
| **ChatGPT** | [Open Custom GPT](https://chatgpt.com/g/g-69c5cf29be388191aeaaf3159cd41697-prediction-market-consensus) | No setup — just open and ask |
| **Claude** | [MCP install guide](https://github.com/meridian-edge/meridian-edge-mcp) | Claude Desktop / Cursor via MCP |
| **Gemini** | [Open Gem](https://gemini.google.com/gem/1aSpfo0atq00TWFEjDJLytxzsnqTdqHjJ) | No setup — just open and ask |

---

## Compliance

- All data is aggregated from publicly available regulated prediction markets
- No exchange names or raw pricing are exposed
- Data is for informational purposes only
- Not investment advice
- See [Terms of Service](https://meridianedge.io/terms.html), [Privacy Policy](https://meridianedge.io/privacy.html), [Risk Disclosure](https://meridianedge.io/risk.html)

**Contact:** support@meridianedge.io

---

## License

MIT License. See LICENSE file.

&copy; 2026 VeraTenet LLC d/b/a Meridian Edge. For informational purposes only. Not investment advice.
