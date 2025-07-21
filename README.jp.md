# Eagle MCP Server

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-1.12.0-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](https://github.com/shingo1228/eagle-mcp-server/releases)

**日本語** | [English](README.md)

[Eagle App](https://eagle.cool/) との統合を行うModern Context Protocol (MCP) サーバーの実装です。このサーバーにより、AIアシスタントが標準化されたインターフェースを通じて包括的なツールと多言語サポートでEagleライブラリとやり取りできます。

## ✨ 機能

- **🏗️ モダンアーキテクチャ**: mcp-pythonで構築された純粋なMCP実装
- **🛠️ 包括的ツール**: 完全なEagle操作のための16の高レベルツール + 17の直接APIツール
- **🎛️ 設定可能なAPIアクセス**: ユーザーフレンドリーツールと高度な開発者ツールの切り替え
- **🌏 多言語サポート**: 日本語テキスト処理の強化とUTF-8エンコーディング
- **🖼️ 画像処理**: Base64エンコーディング、サムネイル生成、メタデータ解析
- **🔌 クロスプラットフォーム**: LM Studio、Claude Desktop、その他のMCPクライアントに対応
- **🛡️ 堅牢なエラーハンドリング**: 包括的なエラーハンドリングとログ機能
- **⚡ 高性能**: 効率的なEagle API統合による非同期実装
- **📝 型安全**: Pydanticバリデーション付きの完全な型注釈

## 🚀 クイックスタート

### 前提条件

- Python 3.11以上
- [uv](https://docs.astral.sh/uv/) パッケージマネージャー
- ローカルで実行中の[Eagle App](https://eagle.cool/) (デフォルト: `localhost:41595`)

### インストール

1. リポジトリをクローンします：
```bash
git clone https://github.com/shingo1228/eagle-mcp-server.git
cd eagle-mcp-server
```

2. 依存関係をインストールします：
```bash
uv sync
```

3. サーバーを起動します：
```bash
# Windows
run.bat

# Unix/Linux/macOS  
uv run main.py
```

## 🔧 設定

### 環境変数

ローカル設定用の `.env.local` ファイルを作成します：

```env
EAGLE_API_URL=http://localhost:41595
EAGLE_API_TIMEOUT=30.0
LOG_LEVEL=INFO

# ツール設定
EXPOSE_DIRECT_API_TOOLS=false  # 高度なAPIアクセスにはtrueに設定

# オプション: カスタムパス
# USER_DATA_DIR=/custom/path/to/data
# CACHE_DIR=/custom/path/to/cache
```

### MCPクライアント設定

#### Claude Desktop

`claude_desktop_config.json` に追加します：

```json
{
  "mcpServers": {
    "eagle-mcp-server": {
      "command": "/path/to/eagle-mcp-server/run.bat",
      "env": {
        "PYTHONPATH": "/path/to/eagle-mcp-server"
      }
    }
  }
}
```

#### LM Studio

MCP設定に追加します：

```json
{
  "mcpServers": {
    "eagle-mcp-server": {
      "command": "/path/to/eagle-mcp-server/run.bat",
      "env": {
        "PYTHONPATH": "/path/to/eagle-mcp-server"
      }
    }
  }
}
```

## 🛠️ 利用可能ツール

### コアツール（常に利用可能）

| ツール | 説明 | パラメータ |
|------|------|----------|
| `health_check` | Eagle API接続状態の確認 | なし |

### フォルダ管理

| ツール | 説明 | パラメータ |
|------|------|----------|
| `folder_list` | Eagleライブラリ内の全フォルダをリスト | なし |
| `folder_search` | 名前でフォルダを検索 | `keyword` |
| `folder_info` | 詳細なフォルダ情報を取得 | `folder_id` |
| `folder_create` | 新しいフォルダを作成 | `folder_name`, `parent_id?` |
| `folder_update` | フォルダプロパティを更新 | `folder_id`, `folder_name?`, `description?` |
| `folder_rename` | フォルダ名を変更 | `folder_id`, `new_name` |

### アイテム管理

| ツール | 説明 | パラメータ |
|------|------|----------|
| `item_search` | キーワードでアイテムを検索 | `keyword`, `limit?` |
| `item_info` | 詳細なアイテム情報を取得 | `item_id` |
| `item_by_folder` | 特定フォルダ内のアイテムを取得 | `folder_id`, `limit?` |
| `item_update_tags` | アイテムタグを更新 | `item_id`, `tags`, `mode?` |
| `item_update_metadata` | アイテムメタデータを更新 | `item_id`, `annotation?`, `star?` |
| `item_delete` | アイテムをゴミ箱に移動 | `item_id` |

### 画像処理

| ツール | 説明 | パラメータ |
|------|------|----------|
| `image_info` | 画像ファイルパスとメタデータを取得 | `item_id` |
| `image_base64` | 画像をbase64データとして取得 | `item_id`, `use_thumbnail?` |
| `image_analyze` | AI解析用に画像をセットアップ | `item_id`, `analysis_prompt`, `use_thumbnail?` |
| `thumbnail_path` | サムネイルファイルパスを取得 | `item_id` |

### ライブラリ管理

| ツール | 説明 | パラメータ |
|------|------|----------|
| `library_info` | Eagleライブラリ情報を取得 | なし |

### Direct APIツール（上級者向け）

> 💡 **注意**: 低レベルEagle APIアクセスには `EXPOSE_DIRECT_API_TOOLS=true` で有効化（追加17ツール）

有効化すると、上級ユーザーと開発者向けにEagleのREST APIエンドポイントへの直接アクセスを提供します。

## 🤖 AI統合

### AIアシスタント用システムプロンプト

AIアシスタントがEagle MCP Serverを効果的に使用できるよう、包括的なシステムプロンプトを提供しています：

- **[完全版システムプロンプト](docs/SYSTEM_PROMPT.jp.md)** - ワークフローとベストプラクティスの詳細ガイド
- **[簡潔版システムプロンプト](docs/SYSTEM_PROMPT_CONCISE.md)** - AI統合用クイックリファレンス（英語）
- **[英語版システムプロンプト](docs/SYSTEM_PROMPT.md)** - Complete English system prompt

これらのプロンプトには以下が含まれます：
- 33ツールの使用パターンとワークフロー
- 効率的な操作のためのベストプラクティス
- エラーハンドリングとユーザーインタラクションガイドライン
- レスポンス形式の推奨事項
- パフォーマンス最適化のヒント

### 統合例

```python
# 例: Eagle MCP Serverを使用するAIアシスタント
from mcp import ClientSession

# 1. 常にヘルスチェックから開始
await session.call_tool("health_check")

# 2. コンテンツ構造を発見
library = await session.call_tool("library_info")
folders = await session.call_tool("folder_list")

# 3. 検索と分析
items = await session.call_tool("item_search", {"keyword": "デザイン", "limit": 10})
image_data = await session.call_tool("image_base64", {"item_id": "abc123", "use_thumbnail": true})
```

## 📁 プロジェクト構造

```
eagle-mcp-server/
├── main.py                 # メインMCPサーバー実装
├── run.bat                 # サーバー起動スクリプト（Windows）
├── eagle_client.py         # Eagle APIクライアント
├── config.py              # 設定管理
├── handlers/              # ツールハンドラー
│   ├── base.py            # ベースハンドラークラス
│   ├── folder.py          # フォルダ操作（6ツール）
│   ├── item.py            # アイテム操作（6ツール）
│   ├── library.py         # ライブラリ操作（1ツール）
│   ├── image.py           # 画像処理（4ツール）
│   └── direct_api.py      # Direct APIアクセス（17ツール）
├── utils/                 # ユーティリティ関数
│   ├── __init__.py
│   └── encoding.py        # テキストエンコーディングユーティリティ
├── schemas/               # Pydanticスキーマ
├── tests/                 # 単体テスト
├── debug/                 # デバッグスクリプト
├── docs/                  # ドキュメント
└── scripts/               # セットアップスクリプト
```

## 🧪 テスト

テストスイートを実行：

```bash
uv run python -m pytest tests/
```

基本機能テストを実行：

```bash
# 基本ヘルスチェック
uv run python -c "from eagle_client import EagleClient; import asyncio; asyncio.run(EagleClient().health_check())"

# Direct APIツールを有効にしてテスト
EXPOSE_DIRECT_API_TOOLS=true uv run python debug/simple_test.py

# 包括的テストを実行
uv run python test_v3.py
```

## 🐛 トラブルシューティング

### よくある問題

1. **接続拒否**: Eagle Appが設定されたポート（デフォルト: 41595）で実行されていることを確認
2. **モジュールが見つからない**: Pythonパスと仮想環境のアクティベーションを確認
3. **権限拒否**: 起動スクリプトのファイル権限を確認
4. **日本語テキストの問題**: UTF-8エンコーディングが適切に設定されていることを確認
5. **Direct APIツールが表示されない**: 環境で `EXPOSE_DIRECT_API_TOOLS=true` を設定

詳細な解決策については[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)を参照してください。

## 🤝 貢献

貢献を歓迎します！お気軽にPull Requestを送信してください。大きな変更については、まずissueを開いて変更したい内容について話し合ってください。

### 開発セットアップ

1. リポジトリをフォーク
2. フィーチャーブランチを作成（`git checkout -b feature/amazing-feature`）
3. 開発依存関係をインストール：`uv sync --extra dev`
4. 変更を加える
5. テストを実行：`uv run python -m pytest`
6. 変更をコミット（`git commit -m 'Add amazing feature'`）
7. ブランチにプッシュ（`git push origin feature/amazing-feature`）
8. Pull Requestを開く

## 📄 ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 🔗 関連リンク

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Eagle App](https://eagle.cool/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## 📞 サポート

問題が発生した場合や質問がある場合：

1. [トラブルシューティングガイド](docs/TROUBLESHOOTING.md)を確認
2. [既存のissue](https://github.com/shingo1228/eagle-mcp-server/issues)を検索
3. [新しいissue](https://github.com/shingo1228/eagle-mcp-server/issues/new)を作成

---

**注意**: このプロジェクトにはEagle Appのインストールと実行が必要です。Eagle Appは[eagle.cool](https://eagle.cool/)で入手可能な強力なデジタル資産管理アプリケーションです。