# JAXA Earth MCP & Skill Marketplace Catalog

This repository contains the Model Context Protocol (MCP) server, Claude/OpenCode Agent Skill, and PyPI package for accessing JAXA (Japan Aerospace Exploration Agency) Earth observation data.

## 🚀 Marketplace Installation

### 1. PyPI Installation
```bash
pip install jaxa-earth-mcp
# or with uv
uv pip install jaxa-earth-mcp
```

### 2. OpenCode Integration
Add to your `opencode.json` or `.opencode/plugins.json`:
```json
{
  "mcpServers": {
    "jaxa-earth": {
      "command": "uvx",
      "args": ["jaxa-earth-mcp"]
    }
  }
}
```

### 3. Claude Desktop Configuration
Add to `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):
```json
{
  "mcpServers": {
    "jaxa-earth": {
      "command": "uvx",
      "args": ["jaxa-earth-mcp"]
    }
  }
}
```

### 4. Agent Skill Usage
Copy `skills/jaxa-earth/SKILL.md` to your agent skill directory (e.g. `.claude/skills/jaxa-earth/SKILL.md` or `.agents/skills/jaxa-earth/SKILL.md`).
