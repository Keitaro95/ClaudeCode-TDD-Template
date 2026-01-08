"""
FastAPI テスト用の pytest fixtures

このモジュールは、FastAPI アプリケーションのテストに必要な共通セットアップを提供します。
- AsyncClient: 非同期HTTPクライアントの作成
- 外部サービス（Azure SDK等）の自動モック化
"""

import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
import sys


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


@pytest.fixture(scope="function")
async def async_client():
    """
    FastAPI の AsyncClient を作成し、テストで使用できるようにする。
    各テスト関数で自動注入される。

    使用例:
        @pytest.mark.asyncio
        async def test_endpoint(async_client):
            response = await async_client.post("/api/endpoint", json={...})
            assert response.status_code == 200
    """
    # 実装したバックエンドアプリをインポート
    # NOTE: 実際のアプリ実装後に、正しいパスに修正してください
    try:
        from src.backend.main import app
    except ImportError:
        # アプリがまだ実装されていない場合は、ダミーのFastAPIアプリを使用
        from fastapi import FastAPI
        app = FastAPI()

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
