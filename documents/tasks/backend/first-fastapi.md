# FastAPIバックエンド初期構築タスク

## 概要

株主総会支援システムのFastAPIバックエンドを構築します。
本タスクでは、基本的なプロジェクト構造の作成、必要な依存パッケージのインストール、および基本的なAPIエンドポイントの実装を行います。

**⚠️ 重要: スタブデータの使用**

**このタスクでは、Azure API（Cosmos DB、Blob Storage、Speech Service）やLLM API（Claude、OpenAI、Cohere）は使用せず、すべてスタブデータで動作確認を行います。**

- データベース操作はメモリ内の配列で実装
- LLM回答生成はモックレスポンスで実装
- 音声認識はダミーデータで実装
- 実際のAPI統合は別タスク（[db-api-stub.md](db-api-stub.md)）で実施

これにより、APIキーやAzureリソースなしでも開発・テストが可能です。

**参考ドキュメント:**
- [fileArch.md](../../fileArch.md) - ファイルアーキテクチャ
- [requirements.md](../../requirements.md) - 要件定義書
- [db-api-stub.md](db-api-stub.md) - DB・API統合タスク（次フェーズ）

---

## 前提条件

- Python 3.11以上がインストール済み
- uvがインストール済み
- プロジェクトルートディレクトリ: `/Users/keitarosasaki/Documents/cosmo-ir-2026/`

---

## タスク一覧

### Phase 1: プロジェクト初期化

#### 1.1 ディレクトリ構造の作成

以下のディレクトリ構造を作成する:

```
src/
├── app/
│   └── backend/
│       ├── __init__.py
│       ├── main.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── v1/
│       │   │   ├── __init__.py
│       │   │   ├── answer.py
│       │   │   ├── speech.py
│       │   │   ├── session.py
│       │   │   ├── qa_history.py
│       │   │   └── stream.py
│       │   └── dependencies.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   ├── logging.py
│       │   └── security.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── llm_service.py
│       │   ├── vector_search_service.py
│       │   ├── rerank_service.py
│       │   ├── speech_service.py
│       │   ├── embedding_service.py
│       │   └── sse_service.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── answer.py
│       │   ├── question.py
│       │   ├── session.py
│       │   ├── qa_pair.py
│       │   └── user.py
│       ├── repositories/
│       │   ├── __init__.py
│       │   ├── cosmos_db.py
│       │   ├── blob_storage.py
│       │   ├── qa_pair_repository.py
│       │   ├── session_repository.py
│       │   └── qa_history_repository.py
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── prompt_builder.py
│       │   └── error_handlers.py
│       └── schemas/
│           ├── __init__.py
│           ├── answer_schema.py
│           ├── question_schema.py
│           └── session_schema.py
└── shared/
    ├── __init__.py
    ├── constants.py
    └── types.py
```

**実装コマンド:**
```bash
cd /Users/keitarosasaki/Documents/cosmo-ir-2026
mkdir -p src/app/backend/{api/v1,core,services,models,repositories,utils,schemas}
mkdir -p src/shared
touch src/app/backend/__init__.py
touch src/app/backend/main.py
touch src/app/backend/api/{__init__.py,dependencies.py}
touch src/app/backend/api/v1/{__init__.py,answer.py,speech.py,session.py,qa_history.py,stream.py}
touch src/app/backend/core/{__init__.py,config.py,logging.py,security.py}
touch src/app/backend/services/{__init__.py,llm_service.py,vector_search_service.py,rerank_service.py,speech_service.py,embedding_service.py,sse_service.py}
touch src/app/backend/models/{__init__.py,answer.py,question.py,session.py,qa_pair.py,user.py}
touch src/app/backend/repositories/{__init__.py,cosmos_db.py,blob_storage.py,qa_pair_repository.py,session_repository.py,qa_history_repository.py}
touch src/app/backend/utils/{__init__.py,prompt_builder.py,error_handlers.py}
touch src/app/backend/schemas/{__init__.py,answer_schema.py,question_schema.py,session_schema.py}
touch src/shared/{__init__.py,constants.py,types.py}
```

#### 1.2 必要パッケージのインストール

**基本パッケージ（必須）:**
```bash
uv add fastapi uvicorn[standard] pydantic pydantic-settings
uv add sse-starlette python-multipart python-dotenv
```

**⚠️ Azure/LLM APIパッケージは今は不要（スタブモード）**

以下のパッケージは別タスク（[db-api-stub.md](db-api-stub.md)）で実際のAPI統合時に追加します:
```bash
# 今はインストール不要
# uv add azure-cosmos azure-storage-blob azure-cognitiveservices-speech
# uv add anthropic openai cohere
```

**開発用パッケージ:**
```bash
uv add --dev pytest pytest-asyncio httpx
```

---

### Phase 2: 基本設定ファイルの実装

#### 2.1 環境変数設定 (.env.example)

プロジェクトルートに `.env.example` を作成:

```bash
# ⚠️ このフェーズでは以下のAPIキーは不要です（スタブデータを使用）
# Azure
# AZURE_COSMOS_DB_ENDPOINT=https://<your-account>.documents.azure.com:443/
# AZURE_COSMOS_DB_KEY=<your-key>
# AZURE_BLOB_STORAGE_CONNECTION_STRING=<connection-string>
# AZURE_SPEECH_SERVICE_KEY=<key>
# AZURE_SPEECH_SERVICE_REGION=japaneast

# Claude API
# ANTHROPIC_API_KEY=<your-claude-api-key>

# OpenAI (Embedding)
# OPENAI_API_KEY=<your-openai-api-key>

# Cohere (Rerank)
# COHERE_API_KEY=<your-cohere-api-key>

# Backend（この設定のみ必要）
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
BACKEND_RELOAD=true

# Session
SESSION_SECRET_KEY=your-development-secret-key-change-in-production

# CORS
CORS_ORIGINS=["http://localhost:8501", "http://localhost:8502"]
```

#### 2.2 コア設定モジュール (src/app/backend/core/config.py)

Pydantic Settingsを使った設定管理（**スタブモード用に簡素化**）:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        # APIキーがなくてもエラーにならないようにする
        extra="ignore"
    )

    # ⚠️ このフェーズではAzure/LLM APIキーは使用しない（スタブデータ使用）
    # Azure（オプショナル - 今は不要）
    azure_cosmos_db_endpoint: Optional[str] = None
    azure_cosmos_db_key: Optional[str] = None
    azure_blob_storage_connection_string: Optional[str] = None
    azure_speech_service_key: Optional[str] = None
    azure_speech_service_region: str = "japaneast"

    # Claude API（オプショナル - 今は不要）
    anthropic_api_key: Optional[str] = None

    # OpenAI（オプショナル - 今は不要）
    openai_api_key: Optional[str] = None

    # Cohere（オプショナル - 今は不要）
    cohere_api_key: Optional[str] = None

    # Backend（必須）
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    backend_reload: bool = True

    # Session（必須）
    session_secret_key: str = "your-development-secret-key-change-in-production"

    # CORS（必須）
    cors_origins: List[str] = ["http://localhost:8501", "http://localhost:8502"]

    # LLM Settings（スタブモード用のデフォルト値）
    claude_model: str = "claude-sonnet-4-5-20250929"
    embedding_model: str = "text-embedding-3-large"
    embedding_dimension: int = 3072

    # Timeout
    llm_timeout: int = 15
    vector_search_top_k: int = 5
    rerank_top_k: int = 3


settings = Settings()
```

#### 2.3 ロギング設定 (src/app/backend/core/logging.py)

構造化ログの設定:

```python
import logging
import sys
from typing import Any


def setup_logging() -> None:
    """ロギングの初期設定"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def get_logger(name: str) -> logging.Logger:
    """ロガーの取得"""
    return logging.getLogger(name)
```

---

### Phase 3: データモデルの実装

#### 3.1 共通型定義 (src/shared/constants.py)

```python
"""システム全体で使用する定数"""

# 回答モード
RESPONSE_MODE_CHECK = "check"
RESPONSE_MODE_DIRECT = "direct"

# 回答レベル
ANSWER_LEVEL_SUMMARY = "summary"
ANSWER_LEVEL_DETAIL = "detail"

# デフォルト文字数
DEFAULT_SUMMARY_LENGTH = 100
DEFAULT_DETAIL_LENGTH = 1000

# 文字数調整範囲
SUMMARY_LENGTH_MIN = 50
SUMMARY_LENGTH_MAX = 300
DETAIL_LENGTH_MIN = 500
DETAIL_LENGTH_MAX = 2000

# 文字数調整単位
SUMMARY_LENGTH_STEP = 50
DETAIL_LENGTH_STEP = 250
```

#### 3.2 質問モデル (src/app/backend/models/question.py)

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Question(BaseModel):
    """質問モデル"""
    id: Optional[str] = None
    session_id: str
    question_text: str = Field(..., min_length=1, max_length=2000)
    memo: Optional[str] = Field(None, max_length=2000)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class QuestionCreate(BaseModel):
    """質問作成リクエスト"""
    session_id: str
    question_text: str = Field(..., min_length=1, max_length=2000)
    memo: Optional[str] = Field(None, max_length=2000)
```

#### 3.3 回答モデル (src/app/backend/models/answer.py)

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Answer(BaseModel):
    """回答モデル"""
    id: Optional[str] = None
    question_id: str
    summary: str = Field(..., min_length=1)
    detail: str = Field(..., min_length=1)
    operator_id: Optional[str] = None
    response_mode: str  # check or direct
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AnswerGenerate(BaseModel):
    """回答生成リクエスト"""
    question_text: str = Field(..., min_length=1, max_length=2000)
    summary_length: int = Field(default=100, ge=50, le=300)
    detail_length: int = Field(default=1000, ge=500, le=2000)
    session_id: str


class AnswerResponse(BaseModel):
    """回答生成レスポンス"""
    summary: str
    detail: str
    question_text: str
```

#### 3.4 セッションモデル (src/app/backend/models/session.py)

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Session(BaseModel):
    """セッションモデル"""
    id: Optional[str] = None
    session_name: str = Field(..., min_length=1, max_length=200)
    date: datetime
    answer_summary_length: int = Field(default=100, ge=50, le=300)
    answer_detail_length: int = Field(default=1000, ge=500, le=2000)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SessionCreate(BaseModel):
    """セッション作成リクエスト"""
    session_name: str = Field(..., min_length=1, max_length=200)
    date: datetime
    answer_summary_length: int = Field(default=100, ge=50, le=300)
    answer_detail_length: int = Field(default=1000, ge=500, le=2000)
```

---

### Phase 4: FastAPIアプリケーションの基本実装

#### 4.1 メインアプリケーション (src/app/backend/main.py)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.backend.core.config import settings
from src.app.backend.core.logging import setup_logging, get_logger
from src.app.backend.api.v1 import answer, session, stream

# ロギング設定
setup_logging()
logger = get_logger(__name__)

# FastAPIアプリケーション
app = FastAPI(
    title="株主総会支援システム API",
    description="株主総会当日の質疑応答支援システムのバックエンドAPI",
    version="1.0.0",
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(answer.router, prefix="/api/v1/answer", tags=["answer"])
app.include_router(session.router, prefix="/api/v1/session", tags=["session"])
app.include_router(stream.router, prefix="/api/v1/stream", tags=["stream"])


@app.get("/")
async def root():
    """ヘルスチェック"""
    return {"message": "株主総会支援システム API", "status": "ok"}


@app.get("/health")
async def health():
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.app.backend.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.backend_reload,
    )
```

#### 4.2 セッションエンドポイント (src/app/backend/api/v1/session.py)

```python
from fastapi import APIRouter, HTTPException
from typing import List
from src.app.backend.models.session import Session, SessionCreate
from src.app.backend.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

# ⚠️ スタブデータ: メモリ内配列でDB操作をシミュレート
# 実際のCosmos DB統合は別タスク（db-api-stub.md）で実施
sessions_db: List[Session] = []


@router.post("/", response_model=Session)
async def create_session(session: SessionCreate):
    """
    セッションを作成（スタブ実装）

    ⚠️ メモリ内配列で動作（サーバー再起動でデータ消失）
    実際のCosmos DB統合は別タスクで実施
    """
    try:
        import uuid
        new_session = Session(
            id=str(uuid.uuid4()),
            **session.model_dump()
        )
        sessions_db.append(new_session)
        logger.info(f"[STUB] Session created: {new_session.id}")
        return new_session
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}", response_model=Session)
async def get_session(session_id: str):
    """
    セッションを取得（スタブ実装）

    ⚠️ メモリ内配列から検索
    """
    for session in sessions_db:
        if session.id == session_id:
            logger.info(f"[STUB] Session retrieved: {session_id}")
            return session
    logger.warning(f"[STUB] Session not found: {session_id}")
    raise HTTPException(status_code=404, detail="Session not found")


@router.get("/", response_model=List[Session])
async def list_sessions():
    """
    セッション一覧を取得（スタブ実装）

    ⚠️ メモリ内配列のすべてを返却
    """
    logger.info(f"[STUB] Listing {len(sessions_db)} sessions")
    return sessions_db
```

#### 4.3 回答エンドポイント (src/app/backend/api/v1/answer.py)

```python
from fastapi import APIRouter, HTTPException
from src.app.backend.models.answer import AnswerGenerate, AnswerResponse
from src.app.backend.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/generate", response_model=AnswerResponse)
async def generate_answer(request: AnswerGenerate):
    """
    回答を生成（スタブ実装）

    ⚠️ このフェーズではスタブデータを返します
    実際のLLM統合は別タスク（db-api-stub.md）で実施

    TODO（次フェーズ）:
    - Embedding生成
    - Vector DB検索
    - Rerank
    - Claude Sonnet 4.5 API呼び出し
    """
    try:
        logger.info(f"[STUB] Generating answer for question: {request.question_text[:50]}...")

        # ⚠️ スタブレスポンス（実際のLLMは使用しない）
        summary = f"【スタブ回答】要約（{request.summary_length}文字目安）: 質問「{request.question_text[:30]}...」に対する要約回答です。本番環境では実際のLLMが詳細な回答を生成します。"
        detail = f"【スタブ回答】詳細（{request.detail_length}文字目安）: 質問「{request.question_text[:30]}...」に対する詳細回答です。本番環境では、ベクトルDB検索により関連する想定問答を取得し、Claude Sonnet 4.5が根拠やデータを含めた詳細な回答を生成します。このスタブ実装では、API統合なしで動作確認が可能です。"

        return AnswerResponse(
            summary=summary,
            detail=detail,
            question_text=request.question_text
        )
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

#### 4.4 SSEストリームエンドポイント (src/app/backend/api/v1/stream.py)

```python
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
from src.app.backend.core.logging import get_logger
import asyncio

logger = get_logger(__name__)
router = APIRouter()


@router.get("/officer/{session_id}")
async def stream_officer(session_id: str):
    """
    役員画面用SSEストリーム（スタブ実装）

    ⚠️ このフェーズでは基本的なハートビートのみ実装
    実際のデータ配信は別タスク（db-api-stub.md）で実施

    TODO（次フェーズ）:
    - SSE管理サービスとの連携
    - 質問・回答のブロードキャスト
    - 複数クライアント管理
    """
    async def event_generator():
        try:
            # 接続確認
            logger.info(f"[STUB] SSE connection opened for session {session_id}")
            yield {
                "event": "connected",
                "data": f"Connected to session {session_id}"
            }

            # 定期的なハートビート（スタブ実装）
            while True:
                await asyncio.sleep(30)
                yield {
                    "event": "heartbeat",
                    "data": "ping"
                }
        except asyncio.CancelledError:
            logger.info(f"[STUB] SSE connection closed for session {session_id}")

    return EventSourceResponse(event_generator())
```

---

### Phase 5: 動作確認

#### 5.1 サーバー起動

```bash
cd /Users/keitarosasaki/Documents/cosmo-ir-2026
uv run uvicorn src.app.backend.main:app --reload --port 8000
```

#### 5.2 エンドポイント確認

**ヘルスチェック:**
```bash
curl http://localhost:8000/health
```

**セッション作成:**
```bash
curl -X POST http://localhost:8000/api/v1/session/ \
  -H "Content-Type: application/json" \
  -d '{
    "session_name": "2026年定時株主総会",
    "date": "2026-06-15T10:00:00",
    "answer_summary_length": 100,
    "answer_detail_length": 1000
  }'
```

**回答生成:**
```bash
curl -X POST http://localhost:8000/api/v1/answer/generate \
  -H "Content-Type: application/json" \
  -d '{
    "question_text": "今期の業績見通しについて教えてください",
    "summary_length": 100,
    "detail_length": 1000,
    "session_id": "test-session-id"
  }'
```

**OpenAPI Docs:**
ブラウザで `http://localhost:8000/docs` にアクセスして、自動生成されたAPIドキュメントを確認

---

## 次のステップ

### Phase 6以降のタスク（別途実装）

1. **Azure統合**
   - Cosmos DB接続実装
   - Blob Storage接続実装
   - Azure Speech Service統合

2. **LLM統合**
   - Embedding Service実装
   - Vector Search Service実装
   - Rerank Service実装
   - Claude Sonnet 4.5統合

3. **SSE同期機能**
   - SSE Service実装
   - 複数クライアント管理

4. **テスト実装**
   - 単体テスト
   - 統合テスト

---

## チェックリスト

- [ ] ディレクトリ構造の作成
- [ ] 必要パッケージのインストール
- [ ] .env.exampleの作成
- [ ] core/config.pyの実装
- [ ] core/logging.pyの実装
- [ ] shared/constants.pyの実装
- [ ] models/question.pyの実装
- [ ] models/answer.pyの実装
- [ ] models/session.pyの実装
- [ ] main.pyの実装
- [ ] api/v1/session.pyの実装
- [ ] api/v1/answer.pyの実装
- [ ] api/v1/stream.pyの実装
- [ ] サーバー起動確認
- [ ] エンドポイント動作確認
- [ ] OpenAPI Docsの確認

---

**Copyright © MILIZE Inc. ALL rights reserved**

**機密区分: Confidential**
