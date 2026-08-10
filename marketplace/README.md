# JAXA Earth MCP & スキル マーケットプレイス カタログ

本リポジトリには、JAXA (宇宙航空研究開発機構) の地球観測データを扱うための MCP (Model Context Protocol) サーバー、Claude/OpenCode Agent スキル、および PyPI パッケージが含まれています。

## 🚀 インストール手順

### 1. PyPI からのインストール
```bash
pip install jaxa-earth-mcp
# または uv を使用
uv pip install jaxa-earth-mcp
```

### 2. OpenCode への組み込み
`opencode.json` または `.opencode/plugins.json` に以下を追加します:
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

### 3. Claude Desktop 設定
`%APPDATA%\Claude\claude_desktop_config.json` (Windows) または `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) に追加します:
```json
{
  "mcpServers": {
    "jaxa-earth": {
      "command": "uvx",
      "args": [
        "jaxa-earth-mcp"
      ]
    }
  }
}
```

### 4. Agent スキルの利用
`skills/jaxa-earth/SKILL.md` をお使いのエージェントスキルディレクトリ（例: `.claude/skills/jaxa-earth/SKILL.md` や `.agents/skills/jaxa-earth/SKILL.md`）にコピーします。
