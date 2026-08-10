# jaxa-earth-mcp 🌍📡

[JAXA Earth Python API](https://data.earth.jaxa.jp/api/python/v0.1.6/docs.md) (`jaxa.earth.je` v0.1.6) をラップした MCP (Model Context Protocol) サーバー、Agent スキル、および PyPI 配布用パッケージです。

---

## 🌟 主な機能

- **MCP ツール**:
    - `list_collections`: 利用可能な衛星データセット（AW3D30, GSMaP, GCOM-C, ALOS-2 等）の検索およびフィルタリング。
    - `get_api_documentation`: API リファレンスとコード例 (`docs.md` v0.1.6) の提供。
    - `generate_jaxa_python_script`: 正しいメソッド呼び出し順序に準拠した Python スクリプトの自動生成。
- **Agent スキル (SKILL)**: OpenCode、Claude Code、各種 AI エージェント向けに最適化された専用スキル (`skills/jaxa-earth/SKILL.md`)。
- **マーケットプレイス対応**: OpenCode プラグイン/スキル、Claude Desktop、Smithery AI 等の設定ファイルを同梱。
- **PyPI パッケージ化**: `pip install jaxa-earth-mcp` で即座に導入可能。

---

## 🗺️ JAXA API リファレンスと MCP 機能の対応表

### 1. MCP メソッド（ツール & プロンプト）対応表

| JAXA Earth API (`jaxa.earth.je` v0.1.6) | MCP メソッド名 | 種別 | 内容・役割 |
|---|---|---|---|
| API 公式仕様書 (`docs.md`) | `get_api_documentation` | Tool | 指定クラス (`FeatureCollection`, `ImageCollection` 等) または全体の公式ドキュメント・コード例を取得 |
| `ImageCollectionList.filter_name()` | `list_collections` | Tool | JAXA プラットフォーム上の衛星データセットおよびバンドの検索・一覧取得 |
| `ImageCollection` + `ImageProcess` 一連のチェイン処理 | `generate_jaxa_python_script` | Tool | 正しい呼び出し順序 (`filter_date` ➔ `filter_resolution` ➔ `filter_bounds` ➔ `select` ➔ `get_images`) に準拠したスクリプト自動生成 |
| API 活用プロンプト | `satellite_data_analysis` | Prompt | 衛星観測データ解析タスク用プロンプトテンプレート |

### 2. MCP リソース対応表

| JAXA Earth API (`jaxa.earth.je` v0.1.6) | MCP リソース URI | 内容・役割 |
|---|---|---|
| API 公式仕様書 (`docs.md`) | `jaxa://docs/api` | JAXA Earth API 全体の公式リファレンスドキュメントリソース |
| 登録済み主要コレクションカタログ | `jaxa://collections/popular` | AW3D30, GSMaP, GCOM-C, ALOS-2 等の主要衛星データセット一覧リソース |

---

## 📦 インストール方法

```bash
# pip を使用する場合
pip install jaxa-earth-mcp jaxa-earth

# uv を使用する場合
uv pip install jaxa-earth-mcp jaxa-earth
```

---

## ⚙️ クイックスタート

### MCP サーバーの起動 (stdio モード)

```bash
jaxa-earth-mcp
# または uvx 経由
uvx jaxa-earth-mcp
```

### MCP サーバーの起動 (SSE モード)

```bash
jaxa-earth-mcp --transport sse --port 8000
```

---

## 🔧 クライアント設定

### OpenCode 設定

`opencode.json` または `.opencode/plugins.json` に追加:

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

### Claude Code / Plugin でのインストール

リポジトリを指定してプラグインとして追加可能です:

```bash
claude plugin add kannkyo/jaxa-earth-mcp
```

または `claude_desktop_config.json` に MCP サーバーとして追加:

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

## 🎓 エージェントスキルの組み込み

`skills/jaxa-earth/SKILL.md` を各自の環境にコピーして使用します:

- **Claude Code**: `.claude/skills/jaxa-earth/SKILL.md`
- **OpenCode / Agent**: `.agents/skills/jaxa-earth/SKILL.md`

---

## 🚀 ビルドおよび PyPI への公開手順

```bash
# パッケージのビルド (.whl および .tar.gz)
python -m build

# PyPI へアップロード
python -m twine upload dist/*
```

---

## 📜 ライセンス

MIT License
