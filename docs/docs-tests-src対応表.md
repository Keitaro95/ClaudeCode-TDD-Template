# documents / tests / src 対応表

TDDで開発されたファイルの対応関係。ドキュメント(仕様) → テスト(RED) → 実装(GREEN)の流れで構成。

---

## Backend - Speech API

| Document | Tests | src実装 |
|----------|-------|---------|
| `backend/speech/test_speech_api.md` | `test_speech_recognize_mock.py`, `test_speech_recognize_json.py` | `services/speech.py` |
| `backend/speech/speech-di.md` | - | `services/speech.py` |
| `backend/speech/azure-speech.md` | `test_azure_speech_service.py` | `services/speech.py` |
| `backend/speech/azure-speech-service-spec.md` | `test_azure_speech_service.py` | `services/speech.py` |
| `backend/speech/speech-backend.md` | `test_speech_backend.py`, `test_speech_main_migration.py` | `services/speech.py`, `main.py` |

---

## Backend - RAG API

| Document | Tests | src実装 |
|----------|-------|---------|
| `backend/rag/test_rag_api.md` | - | `services/rag.py` |

---

## Backend - Stream API

| Document | Tests | src実装 |
|----------|-------|---------|
| `backend/stream/test_stream_api.md` | `test_stream_main_migration.py`, `test_stream_broadcast_params.py` | `services/stream.py` |
| `backend/stream/streaming-response.md` | `test_stream_main_migration.py` | `services/stream.py` |

---

## Frontend - Operator画面

| Document | Tests | src実装 |
|----------|-------|---------|
| `operator/done_test_operator_layout.md` | `test_operator_layout.py`, `test_sidebar_controls.py` | `1_operator_app.py` |
| `operator/done_test_operator_speech.md` | **`test_operator_speech_1.py`** (統合済み) | `1_operator_app.py`, `operator_speech_session_manager.py` |
| `operator/done_test_operator_answer.md` | **`test_operator_answer1.py`** (統合済み) | `1_operator_app.py` |
| `operator/done_test_operator_broadcast.md` | `test_operator_broadcast.py`, `test_update_ui.py` | `1_operator_app.py` |

---

## Frontend - Officer画面

| Document | Tests | src実装 |
|----------|-------|---------|
| `officer/done_test_officer_layout.md` | `test_officer_layout.py`, `test_officer_question_area.py`, `test_officer_answer_tabs.py` | `2_officer_app.py` |
| `officer/done_test_officer_font_size.md` | `test_officer_font_size.py`, `test_officer_font_size_buttons.py` | `2_officer_app.py` |
| `officer/done_test_officer_sse.md` | `test_officer_sse.py` | `2_officer_app.py` |

---

## 補足ドキュメント (設計・リファレンス)

| Document | 用途 |
|----------|------|
| `operator/operator-ui.md` | UI設計書 |
| `operator/operator-endpoint.md` | エンドポイント設計 |
| `operator/done_operator-st-example.md` | Streamlit実装例 |
| `frontend/ui-layout.md` | 全体レイアウト設計 |
| `backend/speech/speech-code-example.md` | コード例 |
| `backend/TEST_LIST_API_MIGRATION.md` | APIマイグレーションリスト |

---

## ファイルパス一覧

### src (実装)
```
src/backend/main.py
src/backend/services/speech.py
src/backend/services/rag.py
src/backend/services/stream.py
src/frontend/app/main.py
src/frontend/app/pages/1_operator_app.py
src/frontend/app/pages/2_officer_app.py
src/frontend/app/pages/operator_speech_session_manager.py
```

### tests
```
tests/backend/services/speech/
  test_speech_recognize_mock.py
  test_speech_recognize_json.py
  test_speech_backend.py
  test_speech_main_migration.py
  test_azure_speech_service.py

tests/backend/services/rag/
  test_stream_main_migration.py
  test_stream_broadcast_params.py

tests/frontend/app/pages/operator/
  test_operator_layout.py
  test_operator_speech_1.py          # 統合済み (7ファイル → 1ファイル)
  test_operator_answer1.py           # 統合済み (12ファイル → 1ファイル)
  test_operator_broadcast.py
  test_sidebar_controls.py
  test_update_ui.py

tests/frontend/app/pages/officer/
  test_officer_layout.py
  test_officer_question_area.py
  test_officer_answer_tabs.py
  test_officer_font_size.py
  test_officer_font_size_buttons.py
  test_officer_sse.py
```
