# トラブルシューティング

## 🔍 よくある問題と解決方法

### Eagle API 関連

#### 問題: Eagle API に接続できない

**症状:**
- `EagleAPIError: Request failed` エラー
- `health_check` が `False` を返す

**解決方法:**
1. Eagle アプリケーションが起動しているか確認
2. ブラウザで http://localhost:41595 にアクセス
3. Eagle の API が有効になっているか確認
4. ファイアウォールの設定を確認

#### 問題: 文字化けが発生する

**症状:**
- 日本語フォルダ名が正しく表示されない
- Unicode エラーが発生する

**解決方法:**
1. システムの文字エンコーディングを確認
2. 環境変数 `PYTHONIOENCODING=utf-8` を設定
3. コマンドプロンプトで `chcp 65001` を実行

### MCP サーバー関連

#### 問題: MCP サーバーが起動しない

**症状:**
- `ImportError` エラー
- `ModuleNotFoundError` エラー

**解決方法:**
1. 依存関係を再インストール: `uv sync`
2. Python バージョンを確認: `python --version`
3. 仮想環境を確認: `uv run python -c "import sys; print(sys.executable)"`

#### 問題: 設定ファイルが読み込まれない

**症状:**
- デフォルト設定が使用される
- 環境変数が反映されない

**解決方法:**
1. `.env.local` ファイルの存在を確認
2. ファイルの権限を確認
3. 環境変数の構文を確認

### Claude Desktop 統合

#### 問題: Claude Desktop でツールが表示されない

**症状:**
- MCP サーバーが認識されない
- ツールリストが空

**解決方法:**
1. `claude_desktop_config.json` のパスを確認
2. JSON 構文の妥当性を確認
3. Claude Desktop を再起動
4. ログファイルを確認

#### 問題: ツール実行時にエラーが発生する

**症状:**
- `toolCallFailed` エラー
- レスポンスが返らない

**解決方法:**
1. Eagle アプリケーションの起動を確認
2. MCP サーバーのログを確認
3. 手動でツールテストを実行: `uv run python simple_test.py`

### LM Studio 統合

#### 問題: LM Studio でツールが利用できない

**症状:**
- MCP サーバーが認識されない
- 無限ループが発生する

**解決方法:**
1. LM Studio の MCP 設定を確認
2. MCP サーバーのログレベルを DEBUG に設定
3. 会話ログを確認
4. LM Studio を再起動

### パフォーマンス問題

#### 問題: 応答が遅い

**症状:**
- ツール実行に時間がかかる
- タイムアウトエラーが発生する

**解決方法:**
1. Eagle API のタイムアウト設定を調整
2. リクエストの限界値を調整
3. キャッシュディレクトリを確認

## 📋 デバッグ方法

### 1. ログレベルの設定

```bash
# .env.local に追加
LOG_LEVEL=DEBUG
```

### 2. 手動テストの実行

```bash
# 基本動作確認
uv run python simple_test.py

# 設定確認
uv run python -c "from config import config; print(config.to_dict())"
```

### 3. Eagle API の直接テスト

```bash
# ブラウザまたは curl でテスト
curl http://localhost:41595/api/application/info
```

### 4. MCP サーバーのテスト

```bash
# stdio モードで起動
uv run main.py

# バッチファイルで起動
run.bat
```

## 🆘 サポート

問題が解決しない場合は、以下の情報を含めてサポートにお問い合わせください：

1. オペレーティングシステム
2. Python バージョン
3. Eagle アプリケーションのバージョン
4. エラーメッセージの全文
5. 設定ファイルの内容（個人情報を除く）
6. ログファイルの内容

## 🔧 高度なトラブルシューティング

### 環境の完全リセット

```bash
# 仮想環境を削除
rm -rf .venv

# 依存関係を再インストール
uv sync

# 設定ファイルを再作成
cp .env.example .env.local
```

### ログファイルの場所

- Windows: `%LOCALAPPDATA%\eagle-mcp-server-v2\logs\`
- macOS: `~/.local/share/eagle-mcp-server-v2/logs/`
- Linux: `~/.local/share/eagle-mcp-server-v2/logs/`