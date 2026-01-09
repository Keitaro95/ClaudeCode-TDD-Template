# プロトタイプ タスクリスト

## セットアップ

- [ ] pyproject.toml作成（uv init）
- [ ] 必要な依存関係追加（streamlit, fastapi, uvicorn, sse-starlette）
- [ ] .env.example作成
- [ ] .gitignore作成

## ディレクトリ・ファイル作成

- [ ] src/frontend/app/pages/ディレクトリ作成
- [ ] src/backend/ディレクトリ作成
- [ ] src/backend/services/ディレクトリ作成

## バックエンド実装

### FastAPI基本

- [ ] src/backend/main.py実装（FastAPIアプリ初期化、CORS設定）

### サービス層（services/）

- [ ] src/backend/services/speech.py実装（POST /speech/recognize エンドポイント + Mock実装）
- [ ] src/backend/services/rag.py実装（POST /rag/answer エンドポイント + Mock実装）
- [ ] src/backend/services/stream.py実装（POST /stream/broadcast エンドポイント + GET /stream/officer SSEエンドポイント）

## フロントエンド実装

### オペレータ画面

- [ ] src/frontend/app/pages/operator_app.py作成（基本レイアウト）
- [ ] サイドバー実装（要約の文字数設定、詳細の文字数設定、設定適用ボタン）
- [ ] 音声認識エリア実装（開始/停止ボタン、文字起こし表示、POST /speech/recognize呼び出し）
- [ ] 質問入力エリア実装（textbox、音声認識結果を自動反映）
- [ ] 回答生成ボタン実装（POST /rag/answer呼び出し）
- [ ] 回答表示エリア実装（要約/詳細切り替えタブ、textbox）
- [ ] 回答送信ボタン実装（POST /stream/broadcast へデータ送信）

### 役員画面

- [ ] src/frontend/app/pages/officer_app.py作成（基本レイアウト）
- [ ] 文字サイズ調整実装（-文字/+文字ボタン、session_stateで管理、16px-48px、デフォルト24px）
- [ ] 質問表示エリア実装（textbox読み取り専用、SSEで更新）
- [ ] 回答表示エリア実装（タブ：要約/詳細、textbox読み取り専用、SSEで更新）
- [ ] SSE接続実装（GET /stream/officer からイベント受信、session_state更新、自動再描画）

## 動作確認

- [ ] バックエンド起動確認（uvicorn src.backend.main:app --reload --port 8000）
- [ ] フロントエンド起動確認（streamlit run src/frontend/app/pages/operator_app.py --server.port 8501）
- [ ] オペレータ画面アクセス確認（http://localhost:8501）
- [ ] 役員画面アクセス確認（http://localhost:8501/officer_app）
- [ ] シナリオ1：音声認識 → 回答生成 → 配信フロー確認
- [ ] シナリオ2：役員画面の文字サイズ調整確認
- [ ] シナリオ3：役員画面の要約・詳細切り替え確認

## ドキュメント

- [ ] README.md更新（起動方法、アクセスURL、環境変数設定方法）
