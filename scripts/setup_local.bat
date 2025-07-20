@echo off
echo Eagle MCP Server - 環境セットアップ
echo =====================================

cd /d "%~dp0\.."

echo.
echo 1. 依存関係のインストール...
uv sync
if %errorlevel% neq 0 (
    echo エラー: 依存関係のインストールに失敗しました
    pause
    exit /b 1
)

echo.
echo 2. 環境設定ファイルの作成...
if not exist .env.local (
    copy .env.example .env.local
    echo .env.local ファイルを作成しました
    echo 必要に応じて .env.local を編集してください
) else (
    echo .env.local ファイルは既に存在します
)

echo.
echo 3. 設定テンプレートの確認...
if not exist config.local.json (
    echo config.local.json は存在しません（オプション）
    echo 必要に応じて config.template.json を参考に作成してください
) else (
    echo config.local.json ファイルが存在します
)

echo.
echo 4. 必要ディレクトリの作成...
python -c "from config import config; config.create_directories(); print('ディレクトリを作成しました')"

echo.
echo 5. 動作確認...
echo Eagle アプリケーションが起動していることを確認しています...
uv run python -c "import asyncio; from eagle_client import EagleClient; print('テスト中...'); asyncio.run(EagleClient().health_check())"

echo.
echo セットアップが完了しました！
echo.
echo 次のステップ:
echo   1. .env.local を編集して環境に合わせて調整
echo   2. Eagle アプリケーションを起動
echo   3. run.bat でサーバーを起動
echo   4. Claude Desktop または LM Studio で設定
echo.
pause