# プロトタイプ - ファイル構成（最小限）

## 基本方針

- **ハリウッドの原則**: 必要になったら追加する（Don't call us, we'll call you）
- **proto.mdの骨子に基づいた最小構成**
- **フロントエンド**: Streamlit
- **バックエンド**: FastAPI
- **パッケージ管理**: uv

---

## ディレクトリ構造

```
cosmo-ir-2026/
├── src/
│   ├── frontend/
│   │   └── app/
│   │       ├── main.py                    # エントリーポイント（入り口）
│   │       └── pages/                     # ここに画面ごとのファイルを置く
│   │           ├── 1_operator_app.py      # オペレータ画面
│   │           └── 2_officer_app.py       # 役員画面
│   │
│   └── backend/
│       ├── main.py                        # FastAPI エントリポイント
│       └── services/
│           ├── speech.py                  # 音声認識エンドポイント（Mock）
│           ├── rag.py                     # RAG回答生成エンドポイント（Mock）
│           └── stream.py                  # SSE エンドポイント（役員画面への配信）
│
├── .env.example                    # 環境変数サンプル
├── .gitignore
├── pyproject.toml                  # uv設定・依存関係
└── README.md
```

---

## 主要モジュールの責務

### フロントエンド

| ファイル | 責務 |
|---------|------|
| **main.py** | Streamlitアプリケーションのエントリーポイント |
| **pages/1_operator_app.py** | オペレータ画面（サイドバー：要約・詳細の文字数設定、音声認識ボタン、回答生成ボタン、回答送信ボタン） |
| **pages/2_officer_app.py** | 役員画面（文字サイズ調整（-/+ボタン）、質問表示、要約/詳細タブ表示） |

### バックエンド

| ファイル | 責務 |
|---------|------|
| **main.py** | FastAPIアプリ初期化、サービスルーター登録 |
| **services/speech.py** | `POST /api/speech/recognize` - Mock音声認識結果を返却 |
| **services/rag.py** | `POST /api/rag/answer` - 質問を受け取り、要約・詳細の回答をJSON返却（Mock） |
| **services/stream.py** | `GET /api/stream/officer` - SSE で役員画面に回答を配信 |

---

## データフロー（プロトタイプ）

### 1. 音声認識フロー

```
[オペレータ画面] 開始ボタン押下
  ↓
POST /api/speech/recognize（Mock音声データ送信）
  ↓
[Backend: services/speech.py] Mock音声認識
  ↓ SSE
[オペレータ画面] 文字起こしストリーミング表示
```

### 2. RAG回答生成フロー

```
[オペレータ画面] 回答作成ボタン押下
  ↓
POST /api/rag/answer（質問テキスト送信）
  ↓
[Backend: services/rag.py] Mock回答返却（要約・詳細）
  ↓
[オペレータ画面] 回答textboxに表示
  ↓ 回答送信ボタン押下
  ↓
GET /api/stream/officer（SSE）
  ↓
[役員画面] 質問・回答を表示
```

---

## 技術スタック（最小限）

| 技術 | 用途 |
|------|------|
| **Streamlit** | フロントエンドUI |
| **FastAPI** | REST API |
| **uvicorn** | ASGIサーバー |
| **sse-starlette** | SSE配信 |

---

## 環境変数（最小限）

```bash
# Azure Speech Service（オプション）
AZURE_SPEECH_SERVICE_KEY=<key>
AZURE_SPEECH_SERVICE_REGION=japaneast

# Backend
BACKEND_URL=http://localhost:8000
```

---

## 開発ワークフロー

```bash
# バックエンド起動
uv run uvicorn src.backend.main:app --reload --port 8000

# フロントエンド起動（別ターミナル）
# Streamlitマルチページアプリ（オペレータ画面・役員画面）
uv run streamlit run src/frontend/app/main.py --server.port 8501
```

---

**Copyright © MILIZE Inc. ALL rights reserved**

**機密区分: Confidential**
