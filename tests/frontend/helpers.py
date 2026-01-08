"""
Streamlit AppTest ヘルパー関数

このモジュールは、Streamlit の AppTest を使ったテストを簡単に記述するためのヘルパー関数を提供します。
"""

from streamlit.testing.v1 import AppTest
from typing import Any
import sys
import os


def create_streamlit_runner(page_path: str) -> AppTest:
    """
    Streamlit AppTest のヘルパー関数。
    外部依存をモックした状態でStreamlitアプリのインスタンスを返す。

    Args:
        page_path: テストするStreamlitページのパス
                  例: "src/frontend/app/pages/1_operator_app.py"

    Returns:
        AppTest: 初期化済みのAppTestインスタンス

    使用例:
        def test_operator_button(mocker):
            mocker.patch("requests.post", return_value=mock_backend_api())
            at = create_streamlit_runner("src/frontend/app/pages/1_operator_app.py")
            at.button[0].click().run()
            assert "expected text" in at.text_area[0].value
    """
    # 1. 環境変数をテスト用に設定
    os.environ["BACKEND_URL"] = "http://test:8000"

    # 2. Azure SDKをモック化（conftest.pyで既にモックされているが、念のため）
    from unittest.mock import MagicMock

    mock_speech = MagicMock()
    mock_recognizer = MagicMock()
    mock_result = MagicMock()
    mock_result.text = "テスト音声入力"
    mock_recognizer.recognize_once_async.return_value.get.return_value = mock_result
    mock_speech.SpeechRecognizer.return_value = mock_recognizer
    sys.modules["azure.cognitiveservices.speech"] = mock_speech

    # 3. Streamlit AppTest を初期化
    at = AppTest.from_file(page_path)
    at.run()

    return at


def mock_backend_api(
    summary: str = "これはテスト要約です。",
    detail: str = "これはテスト詳細回答です。より長い説明がここに入ります。",
    status_code: int = 200
) -> Any:
    """
    FastAPI バックエンドへのHTTPリクエストをモック化する。
    requests.post や httpx などのライブラリをモックする。

    Args:
        summary: モックレスポンスのsummaryフィールド
        detail: モックレスポンスのdetailフィールド
        status_code: HTTPステータスコード

    Returns:
        Mock: モックされたレスポンスオブジェクト

    使用例:
        def test_api_call(mocker):
            mocker.patch("requests.post", return_value=mock_backend_api())
            # テスト処理
    """
    from unittest.mock import MagicMock

    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.json.return_value = {
        "summary": summary,
        "detail": detail
    }
    return mock_response


def mock_azure_speech_result(text: str = "テスト音声認識結果") -> None:
    """
    Azure Speech Service の認識結果をモック化する。

    Args:
        text: モックする音声認識結果のテキスト

    使用例:
        def test_speech_recognition():
            mock_azure_speech_result("カスタム音声結果")
            # この後のテストでは指定したテキストが返される
    """
    from unittest.mock import MagicMock

    mock_speech = MagicMock()
    mock_recognizer = MagicMock()
    mock_result = MagicMock()
    mock_result.text = text
    mock_recognizer.recognize_once_async.return_value.get.return_value = mock_result
    mock_speech.SpeechRecognizer.return_value = mock_recognizer
    sys.modules["azure.cognitiveservices.speech"] = mock_speech
