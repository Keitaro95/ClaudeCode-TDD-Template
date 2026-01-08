****# プロトタイプ タスクリスト

## セットアップ

- [ ] pyproject.toml作成（uv init）
- [ ] 必要な依存関係追加（streamlit, fastapi, uvicorn, sse-starlette）
- [ ] .env.example作成
- [ ] .gitignore作成

## ディレクトリ・ファイル作成

- [ ] src/frontend/ディレクトリ作成
- [ ] src/backend/ディレクトリ作成
- [ ] src/backend/api/ディレクトリ作成
- [ ] src/backend/services/ディレクトリ作成

## バックエンド実装

### FastAPI基本

- [ ] src/backend/main.py実装（FastAPIアプリ初期化、CORS設定、ルーター登録）
- [ ] src/backend/api/speech.py実装（POST /api/speech/recognize エンドポイント）
- [ ] src/backend/api/rag.py実装（POST /api/rag/answer エンドポイント）
- [ ] src/backend/api/stream.py実装（GET /api/stream/officer SSEエンドポイント）

### サービス層

- [ ] src/backend/services/speech_service.py実装（Mock音声認識結果返却）
- [ ] src/backend/services/rag_service.py実装（Mock RAG回答返却：要約・詳細）

## フロントエンド実装

### オペレータ画面

- [ ] src/frontend/operator_app.py作成（基本レイアウト）
- [ ] サイドバー実装（要約の文字数設定、詳細の文字数設定、設定適用ボタン）
- [ ] 音声認識エリア実装（開始/停止ボタン、文字起こし表示）
- [ ] 質問入力エリア実装（textbox）
- [ ] 回答生成ボタン実装（/api/rag/answer呼び出し）
- [ ] 回答表示エリア実装（要約/詳細切り替え、textbox）
- [ ] 回答送信ボタン実装（/api/stream/officer へデータ送信）

### 役員画面

- [ ] src/frontend/officer_app.py作成（基本レイアウト）
- [ ] 文字サイズ調整実装（-文字/+文字ボタン、session_stateで管理）
- [ ] 質問表示エリア実装（textbox、SSEで更新）
- [ ] 回答表示エリア実装（タブ：要約/詳細、SSEで更新）
- [ ] SSE接続実装（/api/stream/officer からイベント受信、session_state更新）

## 動作確認

- [ ] バックエンド起動確認（uvicorn）
- [ ] オペレータ画面起動確認（streamlit）
- [ ] 役員画面起動確認（streamlit）
- [ ] 音声認識フロー確認（Mock データ）
- [ ] RAG回答生成フロー確認（Mock データ）
- [ ] SSE配信フロー確認（オペレータ→役員画面）

## ドキュメント

- [ ] README.md更新（起動方法、環境変数設定方法）
