"""
Streamlit テスト用の pytest fixtures

このモジュールは、Streamlit アプリケーションのテストに必要な共通セットアップを提供します。
- 外部依存（Azure SDK、HTTPライブラリ等）の自動モック化
"""

import pytest
from unittest.mock import MagicMock
import sys


@pytest.fixture(scope="function", autouse=True)
def mock_external_deps():
    """
    Streamlitテスト用の外部依存モック。
    すべてのテストで自動適用される。

    モック対象:
    - requests: FastAPIバックエンドへのHTTP呼び出し
    - Azure SDK: 音声認識等の外部サービス
    """
    # requestsライブラリをモック化（FastAPI呼び出し用）
    mock_requests = MagicMock()
    mock_requests.post.return_value.status_code = 200
    mock_requests.post.return_value.json.return_value = {
        "summary": "モック要約",
        "detail": "モック詳細"
    }
    sys.modules["requests"] = mock_requests

    # Azure Speech Service のモック
    mock_speech = MagicMock()
    mock_recognizer = MagicMock()
    mock_result = MagicMock()
    mock_result.text = "テスト音声入力"
    mock_recognizer.recognize_once_async.return_value.get.return_value = mock_result
    mock_speech.SpeechRecognizer.return_value = mock_recognizer
    sys.modules["azure.cognitiveservices.speech"] = mock_speech

    yield

    # クリーンアップ
    if "requests" in sys.modules:
        del sys.modules["requests"]
    if "azure.cognitiveservices.speech" in sys.modules:
        del sys.modules["azure.cognitiveservices.speech"]
