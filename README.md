# Coastline Intel — Competitor Intelligence MCP Server

A local MCP server for Harbour Play that reads brand and competitor data and generates a markdown intelligence report using Claude.

---

## What it does

Exposes four tools to Claude:

| Tool | What it returns |
|---|---|
| `get_brand_brief` | Contents of `brand_brief.md` |
| `get_competitors` | Contents of `competitors.md` |
| `get_competitor_notes` | Contents of `competitor_notes.md` |
| `generate_competitor_insights` | A full markdown competitor intelligence report |

---

## Setup

### 1. Install dependencies

```bash
cd "coastline-intel"
pip install -r requirements.txt
```

> If you use a virtual environment:
> ```bash
> python -m venv .venv
> source .venv/bin/activate   # Mac/Linux
> .venv\Scripts\activate      # Windows
> pip install -r requirements.txt
> ```

### 2. Set your Anthropic API key

The `generate_competitor_insights` tool calls the Claude API. You need an API key:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

To make this permanent, add it to your `~/.zshrc` or `~/.bashrc`.

### 3. Test the server runs

```bash
python server.py
```

You should see no output (it waits for MCP input over stdio). Press `Ctrl+C` to stop.

---

## Connect to Claude Code

Add the server to your Claude Code MCP config. Open (or create) `~/.claude/settings.json` and add:

```json
{
  "mcpServers": {
    "coastline-intel": {
      "command": "python",
      "args": ["/FULL/PATH/TO/coastline-intel/server.py"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-..."
      }
    }
  }
}
```

Replace `/FULL/PATH/TO/coastline-intel/server.py` with the actual path on your machine. For example:

```
/Users/yourname/vibe Project/coastline-intel/server.py
```

> **Tip:** Run `pwd` inside the `coastline-intel` folder to get the full path.

Restart Claude Code after saving the config.

---

## Usage

Once connected, ask Claude things like:

- "Read the brand brief and competitor notes, then generate a competitor intelligence report."
- "Use the coastline-intel tools to analyse our competitors and give me recommendations."
- "Call generate_competitor_insights and save the output to report.md."

Claude will call the tools in sequence and return the full markdown report.

---

## File structure

```
coastline-intel/
├── server.py           # MCP server
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── brand_brief.md      # Harbour Play brand info
├── competitors.md      # Competitor list and URLs
└── competitor_notes.md # Manually collected competitor notes
```

---

## Updating the data

Edit `brand_brief.md`, `competitors.md`, or `competitor_notes.md` directly. The server reads files on each tool call, so changes take effect immediately — no restart needed.
