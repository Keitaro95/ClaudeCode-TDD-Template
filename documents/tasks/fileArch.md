# 株主総会支援システム - ファイルアーキテクチャ

## プロジェクト構成の基本方針

- **フロントエンド**: Streamlit (src/app/frontend)
- **バックエンド**: FastAPI (src/app/backend)
- **パッケージ管理**: uv
- **デプロイ**: Azure App Service

---

## ディレクトリ構造

```
cosmo-ir-2026/
├── src/
│   ├── app/
│   │   ├── frontend/              # Streamlit フロントエンド
│   │   │   ├── __init__.py
│   │   │   ├── officer_app.py     # 役員画面メインアプリ
│   │   │   ├── operator_app.py    # オペレータ画面メインアプリ
│   │   │   ├── components/        # UIコンポーネント
│   │   │   │   ├── __init__.py
│   │   │   │   ├── font_slider.py           # 文字サイズ調整スライダー
│   │   │   │   ├── answer_tabs.py           # 要約/詳細タブ
│   │   │   │   ├── mode_toggle.py           # チェック/ダイレクトモード切り替え
│   │   │   │   ├── question_display.py      # 質問表示エリア
│   │   │   │   ├── answer_display.py        # 回答表示エリア
│   │   │   │   ├── speech_recognition.py    # 音声認識エリア
│   │   │   │   ├── memo_input.py            # メモ・質問入力エリア
│   │   │   │   ├── answer_length_control.py # 回答レベル文字数設定
│   │   │   │   └── answer_editor.py         # 回答確認・編集エリア
│   │   │   ├── services/          # フロントエンド用サービス層
│   │   │   │   ├── __init__.py
│   │   │   │   ├── api_client.py            # バックエンドAPI呼び出し
│   │   │   │   └── sse_client.py            # SSE接続管理
│   │   │   ├── utils/             # フロントエンド用ユーティリティ
│   │   │   │   ├── __init__.py
│   │   │   │   ├── session_state.py         # Streamlit session_state管理
│   │   │   │   └── local_storage.py         # ブラウザlocalStorage連携
│   │   │   └── config.py          # フロントエンド設定
│   │   │
│   │   └── backend/               # FastAPI バックエンド
│   │       ├── __init__.py
│   │       ├── main.py            # FastAPIアプリケーションエントリポイント
│   │       ├── api/               # APIエンドポイント
│   │       │   ├── __init__.py
│   │       │   ├── v1/
│   │       │   │   ├── __init__.py
│   │       │   │   ├── answer.py            # 回答生成エンドポイント
│   │       │   │   ├── speech.py            # 音声認識エンドポイント
│   │       │   │   ├── session.py           # セッション管理エンドポイント
│   │       │   │   ├── qa_history.py        # 質疑応答履歴エンドポイント
│   │       │   │   └── stream.py            # SSEストリーミングエンドポイント
│   │       │   └── dependencies.py          # 依存性注入
│   │       ├── core/              # コア機能
│   │       │   ├── __init__.py
│   │       │   ├── config.py                # バックエンド設定
│   │       │   ├── logging.py               # ロギング設定
│   │       │   └── security.py              # 認証・認可（将来実装）
│   │       ├── services/          # ビジネスロジック層
│   │       │   ├── __init__.py
│   │       │   ├── llm_service.py           # LLM回答生成サービス
│   │       │   ├── vector_search_service.py # ベクトルDB検索サービス
│   │       │   ├── rerank_service.py        # Rerankサービス
│   │       │   ├── speech_service.py        # Azure Speech Service連携
│   │       │   ├── embedding_service.py     # Embedding生成サービス
│   │       │   └── sse_service.py           # SSEブロードキャストサービス
│   │       ├── models/            # データモデル（Pydantic）
│   │       │   ├── __init__.py
│   │       │   ├── answer.py                # 回答モデル
│   │       │   ├── question.py              # 質問モデル
│   │       │   ├── session.py               # セッションモデル
│   │       │   ├── qa_pair.py               # 想定問答モデル
│   │       │   └── user.py                  # ユーザーモデル（将来実装）
│   │       ├── repositories/      # データアクセス層
│   │       │   ├── __init__.py
│   │       │   ├── cosmos_db.py             # Cosmos DB接続・操作
│   │       │   ├── blob_storage.py          # Blob Storage操作
│   │       │   ├── qa_pair_repository.py    # 想定問答CRUD
│   │       │   ├── session_repository.py    # セッションCRUD
│   │       │   └── qa_history_repository.py # 質疑応答履歴CRUD
│   │       ├── utils/             # バックエンド用ユーティリティ
│   │       │   ├── __init__.py
│   │       │   ├── prompt_builder.py        # プロンプト構築
│   │       │   └── error_handlers.py        # エラーハンドリング
│   │       └── schemas/           # レスポンススキーマ（OpenAPI用）
│   │           ├── __init__.py
│   │           ├── answer_schema.py
│   │           ├── question_schema.py
│   │           └── session_schema.py
│   │
│   └── shared/                    # フロントエンド・バックエンド共通モジュール
│       ├── __init__.py
│       ├── constants.py           # 定数定義
│       └── types.py               # 共通型定義
│
├── tests/                         # テストコード
│   ├── __init__.py
│   ├── frontend/                  # フロントエンドテスト
│   │   └── test_components.py
│   └── backend/                   # バックエンドテスト
│       ├── test_api/
│       │   ├── test_answer.py
│       │   └── test_session.py
│       ├── test_services/
│       │   ├── test_llm_service.py
│       │   └── test_vector_search_service.py
│       └── test_repositories/
│           └── test_cosmos_db.py
│
├── scripts/                       # ユーティリティスクリプト
│   ├── setup_azure_resources.py  # Azureリソース初期化
│   ├── seed_qa_pairs.py           # 想定問答データのシード
│   ├── batch_embedding.py         # バッチEmbedding処理
│   └── migrate_db.py              # データベースマイグレーション
│
├── docs/                          # ドキュメント
│   ├── api/                       # API仕様書（OpenAPI）
│   ├── architecture/              # アーキテクチャ設計書
│   └── operation/                 # 運用手順書
│
├── .github/                       # GitHub Actions設定
│   └── workflows/
│       ├── ci.yml                 # CI（テスト・ビルド）
│       └── deploy.yml             # デプロイ（Azure App Service）
│
├── .env.example                   # 環境変数サンプル
├── .gitignore
├── pyproject.toml                 # uv設定・依存関係
├── uv.lock                        # uvロックファイル
└── README.md                      # プロジェクト概要

```

---

## 主要モジュールの責務

### フロントエンド (src/app/frontend)

| モジュール | 責務 |
|----------|------|
| **officer_app.py** | 役員画面のメインアプリ。質問・回答の表示、文字サイズ調整、回答モード選択 |
| **operator_app.py** | オペレータ画面のメインアプリ。音声認識、質問編集、回答生成・送信 |
| **components/** | 再利用可能なUIコンポーネント（スライダー、タブ、トグルスイッチ等） |
| **services/api_client.py** | バックエンドAPIへのHTTPリクエスト（回答生成、セッション管理等） |
| **services/sse_client.py** | SSE接続の管理とイベント受信 |
| **utils/session_state.py** | Streamlitのsession_stateを抽象化し、状態管理を簡素化 |
| **utils/local_storage.py** | ブラウザのlocalStorageとの連携（文字サイズ保存等） |

### バックエンド (src/app/backend)

| モジュール | 責務 |
|----------|------|
| **main.py** | FastAPIアプリケーションの初期化、ミドルウェア設定、ルーター登録 |
| **api/v1/** | REST APIエンドポイントの定義（回答生成、音声認識、SSEストリーム等） |
| **services/llm_service.py** | Claude Sonnet 4.5 APIを使った回答生成ロジック |
| **services/vector_search_service.py** | Cosmos DBベクトル検索（想定問答の検索） |
| **services/rerank_service.py** | 検索結果のRerank（Cohere Rerank等） |
| **services/speech_service.py** | Azure Speech Serviceとの連携（リアルタイム音声認識） |
| **services/embedding_service.py** | 質問文のEmbedding生成（OpenAI text-embedding-3-large） |
| **services/sse_service.py** | SSEでのブロードキャスト管理（複数役員画面への配信） |
| **repositories/** | Cosmos DB、Blob Storageへのデータアクセス層（CRUD操作） |
| **models/** | Pydanticモデル（リクエスト・レスポンスの型定義） |
| **schemas/** | OpenAPI用のレスポンススキーマ |

### 共通 (src/shared)

| モジュール | 責務 |
|----------|------|
| **constants.py** | システム全体で使用する定数（回答モード、デフォルト文字数等） |
| **types.py** | フロントエンド・バックエンドで共通の型定義 |

---

## 主要なデータフロー

### 1. 回答生成フロー（チェックモード）

```
[オペレータ画面 (operator_app.py)]
  ↓ (回答生成ボタンクリック)
[api_client.py] POST /api/v1/answer/generate
  ↓
[Backend: api/v1/answer.py]
  ↓
[llm_service.py]
  ├─ [embedding_service.py] 質問文をEmbedding化
  ├─ [vector_search_service.py] ベクトルDB検索（上位5件）
  ├─ [rerank_service.py] Rerankで上位3件に絞り込み
  ├─ [prompt_builder.py] プロンプト構築
  └─ Claude Sonnet 4.5 API呼び出し
  ↓
[オペレータ画面] 回答確認・編集
  ↓ (回答送信ボタンクリック)
[api_client.py] POST /api/v1/answer/send
  ↓
[Backend: sse_service.py] SSEで全役員画面にブロードキャスト
  ↓
[役員画面 (officer_app.py)] 質問・回答を表示
```

### 2. リアルタイム音声認識フロー

```
[株主の音声]
  ↓
[Azure Speech Service] リアルタイム認識
  ↓ (WebSocket接続)
[Backend: speech_service.py] 認識結果を受信
  ↓
[オペレータ画面 (operator_app.py)] 音声認識エリアに表示
```

### 3. SSE同期フロー

```
[役員画面 (officer_app.py)]
  ↓ (起動時)
[sse_client.py] GET /api/v1/stream/officer/{session_id}
  ↓ (SSE接続確立)
[Backend: api/v1/stream.py]
  ↓ (オペレータが回答送信)
[sse_service.py] イベントをブロードキャスト
  ↓
[全役員画面] 質問・回答を同時更新
```

---

## 技術スタック詳細

### フロントエンド

| 技術 | 用途 |
|------|------|
| **Streamlit** | UIフレームワーク |
| **st.session_state** | クライアントサイド状態管理 |
| **requests** | バックエンドAPI呼び出し |
| **sseclient-py** | SSE接続管理 |

### バックエンド

| 技術 | 用途 |
|------|------|
| **FastAPI** | REST APIフレームワーク |
| **Pydantic** | データバリデーション |
| **uvicorn** | ASGIサーバー |
| **azure-cosmos** | Cosmos DB接続 |
| **azure-storage-blob** | Blob Storage接続 |
| **azure-cognitiveservices-speech** | Azure Speech Service連携 |
| **anthropic** | Claude API（Claude Sonnet 4.5） |
| **openai** | Embedding API（text-embedding-3-large） |
| **cohere** | Rerank API（オプション） |
| **sse-starlette** | SSEサポート |

### 共通

| 技術 | 用途 |
|------|------|
| **uv** | パッケージ管理・実行環境 |
| **pytest** | テストフレームワーク |
| **black** | コードフォーマット（uv fmt経由） |
| **mypy** | 型チェック（オプション） |

---

## 環境変数

`.env`ファイルまたはAzure App Serviceの環境変数で設定:

```bash
# Azure
AZURE_COSMOS_DB_ENDPOINT=https://<your-account>.documents.azure.com:443/
AZURE_COSMOS_DB_KEY=<your-key>
AZURE_BLOB_STORAGE_CONNECTION_STRING=<connection-string>
AZURE_SPEECH_SERVICE_KEY=<key>
AZURE_SPEECH_SERVICE_REGION=japaneast

# Claude API
ANTHROPIC_API_KEY=<your-claude-api-key>

# OpenAI (Embedding)
OPENAI_API_KEY=<your-openai-api-key>

# Cohere (Rerank)
COHERE_API_KEY=<your-cohere-api-key>

# Backend
BACKEND_URL=http://localhost:8000  # ローカル開発時
# BACKEND_URL=https://<your-app>.azurewebsites.net  # 本番環境

# Session
SESSION_SECRET_KEY=<random-secret-key>
```

---

## デプロイ構成

### 開発環境

```
[ローカルPC]
  - Frontend: uv run streamlit run src/app/frontend/officer_app.py (ポート8501)
  - Backend: uv run uvicorn src.app.backend.main:app --reload (ポート8000)
```

### 本番環境（Azure App Service）

```
[Azure App Service (Frontend)]
  - Streamlit アプリ
  - URL: https://<app-name>-frontend.azurewebsites.net

[Azure App Service (Backend)]
  - FastAPI アプリ
  - URL: https://<app-name>-backend.azurewebsites.net

[Azure Cosmos DB]
  - 想定問答、セッション、質疑応答履歴

[Azure Blob Storage]
  - 音声ファイル保存

[Azure Speech Service]
  - リアルタイム音声認識
```

---

## CI/CD

### GitHub Actions ワークフロー

#### CI（.github/workflows/ci.yml）

- トリガー: Pull Request、main/devブランチへのpush
- 実行内容:
  - uvでの依存関係インストール
  - コードフォーマットチェック（uv fmt --check）
  - 型チェック（mypy、オプション）
  - 単体テスト実行（pytest）

#### CD（.github/workflows/deploy.yml）

- トリガー: mainブランチへのマージ
- 実行内容:
  - Azureへのログイン
  - Frontend（Streamlit）のAzure App Serviceへのデプロイ
  - Backend（FastAPI）のAzure App Serviceへのデプロイ

---

## 開発ワークフロー

### 1. ローカル開発

```bash
# 依存関係インストール
uv sync

# バックエンド起動
uv run uvicorn src.app.backend.main:app --reload --port 8000

# フロントエンド起動（別ターミナル）
# 役員画面
uv run streamlit run src/app/frontend/officer_app.py --server.port 8501

# オペレータ画面
uv run streamlit run src/app/frontend/operator_app.py --server.port 8502
```

### 2. テスト実行

```bash
# 全テスト実行
uv run pytest

# カバレッジ計測
uv run pytest --cov=src --cov-report=html
```

### 3. コードフォーマット

```bash
# フォーマット適用
uv fmt

# フォーマットチェックのみ
uv fmt --check
```

---

## セキュリティ考慮事項

| 項目 | 対策 |
|------|------|
| **APIキー管理** | 環境変数で管理、ハードコード禁止 |
| **認証** | Azure AD（将来実装）、開発時は簡易認証 |
| **HTTPS** | 本番環境では必須（Azure App Serviceでデフォルト有効） |
| **CORS** | FastAPIでCORS設定（許可するオリジンを明示） |
| **入力検証** | Pydanticモデルで全入力をバリデーション |
| **ログ** | 機密情報（APIキー、個人情報）をログに出力しない |

---

## パフォーマンス最適化

| 項目 | 対策 |
|------|------|
| **Streamlit** | `@st.cache_data`で重い計算やデータロードをキャッシュ |
| **FastAPI** | 非同期処理（async/await）を活用 |
| **ベクトル検索** | Cosmos DBのベクトルインデックスを最適化 |
| **LLM呼び出し** | タイムアウト設定（15秒）、リトライ機構 |
| **SSE** | 接続プールの管理、定期的なハートビート |

---

## 今後の拡張性

### Phase 2（将来実装）

- **ユーザー管理機能**: 管理者・オペレータ・閲覧者の権限管理
- **事前準備サポートツール**: 想定問答の一括登録・編集UI
- **管理画面**: システム設定、ログ閲覧、ユーザー管理
- **アクセシビリティ対応**: WCAG 2.1 Level AA準拠
- **多言語対応**: 英語・日本語の切り替え

### Phase 3（将来実装）

- **AIによる自動学習**: 過去の質疑応答から想定問答を自動生成
- **リアルタイム分析**: 株主総会の進行状況をダッシュボード表示
- **モバイルアプリ**: ネイティブアプリでの提供

---

## 関連ドキュメント

- [requirements.md](../requirements.md) - 要件定義書
- [CLAUDE.md](../../CLAUDE.md) - プロジェクト基本情報・開発規約

---

**Copyright © MILIZE Inc. ALL rights reserved**

**機密区分: Confidential**
