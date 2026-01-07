# バックエンドスタブ実装ガイド v2

## 概要

本ドキュメントは、株主総会支援システムのプロトタイプ開発において、外部API・データベースのスタブ（モック）を実装するための詳細な指示書です。

**目的**: 実際のAzureリソースやAPI接続なしで、エンドツーエンドの動作確認を可能にする

**スコープ**: 以下の外部依存をすべてスタブ化
- Azure Speech Service（音声認識・話者分離）
- Azure Blob Storage（音声ファイル保存）
- Claude Sonnet 4.5 API（回答生成）
- Azure Cosmos DB（想定問答のベクトル検索）
- OpenAI Embedding API（テキストのベクトル化）
- Cohere Rerank API（検索結果の再ランク）

---

## 1. 全体設計

### 1.1 スタブモードの切り替え仕様

#### 環境変数による制御

`.env` ファイルで一括制御:

```bash
# スタブモード設定（true/false）
USE_STUB=true

# 個別のスタブ制御（オプショナル）
USE_STUB_SPEECH=true
USE_STUB_BLOB=true
USE_STUB_CLAUDE=true
USE_STUB_COSMOSDB=true
USE_STUB_EMBEDDING=true
USE_STUB_RERANK=true
```

#### 依存性注入パターン

**ファイル**: `backend/app/dependencies.py`

```python
import os
from typing import Protocol

# プロトコル定義（インターフェース）
class SpeechServiceProtocol(Protocol):
    async def recognize_continuous(self, meeting_id: str): ...

class BlobStorageProtocol(Protocol):
    def upload_audio_file(self, meeting_id: str, audio_data: bytes) -> str: ...

class AnswerGeneratorProtocol(Protocol):
    async def generate_answer(self, question: str, related_qa_pairs: list) -> dict: ...

class VectorSearchProtocol(Protocol):
    async def search_similar_qa(self, query_vector: list, top_k: int) -> list: ...

class EmbeddingProtocol(Protocol):
    async def embed_text(self, text: str) -> list[float]: ...

class RerankProtocol(Protocol):
    def rerank_results(self, query: str, documents: list, top_n: int) -> list: ...


def _use_stub(service_name: str = "") -> bool:
    """スタブモード判定"""
    global_stub = os.getenv("USE_STUB", "false").lower() == "true"
    if service_name:
        specific_stub = os.getenv(f"USE_STUB_{service_name.upper()}", "").lower()
        if specific_stub in ("true", "false"):
            return specific_stub == "true"
    return global_stub


def get_speech_service() -> SpeechServiceProtocol:
    """音声認識サービス取得"""
    if _use_stub("speech"):
        from app.services.stub.speech_recognition_stub import SpeechRecognitionServiceStub
        return SpeechRecognitionServiceStub()
    else:
        from app.services.speech_recognition import SpeechRecognitionService
        return SpeechRecognitionService()


def get_blob_storage_service() -> BlobStorageProtocol:
    """Blob Storage サービス取得"""
    if _use_stub("blob"):
        from app.services.stub.audio_storage_stub import AudioStorageServiceStub
        return AudioStorageServiceStub()
    else:
        from app.services.audio_storage import AudioStorageService
        return AudioStorageService()


def get_answer_generator() -> AnswerGeneratorProtocol:
    """回答生成サービス取得"""
    if _use_stub("claude"):
        from app.services.stub.answer_generator_stub import AnswerGeneratorStub
        return AnswerGeneratorStub()
    else:
        from app.services.answer_generator import AnswerGeneratorService
        return AnswerGeneratorService()


def get_vector_search_service() -> VectorSearchProtocol:
    """ベクトル検索サービス取得"""
    if _use_stub("cosmosdb"):
        from app.services.stub.vector_search_stub import VectorSearchServiceStub
        return VectorSearchServiceStub()
    else:
        from app.services.vector_search import VectorSearchService
        return VectorSearchService()


def get_embedding_service() -> EmbeddingProtocol:
    """Embedding サービス取得"""
    if _use_stub("embedding"):
        from app.services.stub.embedding_stub import EmbeddingServiceStub
        return EmbeddingServiceStub()
    else:
        from app.services.embedding import EmbeddingService
        return EmbeddingService()


def get_rerank_service() -> RerankProtocol:
    """Rerank サービス取得"""
    if _use_stub("rerank"):
        from app.services.stub.rerank_stub import RerankServiceStub
        return RerankServiceStub()
    else:
        from app.services.rerank import RerankService
        return RerankService()
```

### 1.2 ディレクトリ構成

```
backend/
├── app/
│   ├── services/
│   │   ├── stub/                          # スタブ専用ディレクトリ
│   │   │   ├── __init__.py
│   │   │   ├── speech_recognition_stub.py
│   │   │   ├── audio_storage_stub.py
│   │   │   ├── answer_generator_stub.py
│   │   │   ├── vector_search_stub.py
│   │   │   ├── embedding_stub.py
│   │   │   ├── rerank_stub.py
│   │   │   └── mock_data.py              # モックデータ集約
│   │   ├── speech_recognition.py         # 本番実装
│   │   ├── audio_storage.py
│   │   ├── answer_generator.py
│   │   ├── vector_search.py
│   │   ├── embedding.py
│   │   └── rerank.py
│   ├── dependencies.py
│   └── main.py
```

---

## 2. スタブ実装詳細

### 2.1 Azure Speech Service スタブ

#### 2.1.1 リアルタイム音声認識スタブ

**ファイル**: `backend/app/services/stub/speech_recognition_stub.py`

```python
from typing import AsyncIterator
from datetime import datetime
import asyncio
import logging
from app.models.speech import TranscriptionResult

logger = logging.getLogger(__name__)


class SpeechRecognitionServiceStub:
    """Azure Speech Service のスタブ実装"""

    def __init__(self):
        logger.info("[STUB] SpeechRecognitionServiceStub 初期化")
        self.mock_utterances = self._load_mock_utterances()

    def _load_mock_utterances(self) -> list[dict]:
        """モック発話データを読み込み"""
        from app.services.stub.mock_data import MOCK_UTTERANCES
        return MOCK_UTTERANCES

    async def recognize_continuous(
        self,
        meeting_id: str,
        audio_stream=None  # スタブでは使用しない
    ) -> AsyncIterator[TranscriptionResult]:
        """
        リアルタイム音声認識のモックデータを返す

        Args:
            meeting_id: 会議ID
            audio_stream: 音声ストリーム（スタブでは無視）

        Yields:
            TranscriptionResult: 文字起こし結果
        """
        logger.info(f"[STUB] リアルタイム音声認識開始: meeting_id={meeting_id}")

        # 実際の音声認識をシミュレート（2秒間隔で発話を返す）
        for i, utterance in enumerate(self.mock_utterances, 1):
            await asyncio.sleep(2)  # リアルタイム性をシミュレート

            result = TranscriptionResult(
                speaker_id=utterance["speaker_id"],
                speaker_name=utterance.get("speaker_name", utterance["speaker_id"]),
                text=utterance["text"],
                timestamp=datetime.now().isoformat(),
                confidence=utterance.get("confidence", 0.95),
                is_final=True
            )

            logger.info(
                f"[STUB] 発話 {i}/{len(self.mock_utterances)}: "
                f"{result.speaker_name} - {result.text[:30]}..."
            )

            yield result

        logger.info("[STUB] リアルタイム音声認識終了")

    async def start_recognition(self, meeting_id: str) -> bool:
        """音声認識開始（スタブでは常に成功）"""
        logger.info(f"[STUB] 音声認識開始: meeting_id={meeting_id}")
        return True

    async def stop_recognition(self, meeting_id: str) -> bool:
        """音声認識停止（スタブでは常に成功）"""
        logger.info(f"[STUB] 音声認識停止: meeting_id={meeting_id}")
        return True
```

#### 2.1.2 モックデータファイル

**ファイル**: `backend/app/services/stub/mock_data.py`

```python
"""スタブ用モックデータ集約"""

# 株主総会での質疑応答シミュレーション
MOCK_UTTERANCES = [
    {
        "speaker_id": "Speaker_1",
        "speaker_name": "株主A",
        "text": "今期の売上高が前年比10%増加していますが、その主な要因は何でしょうか。",
        "confidence": 0.95
    },
    {
        "speaker_id": "Speaker_2",
        "speaker_name": "IR担当役員",
        "text": "ありがとうございます。主な要因は新規事業の立ち上げと既存顧客からのリピート率向上です。",
        "confidence": 0.93
    },
    {
        "speaker_id": "Speaker_1",
        "speaker_name": "株主A",
        "text": "新規事業について、もう少し詳しく教えていただけますか。",
        "confidence": 0.96
    },
    {
        "speaker_id": "Speaker_2",
        "speaker_name": "IR担当役員",
        "text": "はい。DX支援サービスを開始し、中小企業を中心に現在50社以上と契約しております。",
        "confidence": 0.94
    },
    {
        "speaker_id": "Speaker_3",
        "speaker_name": "株主B",
        "text": "配当政策について教えてください。今後も安定配当を継続していただけるのでしょうか。",
        "confidence": 0.92
    },
    {
        "speaker_id": "Speaker_2",
        "speaker_name": "IR担当役員",
        "text": "当社は安定的な配当の継続を基本方針としており、今後も維持してまいります。",
        "confidence": 0.95
    },
    {
        "speaker_id": "Speaker_4",
        "speaker_name": "株主C",
        "text": "ESG経営への取り組み状況を教えてください。特に環境への配慮について伺いたいです。",
        "confidence": 0.90
    },
    {
        "speaker_id": "Speaker_2",
        "speaker_name": "IR担当役員",
        "text": "CO2排出量削減目標を設定し、2030年までに30%削減を目指しております。",
        "confidence": 0.93
    },
]

# 想定問答データベース（ベクトル検索用）
MOCK_QA_DATABASE = [
    {
        "id": "qa_001",
        "question": "今期の業績見通しについて教えてください。",
        "answer_summary": "売上高は前年比10%増の見込みです。",
        "answer_detail": """今期の業績見通しについてご説明いたします。

【売上高】
前年比10%増の120億円を見込んでおります。

【営業利益】
前年比15%増の15億円を見込んでおります。

【主な増収要因】
1. 新規事業（DX支援サービス）の立ち上げ
2. 既存顧客との取引拡大
3. 新規顧客の獲得

以上でございます。""",
        "category": "業績",
        "tags": ["売上", "利益", "見通し"],
        "confidence": 0.92,
        "created_at": "2025-09-01"
    },
    {
        "id": "qa_002",
        "question": "配当政策について教えてください。",
        "answer_summary": "安定的な配当の継続を基本方針としています。",
        "answer_detail": """配当政策についてご説明いたします。

【基本方針】
当社は、株主還元を経営の重要課題と位置づけており、安定的な配当の継続を基本方針としております。

【配当性向】
連結配当性向30%を目安としております。

【今期の配当予想】
1株当たり年間配当金は50円を予定しております。

今後も業績に応じて、適切な株主還元を実施してまいります。""",
        "category": "株主還元",
        "tags": ["配当", "株主還元"],
        "confidence": 0.88,
        "created_at": "2025-09-01"
    },
    {
        "id": "qa_003",
        "question": "新規事業の進捗状況を教えてください。",
        "answer_summary": "DX支援サービスは順調に拡大しています。",
        "answer_detail": """新規事業の進捗状況についてご報告いたします。

【DX支援サービス】
本年4月に開始したDX支援サービスは、計画を上回るペースで契約数が増加しております。

【契約実績】
- 契約企業数: 50社（目標30社に対して達成率167%）
- 主な業種: 製造業、小売業、サービス業

【今後の展開】
今後3年間で契約企業数200社を目指してまいります。

以上でございます。""",
        "category": "事業戦略",
        "tags": ["新規事業", "DX", "進捗"],
        "confidence": 0.85,
        "created_at": "2025-09-01"
    },
    {
        "id": "qa_004",
        "question": "人材育成への取り組みについて教えてください。",
        "answer_summary": "研修制度の拡充と資格取得支援を実施しています。",
        "answer_detail": """人材育成への取り組みについてご説明いたします。

【研修制度】
階層別研修、専門スキル研修を拡充し、年間延べ5000時間の研修を実施しております。

【資格取得支援】
業務に関連する資格取得費用を全額補助し、取得者には報奨金を支給しております。

【実績】
本年度は延べ120名が各種資格を取得いたしました。

今後も人材育成に注力してまいります。""",
        "category": "人材",
        "tags": ["人材育成", "研修", "資格"],
        "confidence": 0.80,
        "created_at": "2025-09-01"
    },
    {
        "id": "qa_005",
        "question": "ESG経営への取り組みを教えてください。",
        "answer_summary": "環境負荷削減と社会貢献活動に注力しています。",
        "answer_detail": """ESG経営への取り組みについてご説明いたします。

【環境（E）】
CO2排出量削減目標を設定し、2030年までに2020年比30%削減を目指しております。

【社会（S）】
地域社会貢献活動として、清掃活動や教育支援を継続的に実施しております。

【ガバナンス（G）】
取締役会の実効性評価を毎年実施し、透明性の高い経営を推進しております。

今後もESG経営を強化してまいります。""",
        "category": "ESG",
        "tags": ["ESG", "環境", "社会貢献"],
        "confidence": 0.75,
        "created_at": "2025-09-01"
    },
    {
        "id": "qa_006",
        "question": "海外展開の計画はありますか。",
        "answer_summary": "現時点では国内事業に注力しています。",
        "answer_detail": """海外展開についてのご質問にお答えいたします。

【現状】
現時点では、国内市場でのシェア拡大に注力しております。

【中期的な検討】
アジア市場への進出については、中期経営計画の中で検討を進めております。

【準備状況】
市場調査と現地パートナー候補との協議を開始しております。

具体的な進出時期が決まりましたら、改めてご報告申し上げます。""",
        "category": "事業戦略",
        "tags": ["海外展開", "グローバル"],
        "confidence": 0.70,
        "created_at": "2025-09-01"
    },
    {
        "id": "qa_007",
        "question": "コスト削減の具体的な取り組みを教えてください。",
        "answer_summary": "業務プロセス改善とデジタル化を推進しています。",
        "answer_detail": """コスト削減の取り組みについてご説明いたします。

【業務プロセス改善】
業務フローを見直し、不要な工程を削減いたしました。

【デジタル化推進】
ペーパーレス化と業務システムの刷新により、間接コストを前年比10%削減いたしました。

【調達最適化】
購買プロセスを見直し、材料費を5%削減いたしました。

今後も継続的なコスト削減に取り組んでまいります。""",
        "category": "コスト管理",
        "tags": ["コスト削減", "効率化"],
        "confidence": 0.82,
        "created_at": "2025-09-01"
    },
    {
        "id": "qa_008",
        "question": "研究開発投資の方針を教えてください。",
        "answer_summary": "売上高の5%を研究開発に投資しています。",
        "answer_detail": """研究開発投資についてご説明いたします。

【投資方針】
売上高の5%を研究開発費として計上し、新技術・新製品の開発に注力しております。

【重点分野】
AI・IoT技術の活用による製品の高付加価値化を進めております。

【成果】
本年度は3件の特許を出願し、2件の新製品を市場投入いたしました。

今後も技術革新に積極的に投資してまいります。""",
        "category": "研究開発",
        "tags": ["研究開発", "投資", "イノベーション"],
        "confidence": 0.78,
        "created_at": "2025-09-01"
    },
]

# Claude API レスポンスのテンプレート
MOCK_ANSWER_TEMPLATES = {
    "summary_prefix": "ご質問ありがとうございます。",
    "detail_prefix": """ご質問ありがとうございます。

{question}につきまして、以下のとおりご回答申し上げます。

""",
    "detail_suffix": """

以上でございます。今後とも何卒よろしくお願い申し上げます。"""
}
```

---

### 2.2 Azure Blob Storage スタブ

**ファイル**: `backend/app/services/stub/audio_storage_stub.py`

```python
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class AudioStorageServiceStub:
    """Azure Blob Storage のスタブ実装"""

    def __init__(self):
        logger.info("[STUB] AudioStorageServiceStub 初期化")
        self.mock_storage_path = Path("./mock_storage/audio")
        self.mock_storage_path.mkdir(parents=True, exist_ok=True)

    def upload_audio_file(
        self,
        meeting_id: str,
        audio_data: bytes,
        file_extension: str = "wav"
    ) -> str:
        """
        音声ファイルアップロードをモック

        Args:
            meeting_id: 会議ID
            audio_data: 音声データ（バイト列）
            file_extension: ファイル拡張子

        Returns:
            str: モックBlobストレージのURL
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        blob_name = f"{meeting_id}_{timestamp}.{file_extension}"

        # ローカルにファイルを保存（オプション）
        local_path = self.mock_storage_path / blob_name
        with open(local_path, "wb") as f:
            f.write(audio_data)

        # モックURL生成
        mock_url = f"https://mockblobstorage.blob.core.windows.net/audio-files/{blob_name}"

        logger.info(
            f"[STUB] 音声ファイルを保存しました: {mock_url} "
            f"(実際のパス: {local_path}, サイズ: {len(audio_data)} bytes)"
        )

        return mock_url

    def download_audio_file(self, blob_url: str) -> bytes:
        """音声ファイルダウンロードをモック"""
        logger.info(f"[STUB] 音声ファイルをダウンロード: {blob_url}")

        # ローカルファイルから読み込み
        blob_name = blob_url.split("/")[-1]
        local_path = self.mock_storage_path / blob_name

        if local_path.exists():
            with open(local_path, "rb") as f:
                return f.read()
        else:
            logger.warning(f"[STUB] ファイルが見つかりません: {local_path}")
            return b""

    def delete_audio_file(self, blob_url: str) -> bool:
        """音声ファイル削除をモック"""
        logger.info(f"[STUB] 音声ファイルを削除: {blob_url}")

        blob_name = blob_url.split("/")[-1]
        local_path = self.mock_storage_path / blob_name

        if local_path.exists():
            local_path.unlink()
            return True
        return False
```

---

### 2.3 Claude Sonnet 4.5 API スタブ

**ファイル**: `backend/app/services/stub/answer_generator_stub.py`

```python
import asyncio
import logging
from typing import Dict, List
from app.services.stub.mock_data import MOCK_ANSWER_TEMPLATES

logger = logging.getLogger(__name__)


class AnswerGeneratorStub:
    """Claude Sonnet 4.5 API のスタブ実装"""

    def __init__(self):
        logger.info("[STUB] AnswerGeneratorStub 初期化")

    async def generate_answer(
        self,
        question: str,
        related_qa_pairs: List[dict],
        summary_length: int = 100,
        detail_length: int = 1000
    ) -> Dict[str, str]:
        """
        回答生成をモック

        Args:
            question: 質問文
            related_qa_pairs: 関連する想定問答（RAG用）
            summary_length: 要約の文字数
            detail_length: 詳細の文字数

        Returns:
            Dict[str, str]: {"summary": "要約回答", "detail": "詳細回答"}
        """
        logger.info(
            f"[STUB] 回答生成開始: question={question[:50]}..., "
            f"related_qa_count={len(related_qa_pairs)}"
        )

        # API呼び出しの遅延をシミュレート（1〜3秒のランダム）
        delay = 1 + (len(question) % 3)  # 質問の長さに応じて変動
        await asyncio.sleep(delay)

        # 関連QAがあればそれを元に回答を生成
        if related_qa_pairs:
            base_answer = related_qa_pairs[0]["answer_summary"]
            detail_base = related_qa_pairs[0].get("answer_detail", "")
        else:
            base_answer = "現在検討中でございます"
            detail_base = "詳細については、後日改めてご報告申し上げます。"

        # 要約回答を生成
        summary = self._generate_summary(
            question, base_answer, summary_length
        )

        # 詳細回答を生成
        detail = self._generate_detail(
            question, detail_base, related_qa_pairs, detail_length
        )

        logger.info(
            f"[STUB] 回答生成完了: summary={len(summary)}文字, detail={len(detail)}文字"
        )

        return {
            "summary": summary,
            "detail": detail
        }

    def _generate_summary(
        self, question: str, base_answer: str, target_length: int
    ) -> str:
        """要約回答を生成"""
        prefix = MOCK_ANSWER_TEMPLATES["summary_prefix"]
        summary = f"{prefix}{base_answer}"

        # 文字数調整（簡易版）
        if len(summary) > target_length:
            summary = summary[:target_length - 3] + "..."

        return summary

    def _generate_detail(
        self,
        question: str,
        detail_base: str,
        related_qa_pairs: List[dict],
        target_length: int
    ) -> str:
        """詳細回答を生成"""
        prefix = MOCK_ANSWER_TEMPLATES["detail_prefix"].format(question=question)
        suffix = MOCK_ANSWER_TEMPLATES["detail_suffix"]

        # 関連QAから詳細情報を構築
        if detail_base:
            main_content = detail_base
        else:
            main_content = self._build_detail_from_related_qa(related_qa_pairs)

        detail = prefix + main_content + suffix

        # 文字数調整
        if len(detail) > target_length:
            # suffixを残して本文を切り詰め
            available_length = target_length - len(prefix) - len(suffix) - 3
            main_content = main_content[:available_length] + "..."
            detail = prefix + main_content + suffix

        return detail

    def _build_detail_from_related_qa(self, related_qa_pairs: List[dict]) -> str:
        """関連QAから詳細回答を構築"""
        if not related_qa_pairs:
            return """【現状】
当社は現在、中期経営計画に基づき、売上高の拡大と収益性の向上に取り組んでおります。

【今後の見通し】
引き続き、株主の皆様のご期待に応えられるよう、全社一丸となって取り組んでまいります。"""

        # 複数の関連QAから情報を統合
        sections = []
        for i, qa in enumerate(related_qa_pairs[:3], 1):  # 上位3件まで
            category = qa.get("category", "関連情報")
            answer = qa.get("answer_detail", qa.get("answer_summary", ""))
            sections.append(f"【{category}】\n{answer}")

        return "\n\n".join(sections)
```

---

### 2.4 Azure Cosmos DB Vector Search スタブ

**ファイル**: `backend/app/services/stub/vector_search_stub.py`

```python
import random
import logging
from typing import List, Dict
from app.services.stub.mock_data import MOCK_QA_DATABASE

logger = logging.getLogger(__name__)


class VectorSearchServiceStub:
    """Azure Cosmos DB Vector Search のスタブ実装"""

    def __init__(self):
        logger.info("[STUB] VectorSearchServiceStub 初期化")
        self.mock_qa_database = MOCK_QA_DATABASE.copy()

    async def search_similar_qa(
        self,
        query_vector: List[float],
        top_k: int = 5,
        similarity_threshold: float = 0.7
    ) -> List[Dict]:
        """
        ベクトル検索をモック

        Args:
            query_vector: クエリのベクトル（3072次元）
            top_k: 取得件数
            similarity_threshold: 類似度閾値

        Returns:
            List[Dict]: 検索結果（類似度スコア付き）
        """
        logger.info(
            f"[STUB] ベクトル検索実行: top_k={top_k}, "
            f"threshold={similarity_threshold}"
        )

        # 実際のベクトル検索の代わりに、ランダムにスコアを振ってソート
        results = []
        for qa in self.mock_qa_database:
            # モック類似度スコア（0.65〜0.95のランダム値）
            mock_score = random.uniform(0.65, 0.95)

            if mock_score >= similarity_threshold:
                result = qa.copy()
                result["vector_score"] = mock_score
                results.append(result)

        # スコア順にソート
        results.sort(key=lambda x: x["vector_score"], reverse=True)

        # 上位k件を返す
        top_results = results[:top_k]

        logger.info(
            f"[STUB] ベクトル検索完了: {len(top_results)}件取得 "
            f"(平均スコア: {sum(r['vector_score'] for r in top_results) / len(top_results):.2f})"
        )

        return top_results

    async def add_qa_to_index(self, qa_data: Dict, vector: List[float]) -> bool:
        """想定問答をインデックスに追加（モック）"""
        logger.info(f"[STUB] 想定問答を追加: id={qa_data.get('id')}")

        qa_with_vector = qa_data.copy()
        qa_with_vector["vector"] = vector
        self.mock_qa_database.append(qa_with_vector)

        return True

    async def delete_qa_from_index(self, qa_id: str) -> bool:
        """想定問答をインデックスから削除（モック）"""
        logger.info(f"[STUB] 想定問答を削除: id={qa_id}")

        self.mock_qa_database = [
            qa for qa in self.mock_qa_database if qa["id"] != qa_id
        ]

        return True
```

---

### 2.5 OpenAI Embedding API スタブ

**ファイル**: `backend/app/services/stub/embedding_stub.py`

```python
import random
import logging
from typing import List
import hashlib

logger = logging.getLogger(__name__)


class EmbeddingServiceStub:
    """OpenAI Embedding API のスタブ実装"""

    VECTOR_DIMENSION = 3072  # text-embedding-3-large の次元数

    def __init__(self):
        logger.info("[STUB] EmbeddingServiceStub 初期化")

    async def embed_text(self, text: str) -> List[float]:
        """
        テキストをEmbedding化（モック：決定的なランダムベクトル）

        Args:
            text: Embedding化するテキスト

        Returns:
            List[float]: 3072次元のベクトル（L2正規化済み）
        """
        logger.info(f"[STUB] Embedding生成: text={text[:50]}... (長さ: {len(text)}文字)")

        # テキストのハッシュ値をシードとして使用（同じテキストには同じベクトル）
        seed = int(hashlib.md5(text.encode()).hexdigest(), 16) % (2**32)
        random.seed(seed)

        # ランダムベクトル生成
        vector = [random.gauss(0, 1) for _ in range(self.VECTOR_DIMENSION)]

        # L2正規化（コサイン類似度計算用）
        norm = sum(x**2 for x in vector) ** 0.5
        normalized_vector = [x / norm for x in vector]

        logger.info(f"[STUB] Embedding生成完了: dimension={len(normalized_vector)}")

        return normalized_vector

    async def embed_texts_batch(self, texts: List[str]) -> List[List[float]]:
        """
        複数テキストをバッチでEmbedding化（モック）

        Args:
            texts: Embedding化するテキストのリスト

        Returns:
            List[List[float]]: 各テキストのベクトルのリスト
        """
        logger.info(f"[STUB] バッチEmbedding生成: {len(texts)}件")

        results = []
        for text in texts:
            vector = await self.embed_text(text)
            results.append(vector)

        logger.info(f"[STUB] バッチEmbedding生成完了: {len(results)}件")

        return results
```

---

### 2.6 Cohere Rerank API スタブ

**ファイル**: `backend/app/services/stub/rerank_stub.py`

```python
import random
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class RerankServiceStub:
    """Cohere Rerank API のスタブ実装"""

    def __init__(self):
        logger.info("[STUB] RerankServiceStub 初期化")

    def rerank_results(
        self,
        query: str,
        documents: List[Dict],
        top_n: int = 3
    ) -> List[Dict]:
        """
        検索結果をRerank（モック：ランダムスコアで再評価）

        Args:
            query: クエリテキスト
            documents: Rerankする文書リスト
            top_n: 返却する上位件数

        Returns:
            List[Dict]: Rerankされた文書リスト（スコア降順）
        """
        logger.info(
            f"[STUB] Rerank実行: query={query[:50]}..., "
            f"documents={len(documents)}件, top_n={top_n}"
        )

        if not documents:
            return []

        # 各文書にRerankスコアを付与（0.5〜1.0）
        reranked_docs = []
        for doc in documents:
            rerank_score = random.uniform(0.5, 1.0)

            doc_with_score = doc.copy()
            doc_with_score["rerank_score"] = rerank_score
            reranked_docs.append(doc_with_score)

        # スコア順にソート
        reranked_docs.sort(key=lambda x: x["rerank_score"], reverse=True)

        # 上位n件を返す
        top_docs = reranked_docs[:top_n]

        logger.info(
            f"[STUB] Rerank完了: {len(top_docs)}件返却 "
            f"(最高スコア: {top_docs[0]['rerank_score']:.2f})"
        )

        return top_docs
```

---

## 3. FastAPI エンドポイントでの使用例

**ファイル**: `backend/app/routers/qa.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import (
    get_answer_generator,
    get_vector_search_service,
    get_embedding_service,
    get_rerank_service
)
from pydantic import BaseModel

router = APIRouter(prefix="/api/qa", tags=["Q&A"])


class GenerateAnswerRequest(BaseModel):
    question: str
    summary_length: int = 100
    detail_length: int = 1000


class GenerateAnswerResponse(BaseModel):
    summary: str
    detail: str
    related_qa_count: int


@router.post("/generate-answer", response_model=GenerateAnswerResponse)
async def generate_answer(
    request: GenerateAnswerRequest,
    answer_generator=Depends(get_answer_generator),
    vector_search=Depends(get_vector_search_service),
    embedding=Depends(get_embedding_service),
    rerank=Depends(get_rerank_service)
):
    """
    質問に対する回答を生成（スタブ/本番自動切り替え）
    """
    try:
        # 1. 質問をEmbedding化
        query_vector = await embedding.embed_text(request.question)

        # 2. ベクトルDBで類似想定問答を検索（上位5件）
        search_results = await vector_search.search_similar_qa(
            query_vector=query_vector,
            top_k=5
        )

        # 3. Rerankで関連度を評価（上位3件）
        reranked_results = rerank.rerank_results(
            query=request.question,
            documents=search_results,
            top_n=3
        )

        # 4. 回答生成
        answer = await answer_generator.generate_answer(
            question=request.question,
            related_qa_pairs=reranked_results,
            summary_length=request.summary_length,
            detail_length=request.detail_length
        )

        return GenerateAnswerResponse(
            summary=answer["summary"],
            detail=answer["detail"],
            related_qa_count=len(reranked_results)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 4. テストとデバッグ

### 4.1 ログ出力の確認

すべてのスタブは `[STUB]` プレフィックス付きでログ出力するため、容易に識別可能:

```python
# ログ設定例
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 4.2 スタブのテストコード例

**ファイル**: `backend/tests/test_stubs.py`

```python
import pytest
from app.services.stub.speech_recognition_stub import SpeechRecognitionServiceStub
from app.services.stub.answer_generator_stub import AnswerGeneratorStub


@pytest.mark.asyncio
async def test_speech_recognition_stub():
    """音声認識スタブのテスト"""
    service = SpeechRecognitionServiceStub()

    results = []
    async for result in service.recognize_continuous(meeting_id="test_001"):
        results.append(result)

    assert len(results) > 0
    assert results[0].text is not None
    assert results[0].speaker_id is not None


@pytest.mark.asyncio
async def test_answer_generator_stub():
    """回答生成スタブのテスト"""
    service = AnswerGeneratorStub()

    answer = await service.generate_answer(
        question="今期の業績を教えてください",
        related_qa_pairs=[],
        summary_length=100,
        detail_length=1000
    )

    assert "summary" in answer
    assert "detail" in answer
    assert len(answer["summary"]) <= 150  # マージン考慮
    assert len(answer["detail"]) <= 1100
```

---

## 5. 本番実装への移行

### 5.1 移行チェックリスト

- [ ] 各サービスの本番実装が完了している
- [ ] 本番実装のインターフェースがスタブと一致している
- [ ] 環境変数 `USE_STUB=false` に設定
- [ ] 本番APIキー・接続文字列が設定されている
- [ ] 統合テストで本番実装の動作確認済み

### 5.2 段階的な移行

個別のサービスごとに段階的に本番実装へ切り替え可能:

```bash
# 例: Embeddingのみ本番、他はスタブ
USE_STUB=true
USE_STUB_EMBEDDING=false
```

---

## 6. 注意事項

### 6.1 セキュリティ

- スタブデータには **実在の企業情報・個人情報を含めない**
- 本番環境では必ず `USE_STUB=false` に設定
- APIキー等の秘密情報は `.env` ファイルで管理（gitignore必須）

### 6.2 パフォーマンス

- スタブは意図的に遅延を入れている（リアリティのため）
- 本番実装のパフォーマンステストは別途実施
- スタブの遅延時間は `asyncio.sleep()` の値で調整可能

### 6.3 データの一貫性

- スタブのモックデータは `mock_data.py` に集約
- 複数のスタブ間でデータの整合性を保つ
- 想定問答のIDは一意に管理

---

## 7. まとめ

本ドキュメントに従ってスタブを実装することで、以下が実現されます:

✅ Azureリソース・外部APIなしでの動作確認
✅ フロントエンド・バックエンドの並行開発
✅ 環境変数による簡単な本番/スタブ切り替え
✅ 依存性注入パターンによる保守性の高い設計
✅ ログ出力による動作確認の容易さ

スタブ実装により、プロトタイプ開発を加速し、要件定義の精度向上にも貢献します。
