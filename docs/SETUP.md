# Eagle MCP Server セットアップガイド

## 📋 前提条件

- Python 3.11 以上
- uv パッケージマネージャー
- Eagle アプリケーション (http://localhost:41595 で動作)

## 🚀 インストール

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd eagle-mcp-server
```

### 2. 依存関係のインストール

```bash
uv sync
```

### 3. 環境設定

#### 環境変数ファイルの作成

```bash
# .env.local ファイルを作成
cp .env.example .env.local
```

#### .env.local の編集

```bash
# Windows の場合
EAGLE_API_URL=http://localhost:41595
USER_DATA_DIR=C:\Users\{username}\AppData\Local\eagle-mcp-server
CLAUDE_DESKTOP_CONFIG_PATH=C:\Users\{username}\AppData\Roaming\Claude\claude_desktop_config.json
LM_STUDIO_CONFIG_PATH=C:\Users\{username}\.cache\lm-studio\mcp.json
LM_STUDIO_CONVERSATIONS_DIR=C:\Users\{username}\.cache\lm-studio\conversations
```

### 4. 動作確認

```bash
# 基本動作テスト
uv run python simple_test.py

# MCP サーバー起動
uv run main.py
```

## 🔧 Claude Desktop 統合

### 1. 設定ファイルの編集

Claude Desktop の設定ファイルを編集します：

```json
{
  "mcpServers": {
    "eagle-mcp-server": {
      "command": "path/to/eagle-mcp-server/run.bat"
    }
  }
}
```

### 2. Claude Desktop の再起動

設定を反映するため、Claude Desktop を再起動してください。

## 🛠️ LM Studio 統合

### 1. MCP設定ファイルの編集

LM Studio の MCP設定ファイルを編集します：

```json
{
  "mcpServers": {
    "eagle-mcp-server": {
      "command": "path/to/eagle-mcp-server/run.bat"
    }
  }
}
```

### 2. LM Studio の再起動

設定を反映するため、LM Studio を再起動してください。

## 🎯 使用可能なツール

- **health_check**: Eagle API 接続状態確認
- **folder_list**: フォルダリスト取得
- **folder_search**: フォルダ名検索
- **folder_info**: フォルダ詳細情報
- **item_search**: アイテム検索
- **item_info**: アイテム詳細情報
- **library_info**: ライブラリ情報取得

## 🔍 トラブルシューティング

### Eagle API 接続エラー

1. Eagle アプリケーションが起動しているか確認
2. http://localhost:41595 にアクセス可能か確認
3. .env.local の EAGLE_API_URL 設定を確認

### MCP サーバー起動エラー

1. Python 3.11 以上がインストールされているか確認
2. uv sync が正常に完了しているか確認
3. 必要なディレクトリが作成されているか確認

詳細なトラブルシューティングは [TROUBLESHOOTING.md](TROUBLESHOOTING.md) をご確認ください。