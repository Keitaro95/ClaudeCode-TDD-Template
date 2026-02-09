import asyncio
from unittest.mock import MagicMock, patch

import pytest

from src.backend.services.speech import AzureSpeechService


# テストクラス全体に適用するマーカー（全てのメソッドを非同期テストとして扱う）
@pytest.mark.asyncio
class TestAzureSpeechServiceEventHandlers:
    @pytest.fixture
    def mock_speech_env(self):
        """
        セットアップとティアダウンを行うフィクスチャ。
        テスト関数の引数として受け取ることで、準備済みのオブジェクトを使えます。
        """
        # 1. 環境変数のモック
        env_vars = {
            "SPEECH_KEY": "test-key",
            "SPEECH_REGION": "japaneast",
        }

        # 2. Azure SDK のモック
        # 重要: 'azure.cognitiveservices.speech' ではなく、
        # それを使っている 'src.backend.services.speech.speechsdk' をパッチします
        with patch.dict("os.environ", env_vars), patch("src.backend.services.speech.speechsdk") as mock_sdk:
            # 列挙型（Enum）のモック定義
            mock_sdk.ResultReason.RecognizedSpeech = "RecognizedSpeech"
            mock_sdk.CancellationReason.Error = "Error"

            # サービスインスタンス化
            service = AzureSpeechService()

            # テスト実行中のイベントループをサービスに注入
            # (プロダクションコードが _loop を使っているため)
            service._loop = asyncio.get_running_loop()

            # テスト関数に渡すデータをまとめる
            yield {"service": service, "mock_sdk": mock_sdk}
            # withブロックを抜けると自動的にパッチが解除（クリーンアップ）されます

    async def test_recognizing_event_structure(self, mock_speech_env):
        """_on_recognizing ハンドラの構造検証"""
        service = mock_speech_env["service"]

        # Arrange
        mock_evt = MagicMock()
        mock_evt.result.text = "テスト中間結果"

        # Act
        service._on_recognizing(mock_evt)

        # Assert
        # asyncio.wait_for でタイムアウト付きでキュー取得（フリーズ防止）
        event = await asyncio.wait_for(service._event_queue.get(), timeout=1.0)
        assert event == {"type": "recognizing", "text": "テスト中間結果"}

    async def test_recognized_event_structure(self, mock_speech_env):
        """_on_recognized ハンドラの構造検証"""
        service = mock_speech_env["service"]
        mock_sdk = mock_speech_env["mock_sdk"]

        # Arrange
        mock_evt = MagicMock()
        mock_evt.result.text = "確定テキスト"
        mock_evt.result.reason = mock_sdk.ResultReason.RecognizedSpeech

        # Act
        service._on_recognized(mock_evt)

        # Assert
        event = await asyncio.wait_for(service._event_queue.get(), timeout=1.0)
        assert event == {"type": "recognized", "text": "確定テキスト"}

    async def test_session_stopped_event_structure(self, mock_speech_env):
        """_on_session_stopped ハンドラの構造検証"""
        service = mock_speech_env["service"]

        # Arrange
        service._is_recognizing = True
        mock_evt = MagicMock()

        # Act
        service._on_session_stopped(mock_evt)

        # Assert
        event = await asyncio.wait_for(service._event_queue.get(), timeout=1.0)
        assert event == {"type": "session_stopped"}
        assert service._is_recognizing is False

    async def test_canceled_event_structure(self, mock_speech_env):
        """_on_canceled ハンドラの構造検証"""
        service = mock_speech_env["service"]
        mock_sdk = mock_speech_env["mock_sdk"]

        # Arrange
        service._is_recognizing = True
        mock_evt = MagicMock()
        mock_evt.cancellation_details.reason = mock_sdk.CancellationReason.Error
        mock_evt.cancellation_details.error_details = "Connection failed"

        # Act
        service._on_canceled(mock_evt)

        # Assert
        event = await asyncio.wait_for(service._event_queue.get(), timeout=1.0)
        assert event["type"] == "canceled"
        assert event["error"] == "Connection failed"
        assert service._is_recognizing is False
