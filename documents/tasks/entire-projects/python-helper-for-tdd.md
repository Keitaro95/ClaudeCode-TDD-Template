# TDD用テストヘルパー - FastAPI & Streamlit

## 結論

**はい、必要です。**

Pytest FixtureとStreamlit用のヘルパー関数がないと、テストコードがセットアップ処理（外部API接続、モック化など）で埋め尽くされ、TDDの「Red（テストを書く）」フェーズが重くなります。

このプロジェクトでは、以下の構成でテストヘルパーを実装します。

---

## ディレクトリ構造（テスト関連）

```
cosmo-ir-2026/
├── tests/
│   ├── backend/
│   │   ├── conftest.py                  # FastAPI用のpytest fixtures
│   │   ├── test_speech.py               # 音声認識APIのテスト
│   │   ├── test_rag.py                  # RAG APIのテスト
│   │   └── test_stream.py               # SSE APIのテスト
│   │
│   └── frontend/
│       ├── conftest.py                  # Streamlit用のpytest fixtures
│       ├── helpers.py                   # Streamlit AppTest ヘルパー
│       ├── test_operator_app.py         # オペレータ画面のテスト
│       └── test_officer_app.py          # 役員画面のテスト
```

---

## 1. FastAPI におけるヘルパー（Pytest Fixture）

### 目的

FastAPIのTDDでは、以下を自動化するヘルパー（Fixture）が必要です。

1. **TestClientの作成**: `AsyncClient` または `TestClient` の初期化
2. **外部サービスのモック**: Azure Speech API、LLM APIなどを実際に叩かないようにする
3. **環境変数の分離**: テスト用のBACKEND_URLなどを設定

### 実装イメージ

#### `tests/backend/conftest.py`

```python
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
import sys

# 実装したバックエンドアプリをインポート
from src.backend.main import app

# 外部依存のモックを作成するヘルパー
@pytest.fixture(scope="function", autouse=True)
def mock_azure_services():
    """
    Azure SDKをモック化し、実際の外部APIを叩かないようにする。
    autouse=Trueで、すべてのテストで自動適用される。
    """
    # Azure Speech Service のモック
    mock_speech = MagicMock()
    mock_recognizer = MagicMock()
    mock_result = MagicMock()
    mock_result.text = "これはテスト音声です"
    mock_recognizer.recognize_once_async.return_value.get.return_value = mock_result
    mock_speech.SpeechRecognizer.return_value = mock_recognizer

    sys.modules["azure.cognitiveservices.speech"] = mock_speech

    yield

    # クリーンアップ
    if "azure.cognitiveservices.speech" in sys.modules:
        del sys.modules["azure.cognitiveservices.speech"]


# FastAPI TestClient を作成するヘルパー
@pytest.fixture(scope="function")
async def async_client():
    """
    FastAPI の AsyncClient を作成し、テストで使用できるようにする。
    各テスト関数で自動注入される。
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
```

### テスト例

#### `tests/backend/test_rag.py`

```python
import pytest

@pytest.mark.asyncio
async def test_rag_answer_endpoint(async_client):
    """RAG回答生成エンドポイントのテスト"""
    # Arrange
    request_data = {
        "question": "今期の売上目標は？",
        "summary_length": 100,
        "detail_length": 300
    }

    # Act
    response = await async_client.post("/api/rag/answer", json=request_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "detail" in data
    assert len(data["summary"]) > 0
    assert len(data["detail"]) > 0
```

---

## 2. Streamlit におけるヘルパー

### 目的

Streamlitには `AppTest` という公式テストフレームワークがあります。ここでのヘルパーの役割は：

1. **重い処理（Azure SDK、FastAPI呼び出しなど）のモック化**
2. **AppTest の初期化を簡略化**
3. **テスト環境の分離**

### 実装イメージ

#### `tests/frontend/helpers.py`

```python
from streamlit.testing.v1 import AppTest
from unittest.mock import MagicMock, patch
import sys
import os

def create_streamlit_runner(page_path: str):
    """
    Streamlit AppTest のヘルパー関数。
    外部依存をモックした状態でStreamlitアプリのインスタンスを返す。

    Args:
        page_path: テストするStreamlitページのパス
                  例: "src/frontend/app/pages/1_operator_app.py"

    Returns:
        AppTest: 初期化済みのAppTestインスタンス
    """
    # 1. 環境変数をテスト用に設定
    os.environ["BACKEND_URL"] = "http://test:8000"

    # 2. Azure SDKをモック化
    mock_speech = MagicMock()
    mock_speech.SpeechRecognizer.return_value.recognize_once_async.return_value.get.return_value.text = "テスト音声入力"
    sys.modules["azure.cognitiveservices.speech"] = mock_speech

    # 3. Streamlit AppTest を初期化
    at = AppTest.from_file(page_path)
    at.run()

    return at


def mock_backend_api():
    """
    FastAPI バックエンドへのHTTPリクエストをモック化する。
    requests.post や httpx などのライブラリをモックする。
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "summary": "これはテスト要約です。",
        "detail": "これはテスト詳細回答です。より長い説明がここに入ります。"
    }
    return mock_response
```

#### `tests/frontend/conftest.py`

```python
import pytest
from unittest.mock import MagicMock
import sys

@pytest.fixture(scope="function", autouse=True)
def mock_external_deps():
    """
    Streamlitテスト用の外部依存モック。
    すべてのテストで自動適用される。
    """
    # requestsライブラリをモック化（FastAPI呼び出し用）
    mock_requests = MagicMock()
    mock_requests.post.return_value.status_code = 200
    mock_requests.post.return_value.json.return_value = {
        "summary": "モック要約",
        "detail": "モック詳細"
    }
    sys.modules["requests"] = mock_requests

    yield

    # クリーンアップ
    if "requests" in sys.modules:
        del sys.modules["requests"]
```

### テスト例

#### `tests/frontend/test_operator_app.py`

```python
from tests.frontend.helpers import create_streamlit_runner

def test_operator_screen_speech_recognition_button():
    """オペレータ画面：音声認識ボタンのテスト"""
    # Arrange: ヘルパーを使ってアプリ起動
    at = create_streamlit_runner("src/frontend/app/pages/1_operator_app.py")

    # Act: 音声認識ボタンを押す
    at.button[0].click().run()

    # Assert: モックされた音声認識結果が表示されているか
    assert "テスト音声入力" in at.text_area[0].value


def test_operator_screen_answer_generation():
    """オペレータ画面：回答生成ボタンのテスト"""
    # Arrange
    at = create_streamlit_runner("src/frontend/app/pages/1_operator_app.py")

    # 質問テキストを入力
    at.text_area[0].input("今期の売上目標は？").run()

    # Act: 回答作成ボタンを押す
    at.button[1].click().run()

    # Assert: 回答が生成されているか
    assert "モック要約" in at.text_area[1].value
    assert "モック詳細" in at.text_area[2].value
```

---

## 3. TDDエージェントへのプロンプト調整案

新しいTDDエージェント（FastAPI/Streamlit用）を作る場合、以下の指示を含める必要があります。

### FastAPI用

```markdown
## Test Structure Requirements

- Use `async_client` pytest fixture for API interaction
- All external Azure services are automatically mocked via `mock_azure_services` fixture
- Test file location: `tests/backend/test_<service_name>.py`
- Use `@pytest.mark.asyncio` for async test functions

Example:
```python
@pytest.mark.asyncio
async def test_speech_recognize(async_client):
    response = await async_client.post("/api/speech/recognize", json={...})
    assert response.status_code == 200
```
```

### Streamlit用

```markdown
## Test Structure Requirements

- Use `create_streamlit_runner(path)` helper from `tests.frontend.helpers` to initialize the app
- Simulate user interactions using `at.button[index].click().run()` syntax
- Verify UI state via `at.text_area`, `at.markdown`, `at.info`, etc.
- Test file location: `tests/frontend/test_<page_name>.py`

Example:
```python
from tests.frontend.helpers import create_streamlit_runner

def test_operator_button():
    at = create_streamlit_runner("src/frontend/app/pages/1_operator_app.py")
    at.button[0].click().run()
    assert "expected text" in at.markdown[0].value
```
```

---

## まとめ

### ヘルパー関数（またはFixture）は必須

これがないと、TDDのサイクル（Red → Green → Refactor）の「Red」を書く段階で、テストコードの記述コストが高すぎて挫折する原因になります。

### 実装すべきヘルパー

| 対象 | ファイル | 役割 |
|-----|---------|------|
| **FastAPI** | `tests/backend/conftest.py` | `async_client` fixture、外部APIモック |
| **Streamlit** | `tests/frontend/helpers.py` | `create_streamlit_runner()` 関数 |
| **Streamlit** | `tests/frontend/conftest.py` | 外部依存の自動モック |

### TDDのメリット

- **セットアップコストの削減**: 1行でテスト環境が整う
- **テストの可読性向上**: ビジネスロジックに集中できる
- **メンテナンス性**: モック設定が一箇所に集約される

---

**Copyright © MILIZE Inc. ALL rights reserved**

**機密区分: Confidential**
