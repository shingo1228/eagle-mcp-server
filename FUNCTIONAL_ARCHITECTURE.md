### 機能構成図

```mermaid
graph TD
    subgraph "外部クライアント"
        Client[MCPクライアント<br>e.g. LM Studio, Claude]
    end

    subgraph "Eagle MCP Server (本プロジェクト)"
        Main[<b>main.py</b><br>MCPサーバー本体<br>リクエスト受付・応答]
        Handlers("
            <b>handlers/</b><br>
            <u>抽象化ハンドラー</u><br>
            - FolderHandler<br>
            - ItemHandler<br>
            - LibraryHandler<br>
            - ImageHandler<br>
            <br>
            <u>直接APIハンドラー</u><br>
            - DirectApiHandler
        ")
        EagleClient[<b>eagle_client.py</b><br>Eagle APIとの通信担当]
    end

    subgraph "外部サービス"
        EagleAPI[Eagle App API<br>(localhost:41595)]
    end

    Client -- "1. ツール呼び出し (MCP Request)" --> Main
    Main -- "2. ツール名に基づき<br>担当ハンドラーへ処理を委譲" --> Handlers
    Handlers -- "3. EagleClientの<br>メソッドを呼び出し" --> EagleClient
    EagleClient -- "4. HTTPリクエスト (GET/POST)" --> EagleAPI
    EagleAPI -- "5. JSONレスポンス" --> EagleClient
    EagleClient -- "6. APIの応答を返す" --> Handlers
    Handlers -- "7. 応答を整形し<br>TextContentを作成" --> Main
    Main -- "8. 整形後のデータを<br>クライアントへ返す (MCP Response)" --> Client
```

### 各コンポーネントの説明

1.  **外部クライアント (MCP Client)**
    *   LM StudioやClaude Desktopなど、MCPプロトコルに対応したAIアシスタントクライアントです。
    *   ユーザーの指示に基づき、本サーバーが提供するツールを呼び出します。

2.  **Eagle MCP Server (本プロジェクト)**
    *   **`main.py`**:
        *   プロジェクトの中心となるサーバーアプリケーションです。
        *   クライアントからのツール呼び出しリクエストを受け付け、どのハンドラーが処理すべきかを判断し、処理を委譲します。
        *   最終的にハンドラーから返された結果を、MCPプロトコルに準拠した形式でクライアントに応答します。
    *   **`handlers/` (ハンドラー群)**:
        *   ツールごとの具体的な処理を実装するモジュール群です。
        *   **抽象化ハンドラー**: `folder_list` のように、利用者が使いやすいように設計された、より抽象的なツールを提供します。
        *   **DirectApiHandler**: `api_folder_list` のように、Eagle APIのエンドポイントと1対1で対応する、より低レベルなツールを提供します。
    *   **`eagle_client.py`**:
        *   Eagle App APIとの実際のHTTP通信を担うラッパークラスです。
        *   ハンドラーからの指示に基づき、GETやPOSTリクエストを組み立ててEagle App APIに送信し、返ってきたJSONレスポンスをハンドラーに渡します。

3.  **外部サービス (Eagle App API)**
    *   Eagleアプリケーション本体が提供するローカルAPIサーバーです。
    *   `eagle_client.py` からのHTTPリクエストを受け取り、Eagleライブラリに対する実際の操作（フォルダ作成、アイテム検索など）を実行して、結果をJSON形式で返します。
