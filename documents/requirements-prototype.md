# 株主総会支援システム プロトタイプ要件定義書

## 目的

株主総会支援システムのプロトタイプを作成し、以下の基本フローを検証する：

1. オペレータ画面での質問入力・回答生成
2. 役員画面へのリアルタイム配信
3. 要約・詳細の2段階回答の切り替え

---

## システム構成

```
[オペレータ画面 (Streamlit)]  →  [Backend (FastAPI)]  ←  [役員画面 (Streamlit)]
         ↓                              ↓
    [pages/operator_app.py]      [services/]
                                  - speech.py (音声認識 Mock)
                                  - rag.py (RAG Mock + API)
                                  - stream.py (SSE API)
         ↑
    [pages/officer_app.py]
```

## 技術スタック

| レイヤー | 技術 |
|---------|------|
| フロントエンド | Streamlit |
| バックエンド | FastAPI |
| リアルタイム通信 | Server-Sent Events (SSE) |
| 依存関係管理 | uv |

---

## 機能要件

### 1. オペレータ画面

#### 1.1 基本レイアウト

- サイドバー：回答設定エリア
- メインエリア：音声認識、質問入力、回答表示

#### 1.2 回答設定エリア（サイドバー）

- 要約の文字数設定（数値入力、デフォルト: 100）
- 詳細の文字数設定（数値入力、デフォルト: 1000）
- 設定適用ボタン

#### 1.3 音声認識エリア

- 開始/停止ボタン
- 文字起こし表示エリア（textbox）
- **Mock**: ボタンクリックで固定の文字列を返す

#### 1.4 質問入力エリア

- 質問入力textbox
- 音声認識結果を自動で反映（手動編集可能）

#### 1.5 回答生成機能

- 回答生成ボタン
- `/rag/answer` エンドポイント呼び出し
- **Mock**: 要約・詳細の固定文字列を返す
- 回答表示エリア（要約/詳細切り替えタブ、textbox）

#### 1.6 回答送信機能

- 回答送信ボタン
- 質問・要約・詳細を `/stream/broadcast` に送信
- 全役員画面にSSEでブロードキャスト

### 2. 役員画面

#### 2.1 基本レイアウト

- 文字サイズ調整ボタン（-文字 / +文字）
- 質問表示エリア
- 回答表示エリア（要約/詳細タブ）

#### 2.2 文字サイズ調整機能

- -文字ボタン: フォントサイズを小さく
- +文字ボタン: フォントサイズを大きく
- `session_state` で管理（範囲: 16px - 48px、デフォルト: 24px）

#### 2.3 質問表示エリア

- SSEで受信した質問を表示
- textbox（読み取り専用）

#### 2.4 回答表示エリア

- タブUI（要約/詳細）
- SSEで受信した回答を表示
- textbox（読み取り専用）

#### 2.5 SSE接続

- `/stream/officer` からイベント受信
- 受信データで `session_state` を更新
- 自動で画面再描画

### 3. バックエンドAPI

#### 3.1 POST /speech/recognize (services/speech.py)

**リクエスト:**
```json
{
  "audio": "dummy"
}
```

**レスポンス（Mock）:**
```json
{
  "transcript": "株主優待制度の拡充について教えてください。"
}
```

#### 3.2 POST /rag/answer (services/rag.py)

**リクエスト:**
```json
{
  "question": "株主優待制度の拡充について教えてください。",
  "summary_length": 100,
  "detail_length": 1000
}
```

**レスポンス（Mock）:**
```json
{
  "summary": "株主優待制度については現在検討中です。（約100文字）",
  "detail": "株主優待制度については、株主還元施策の一環として検討を進めております。具体的な内容や時期については、取締役会での審議を経て決定し、適切なタイミングで開示いたします。（約1000文字に調整したMock文字列）"
}
```

#### 3.3 POST /stream/broadcast (services/stream.py)

**リクエスト:**
```json
{
  "question": "株主優待制度の拡充について教えてください。",
  "summary": "株主優待制度については現在検討中です。",
  "detail": "株主優待制度については、株主還元施策の一環として..."
}
```

**レスポンス:**
```json
{
  "status": "broadcasted"
}
```

#### 3.4 GET /stream/officer (services/stream.py)

**機能:**
- SSEエンドポイント
- オペレータから送信された質問・回答をブロードキャスト

**イベント形式:**
```
event: update
data: {"question": "...", "summary": "...", "detail": "..."}
```

---

## ディレクトリ構成

```
cosmo-ir-2026/
├── pyproject.toml
├── .env.example
├── .gitignore
├── README.md
├── src/
│   ├── frontend/
│   │   ├── app/
│   │   │   └── pages/
│   │   │       ├── operator_app.py    # オペレータ画面
│   │   │       └── officer_app.py     # 役員画面
│   └── backend/
│       ├── main.py                    # FastAPIアプリ（CORS等の設定のみ）
│       └── services/
│           ├── speech.py              # 音声認識API + Mock実装
│           ├── rag.py                 # RAG API + Mock実装
│           └── stream.py              # SSE API実装
```

---

## 起動方法

### バックエンド起動（1サーバー）

```bash
uv run uvicorn src.backend.main:app --reload --port 8000
```

### フロントエンド起動（Streamlit Multipage App）

```bash
uv run streamlit run src/frontend/app/pages/operator_app.py --server.port 8501
```

Streamlitのマルチページ機能により、以下のURLで各画面にアクセス可能：
- オペレータ画面: `http://localhost:8501`
- 役員画面: `http://localhost:8501/officer_app`

---

## 動作確認シナリオ

### シナリオ1: 音声認識 → 回答生成 → 配信

1. オペレータ画面で「音声認識開始」ボタンをクリック
2. Mock文字列が質問入力エリアに反映される
3. 「回答生成」ボタンをクリック
4. Mock回答（要約・詳細）が表示される
5. 「回答送信」ボタンをクリック
6. 役員画面に質問・回答が即座に表示される

### シナリオ2: 文字サイズ調整

1. 役員画面で「+文字」ボタンをクリック
2. 質問・回答のフォントサイズが大きくなる
3. 「-文字」ボタンで元に戻る

### シナリオ3: 要約・詳細切り替え

1. 役員画面で「要約」タブをクリック
2. 要約回答が表示される
3. 「詳細」タブをクリック
4. 詳細回答が表示される

---

## プロトタイプの制約・割り切り

- 音声認識は固定のMock文字列を返す
- RAG回答も固定のMock文字列を返す
- ベクトルDB、Azure連携は実装しない
- 認証・認可は実装しない
- データベースは使用しない（メモリ内で完結）
- エラーハンドリングは最小限
- レスポンシブデザインは考慮しない

---

## 次フェーズへの移行時に実装する機能

- Azure Speech Service統合
- Claude Sonnet 4.5統合
- Azure Cosmos DB（ベクトルDB）統合
- 認証（Azure AD）
- エラーハンドリング・ログ記録
- レスポンシブデザイン
- パフォーマンス最適化
