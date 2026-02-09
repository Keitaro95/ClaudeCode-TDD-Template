# FastAPI テスト戦略ガイド

---

## 1. テスト全体方針

### 1.1 推奨されるプロジェクト構造：ミラーリング構成

テストコードの配置戦略として、最も保守性が高いとされるのが「ミラーリング構成（Mirroring Structure）」である。これは、アプリケーションコード（app または src ディレクトリ）の階層構造を、テストディレクトリ（tests）内で完全に模倣する手法です。

#### 構造例と解説
```
project_root/
├── app/
│ ├── __init__.py
│ ├── main.py # アプリケーションエントリーポイント
│ ├── api/
│ │ ├── dependencies.py # 依存性注入定義
│ │ ├── routers/ # ルーター定義
│ │ └── v1/
│ ├── core/
│ │ ├── config.py # Pydantic Settings
│ │ └── exceptions.py # カスタム例外
│ ├── services/ # ビジネスロジック
│ └── db/ # データベース関連
├── tests/
│ ├── __init__.py
│ ├── conftest.py # グローバルフィクスチャ（Sessionスコープ等）
│ ├── unit/ # 単体テスト
│ │ ├── services/ # app/servicesに対応
│ │ │ └── test_auth_service.py
│ │ └── core/ # app/coreに対応
│ ├── integration/ # 統合テスト
│ │ ├── api/ # app/apiに対応
│ │ │ └── test_items.py
│ │ └── db/
│ └── performance/ # パフォーマンステスト（pytest-benchmark）
│ └── test_latency.py
└── pytest.ini # pytest設定
```

この構造の利点：
- **検索性の向上**: app/services/auth.py を修正した際、開発者は直感的に tests/unit/services/test_auth_service.py を修正すべきであると認識できます。
- **スコープの明確化**: 単体テスト（Unit）と統合テスト（Integration）をディレクトリレベルで分離することで、CIパイプラインにおいて「高速な単体テストのみ先に実行する」といった最適化が容易になります。

### 1.2 app.dependency_overrides のメカニズムと優位性

従来のPythonテストでは unittest.mock.patch を用いてインポートパスを書き換える手法が一般的であった。しかし、FastAPIにおいては app.dependency_overrides 属性を使用することが強く推奨される。

#### patch に対する dependency_overrides の優位性:
- **リファクタリング耐性**: patch は対象の関数がどこでインポートされているか（実装の詳細）に依存する。インポートの場所が変わるとテストが壊れる。対して dependency_overrides は、依存関数の定義そのものをキーとするため、利用場所が変わってもテストは壊れない。
- **スコープの安全性**: dependency_overrides はFastAPIのDIコンテナレベルでの差し替えであり、グローバルな名前空間を汚染しない。

### 1.3 コンテキストマネージャーによるオーバーライドの安全管理

app.dependency_overrides は辞書（dict）であり、テスト終了後にクリーンアップ（キーの削除）を行わないと、後続のテストにモックが残り続ける「テスト汚染」が発生する。これを防ぐため、yield フィクスチャまたはコンテキストマネージャーを用いた管理をチーム標準とすべきである。

#### 推奨実装パターン（フィクスチャファクトリ）:

```python
# tests/conftest.py

import pytest
from fastapi import FastAPI
from app.main import app as fastapi_app

@pytest.fixture
def override_dependency():
    """
    テストケース内で一時的に依存関係をオーバーライドし、自動的に解除するフィクスチャ。
    """
    overrides_to_restore = {}

    def _override(dependency, replacement):
        overrides_to_restore[dependency] = fastapi_app.dependency_overrides.get(dependency)
        fastapi_app.dependency_overrides[dependency] = replacement

    yield _override

    # テアダウン: 変更された依存関係のみを復元・削除
    for dep, original in overrides_to_restore.items():
        if original is None:
            fastapi_app.dependency_overrides.pop(dep, None)
        else:
            fastapi_app.dependency_overrides[dep] = original
```

### 1.4 TestClient / AsyncClient / AsyncMock 使い分けポイント

#### TestClient（同期）
- **用途**: シンプルなエンドポイントのテスト
- await 不要で書きやすい
- 内部で非同期を同期に変換して実行
- 単純なCRUD操作の検証に最適

#### AsyncClient（非同期）
- **用途**: 複雑な非同期処理のテスト
- @pytest.mark.asyncio + await で記述
- 本番と同じ非同期の実行モデルでテスト
- **必須となるケース**:
  - 並行リクエスト（asyncio.gather）
  - WebSocket / SSE
  - タイミング依存のバグ検出

#### AsyncMock
- **用途**: 非同期関数のモック（代替物）
- async def で定義された依存関係を差し替える
- await で呼び出せるモックを作成
- **使う場面**:
  - DBアクセスのモック
  - 外部APIのモック
  - タイムアウト/リトライのテスト

#### 早見表

| 何をテストする？ | 使うもの |
|---|---|
| 単純なGET/POST | TestClient |
| 並行処理・WebSocket | AsyncClient |
| DB・外部APIの差し替え | AsyncMock |

#### 一言まとめ
- **TestClient**: 手軽に書きたいとき
- **AsyncClient**: 本番と同じ動きを再現したいとき
- **AsyncMock**: 非同期の依存を差し替えたいとき

#### 状況別の推奨選択

```
テストを書く
    │
    ▼
外部依存（DB/API）がある？
    │
    ├─ YES → AsyncMock で依存をモック
    │
    ▼
非同期処理が複雑？（並行処理/WebSocket/SSE）
    │
    ├─ YES → AsyncClient + @pytest.mark.asyncio
    │
    ├─ NO → TestClient（同期）でOK
    │
    ▼
チームの方針は？
    │
    ├─ 統一したい → AsyncClient に統一
    │
    └─ シンプルさ優先 → TestClient をベースに
```

---

## 2. 異常系テスト方針と詳細

### 2.1 with構文を用いた例外処理のテスト

#### pytest.raisesによる例外検証
Pytestではwith pytest.raises(ExceptionType):構文を使って、特定の例外が発生することをテストします。以下は、入力値が不正な場合にValueErrorを送出する関数をテストする例です:

```python
import pytest

def target(x: int):
    if x > 100:
        raise ValueError("不正な値です")
    return x * 2

def test_target_raises():
    # 101を渡すとValueErrorが発生することを検証
    with pytest.raises(ValueError) as e:
        target(101)
    # 発生した例外メッセージを確認
    assert str(e.value) == "不正な値です"
```

上記のようにpytest.raisesのコンテキストマネージャ内で関数を呼び出し、期待する例外クラスを指定します。e.value経由で例外オブジェクトにアクセスし、メッセージ等も検証可能です。

#### 例外テストの注意点
pytest.raises()にはできるだけ具体的な例外クラスを指定します。例えば単にExceptionを指定してしまうと、想定外の例外まで捕捉してしまいテストの意図が曖昧になります。また、withブロック内では例外発生までのコードのみを書き、後続のアサーションはブロックの外に出す必要があります（上記コードでも、assertはwith文と同じインデントにしている点に注意してください）。

#### 例外発生をアサートする例

```python
def test_service_raises_on_error(mocker):
    mocker.patch('myapp.service.call_api', side_effect=ValueError("bad data"))
    # call_api内でValueErrorが起きた場合、target_functionもValueErrorをそのまま送出する想定
    with pytest.raises(ValueError, match="bad data"):
        target_function()  # 内部で call_api() を呼ぶ関数
```

上記のようにwith pytest.raises(ValueError)を使うことで、想定した例外が発生することをテストできます。

### 2.2 FastAPI 異常系テスト設計ガイド

#### 基本的な考え方
異常系テストの目的は「エラーが起きたとき、システムが正しく振る舞うか」を検証すること。具体的には：

- 適切なステータスコードを返しているか
- ユーザーへのメッセージは適切か（詳細すぎない）
- 内部ログに詳細が記録されているか

### 2.3 ステータスコード別テスト設計

#### 400 Bad Request（ビジネスルール違反）
**発生条件**: アプリケーションが明示的に raise HTTPException(400) するケース

```python
def test_duplicate_item_error(client):
    """重複登録を拒否することを検証"""
    # 1回目: 正常登録
    client.post("/items/", json={"name": "unique_item"})

    # 2回目: 同じ名前で登録試行
    response = client.post("/items/", json={"name": "unique_item"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Item already exists"
```

#### 401 Unauthorized（認証失敗）
**発生条件**: トークンなし、トークン切れ、認証情報不正

```python
def test_missing_auth_token(client):
    """認証トークンなしでアクセス拒否されることを検証"""
    response = client.get("/protected/resource")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_expired_token(client):
    """期限切れトークンが拒否されることを検証"""
    expired_token = "eyJ..."  # 期限切れトークン
    response = client.get(
        "/protected/resource",
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    assert response.status_code == 401
```

#### 403 Forbidden（権限不足）
**発生条件**: 認証済みだがアクセス権がない

```python
def test_insufficient_permissions(client, normal_user_token):
    """一般ユーザーが管理者機能にアクセスできないことを検証"""
    response = client.delete(
        "/admin/users/123",
        headers={"Authorization": f"Bearer {normal_user_token}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"
```

#### 404 Not Found（リソース不在）
**発生条件**: 指定されたリソースが存在しない

```python
def test_item_not_found(client):
    """存在しないIDでアクセスした場合を検証"""
    response = client.get("/items/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
```

#### 422 Unprocessable Entity（バリデーションエラー）
**発生条件**: Pydanticによる入力値検証の失敗（FastAPIが自動生成）

```python
def test_validation_error_missing_field(client):
    """必須フィールド欠落時のエラーを検証"""
    response = client.post("/items/", json={"price": 100})  # nameが欠落

    assert response.status_code == 422
    errors = response.json()["detail"]

    # どのフィールドでエラーが起きたか確認
    assert any(e["loc"] == ["body", "name"] for e in errors)
    assert any(e["type"] == "missing" for e in errors)


def test_validation_error_invalid_type(client):
    """型不正時のエラーを検証"""
    response = client.post("/items/", json={"name": "test", "price": "not_a_number"})

    assert response.status_code == 422
```

#### 500 Internal Server Error（サーバー内部エラー）
**発生条件**: 予期しない例外、DB接続エラーなど

```python
from unittest.mock import MagicMock
from sqlalchemy.exc import OperationalError

def test_db_connection_error(client, override_dependency, caplog):
    """DB接続エラー時の挙動を検証"""

    # エラーを発生させるモックを作成
    def raise_error():
        raise OperationalError("Connection failed", params=None, orig=None)

    override_dependency(get_db, raise_error)

    response = client.get("/items/")

    # ユーザーには汎用メッセージを返す（セキュリティ）
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}

    # 内部ログには詳細が残っている（デバッグ用）
    assert "Connection failed" in caplog.text
```

#### 503 Service Unavailable（サービス利用不可）
**発生条件**: 外部サービス障害、メンテナンス中

```python
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_external_api_unavailable(async_client, override_dependency):
    """外部API障害時の挙動を検証"""

    mock_api = AsyncMock()
    mock_api.fetch_data.side_effect = TimeoutError("External API timeout")

    override_dependency(get_external_api, lambda: mock_api)

    response = await async_client.get("/data")

    assert response.status_code == 503
    assert "unavailable" in response.json()["detail"].lower()
```

### 2.4 異常系テストの設計マトリクス

| ステータス | 何をテストする | モック必要？ |
|---|---|---|
| 400 | ビジネスルール違反 | 場合による |
| 401 | 認証なし/失敗 | トークン生成 |
| 403 | 権限不足 | ユーザー権限 |
| 404 | リソース不在 | 不要 |
| 422 | 入力値不正 | 不要 |
| 500 | 内部エラー | 必要（例外発生） |
| 503 | 外部障害 | 必要（タイムアウト） |

### 2.5 重要なポイント

#### 1. ユーザーへの情報とログの分離
```
ユーザーへ: 「Internal Server Error」（詳細を隠す）
ログへ:    「SQLAlchemy OperationalError: Connection refused...」（詳細を残す）
```

#### 2. 422 と 400 の使い分け
- **422**: Pydanticが自動で返す（入力形式の問題）
- **400**: アプリが明示的に返す（ビジネスロジックの問題）

#### 3. MagicMock vs AsyncMock
- **同期関数のモック**: MagicMock + side_effect
- **非同期関数のモック**: AsyncMock + side_effect

---

## 3. LOGとパフォーマンス

### 3.1 パフォーマンス解析と応答時間の検証

機能テストがパスしても、応答時間が許容範囲を超えていれば実運用には耐えられない。CIパイプラインの中でパフォーマンスの退行（Performance Regression）を検知する仕組みを組み込む。

### 3.2 ミドルウェアによる簡易レイテンシ計測

全リクエストの処理時間を計測し、レスポンスヘッダー（X-Process-Time）に付与するミドルウェアは、運用監視だけでなくテスト時の簡易チェックにも有用である。

```python
# app/middleware.py
import time
from fastapi import Request

async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

#### テストコードでのアサーション:

```python
def test_api_latency_threshold(client):
    response = client.get("/fast-endpoint")
    assert response.status_code == 200

    latency = float(response.headers["X-Process-Time"])
    # 閾値判定: ただしCI環境の変動を考慮し、余裕を持たせるかWarning扱いにする
    assert latency < 0.5, f"Performance degradation detected: {latency}s"
```

### 3.3 pytest-benchmark による統計的パフォーマンス解析

より厳密なパフォーマンス測定には、pytest-benchmark プラグインを導入する。これはコードブロックを複数回実行し、平均、最小、最大、標準偏差を算出する。

#### 特徴と利点:
- **統計的信頼性**: 1回の実行ではなく、多数回の試行に基づくため、外れ値の影響を排除できる。
- **比較機能**: 前回のテスト実行結果（ベースライン）と比較し、有意に遅くなった場合のみテストを失敗させる設定が可能。

#### 実装例:

```python
def test_heavy_computation(benchmark):
    # benchmark() は渡された関数を実行し、統計情報を収集する
    result = benchmark(heavy_function, arg1, arg2)
    assert result == expected_output
```

#### チーム運用ルール:
ベンチマークテストは実行時間が長くなる傾向があるため、通常の開発サイクル（pytest）からは除外し、タグ付け（@pytest.mark.benchmark）を行って、専用のCIジョブやリリース前の負荷テストフェーズで実行するように pytest.ini で制御するのが一般的である。

### 3.4 ログ出力の検証方法

#### caplogフィクスチャの活用
pytestにはログ出力を捕捉する組み込みフィクスチャcaplogがあります。caplogを使うと、テスト中に発生したログメッセージを記録し、内容やレベルを検証できます。たとえば、ある関数がエラー時にロガーにエラーメッセージを出力することをテストするには以下のようにします:

```python
import logging

def function_under_test():
    logger = logging.getLogger("myapp")
    logger.error("致命的なエラー発生")

def test_logs_error(caplog):
    # WARNING以上のログをキャプチャ（デフォルトでWARNING以上が対象）
    function_under_test()
    # 指定のエラーログが出力されたか確認
    assert ("myapp", logging.ERROR, "致命的なエラー発生") in caplog.record_tuples
```

上記では、function_under_test()内で出力されたERRORレベルのログをcaplog.record_tuples（タプルのリスト）から検出しています。デフォルトではWARNING以上のログが捕捉されるため、ERRORは自動的に記録されます。必要に応じてcaplog.set_level(logging.INFO)のようにログレベルを下げれば、INFOやDEBUGログもテスト可能です。

ログの検証方法は他にもあり、caplog.textで全ログテキストを一括取得して部分文字列マッチすることもできます。また、各ログの詳細（logger名、レベル、メッセージ）はcaplog.recordsのリストから取り出せます。上の例では簡便さからrecord_tuplesでタプル比較をしていますが、より厳密に検証したければany()関数でrecord.levelnameやrecord.getMessage()をチェックする方法もあります。
