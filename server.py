#!/usr/bin/env python3
"""Competitor Intelligence MCP Server for Harbour Play"""

import asyncio
from pathlib import Path

import anthropic
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

DATA_DIR = Path(__file__).parent

app = Server("coastline-intel")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_brand_brief",
            description="Read the Harbour Play brand brief",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="get_competitors",
            description="Read the list of competitors and their website URLs",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="get_competitor_notes",
            description="Read the manually collected competitor analysis notes",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="generate_competitor_insights",
            description=(
                "Generate a full markdown competitor intelligence report "
                "using the brand brief, competitors list, and competitor notes"
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "get_brand_brief":
        text = (DATA_DIR / "brand_brief.md").read_text()
        return [types.TextContent(type="text", text=text)]

    if name == "get_competitors":
        text = (DATA_DIR / "competitors.md").read_text()
        return [types.TextContent(type="text", text=text)]

    if name == "get_competitor_notes":
        text = (DATA_DIR / "competitor_notes.md").read_text()
        return [types.TextContent(type="text", text=text)]

    if name == "generate_competitor_insights":
        brand_brief = (DATA_DIR / "brand_brief.md").read_text()
        competitors = (DATA_DIR / "competitors.md").read_text()
        notes = (DATA_DIR / "competitor_notes.md").read_text()

        prompt = f"""You are a marketing strategist specialising in gaming and entertainment brands.

Using the brand brief, competitor list, and competitor notes below, write a competitor intelligence report in markdown.

---
## Brand Brief
{brand_brief}

## Competitors
{competitors}

## Competitor Notes
{notes}
---

Structure the report with these sections:

# Competitor Intelligence Report — Harbour Play

## 1. Executive Summary
Two to three sentences covering the most important finding.

## 2. Competitor Profiles
A short paragraph on each competitor covering their positioning, messaging style, and strengths.

## 3. Competitive Gaps
Where the competitors are weak or silent — and where Harbour Play has room to stand out.

## 4. Content & Messaging Opportunities
Specific angles, topics, or tones that are underused across the competitive set.

## 5. Recommended Actions
Five specific, prioritised actions Harbour Play should take next.

Keep everything grounded in the notes provided. Be direct and practical."""

        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-opus-4-6",  # current flagship model (March 2026)
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )

        report = response.content[0].text
        return [types.TextContent(type="text", text=report)]

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
