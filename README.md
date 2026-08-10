# jaxa-earth-mcp 🌍📡

MCP (Model Context Protocol) Server, Agent SKILL, and PyPI package wrapping the official [JAXA Earth Python API](https://data.earth.jaxa.jp/api/python/v0.1.6/docs.md) (`jaxa.earth.je` v0.1.6).

---

## 🌟 Features

- **MCP Tools**:
  - `list_collections`: Search & filter available satellite datasets (AW3D30, GSMaP, GCOM-C, ALOS-2, etc.).
  - `get_api_documentation`: Access structured API reference & code samples (`docs.md` v0.1.6).
  - `generate_jaxa_python_script`: Auto-generate valid Python code with correct method chaining order.
- **Agent Skill**: High-quality Agent Skill definition (`skills/jaxa-earth/SKILL.md`) for OpenCode, Claude Code, and autonomous AI agents.
- **Marketplace Manifests**: Ready for OpenCode Marketplace, Claude Desktop, and Smithery AI.
- **PyPI Package**: Packaged for distribution via PyPI (`pip install jaxa-earth-mcp`).

---

## 📦 Installation

```bash
# Via pip
pip install jaxa-earth-mcp jaxa-earth

# Via uv
uv pip install jaxa-earth-mcp jaxa-earth
```

---

## ⚙️ Quick Start

### Run MCP Server (stdio mode)
```bash
jaxa-earth-mcp
# or with uvx
uvx jaxa-earth-mcp
```

### Run MCP Server (SSE mode)
```bash
jaxa-earth-mcp --transport sse --port 8000
```

---

## 🔧 Client Setup

### OpenCode Setup
Add to your config:
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

### Claude Desktop Setup
Add to `claude_desktop_config.json`:
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

---

## 🎓 Agent Skill Integration

Copy `skills/jaxa-earth/SKILL.md` to your environment:
- **Claude Code**: `.claude/skills/jaxa-earth/SKILL.md`
- **OpenCode / Agent**: `.agents/skills/jaxa-earth/SKILL.md`

---

## 🚀 Building & PyPI Publishing

```bash
# Build wheel and sdist
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

---

## 📜 License

MIT License
