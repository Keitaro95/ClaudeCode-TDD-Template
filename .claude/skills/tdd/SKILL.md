---
name: tdd
description: テスト駆動開発（TDD）の0spec-1red-2green-3blueサイクルを実施します。対話でテスト対象を絞り込み、コンテキスト消費を最小化します。
---

# TDD 統合スキル（コンテキスト最適化版）

専用のサブエージェント（`.claude/agents/tdd/`）を使用して、テスト駆動開発の4フェーズサイクルを実施します。

## サブエージェント一覧

| フェーズ | ファイル | 役割 |
|----------|----------|------|
| 0spec | `0spec.md`  | feature仕様書 → test仕様書の生成 |
| 1red | `1red.md` | 失敗するテストコードを書く |
| 2green | `2green.md` | テストを通す最小限の実装 |
| 3blue | `3blue.md` | リファクタリング評価・実施 |

---

## 対話フロー（必須）

TDDを開始する前に、以下の対話を行ってください。

### ステップ1: feature仕様書（green code仕様）の提示を求める

```
TDDを開始します。

まず、feature仕様書（green code仕様）のパスを教えてください。
docs/ 配下にある feature-*.md ファイルです。

現在あるfeature仕様書:
```

`docs/**/feature-*.md` をGlobで検索し、一覧を表示してください。

### ステップ2: 参考コードの確認

```
参考にする既存の実装コードがあれば、パスを教えてください。
（なければ「なし」で進めます）
```

### ステップ3: 確認して開始

ユーザーがfeature仕様書を選択したら、以下を確認表示してから開始します：

```
以下の内容でTDDを開始します：

- feature仕様書: {選択されたパス}
- 参考コード: {パスまたは「なし」}
- test仕様書出力先: {feature仕様書と同じディレクトリの test-*.md}
- テストコード配置先: tests/{ミラーパス}/test_*.py
- 実装コード: src/{対応パス}

よろしいですか？
```

---

## ディレクトリのミラールール

docs の構造を tests にミラーしてテストコードを配置します：

| docs パス | tests パス | src パス |
|-----------|------------|----------|
| `docs/backend/services/rag/` | `tests/backend/services/rag/` | `src/backend/services/rag.py` |
| `docs/backend/services/speech/` | `tests/backend/services/speech/` | `src/backend/services/speech.py` |
| `docs/backend/services/stream/` | `tests/backend/services/stream/` | `src/backend/services/stream.py` |
| `docs/frontend/app/pages/officer/` | `tests/frontend/app/pages/officer/` | `src/frontend/app/pages/2_officer_app.py` |
| `docs/frontend/app/pages/operator/` | `tests/frontend/app/pages/operator/` | `src/frontend/app/pages/1_operator_app.py` |

---

## フェーズ0: SPEC - test仕様書を書く

📝 SPECフェーズ: `tdd-spec-writer` サブエージェント (`0spec.md`) に委任

### 入力
- ユーザーが選択したfeature仕様書（`docs/**/feature-*.md`）
- 参考コード（任意）

### 処理
feature仕様書を読み取り、テストシナリオに変換して `docs/**/test-*.md` に出力する。

### コンテキスト制限（厳守）

サブエージェントは以下の情報**のみ**を返してください：

```
---
STATUS: SPEC_CREATED / SPEC_FAILED
FEATURE_FILE: docs/xxx/feature-yyy.md
TEST_SPEC_FILE: docs/xxx/test-yyy.md
SCENARIOS: N件のテストシナリオを生成
SUMMARY: 生成内容の要約（1-2行）
---
```

### 完了条件
test仕様書が生成されたら、ユーザーにテストシナリオ一覧を提示し、次のフェーズへの進行を確認する。

---

## フェーズ1: RED - 失敗するテストを書く

🔴 REDフェーズ: `tdd-test-writer-red` サブエージェント (`1red.md`) に委任

### 入力
- フェーズ0で生成されたtest仕様書（`docs/**/test-*.md`）
- ユーザーが選択した1つのテストシナリオ
- テスト配置場所（`tests/{ミラーパス}/`）

### コンテキスト制限（厳守）

```
---
STATUS: RED_CONFIRMED / RED_FAILED
FILE: tests/xxx/test_yyy.py
TEST_NAME: test_機能名
SUMMARY: 期待通り失敗した理由（1行）
---
```

### 完了条件
テストが失敗することを確認してから次のフェーズへ進む。

---

## フェーズ2: GREEN - テストを通す

🟢 GREENフェーズ: `tdd-implementer-green` サブエージェント (`2green.md`) に委任

### 入力
- REDフェーズで作成したテストファイルのパス
- 実装対象ファイル（`src/{対応パス}`）
- **テストファイルと実装ファイルのみ**を読み込む

### コンテキスト制限（厳守）

```
---
STATUS: GREEN_CONFIRMED / GREEN_FAILED
FILE: src/xxx/yyy.py
TEST_FILE: tests/xxx/test_yyy.py
CHANGES: 変更内容の要約（1-2行）
---
```

### 完了条件
テストが成功することを確認してから次のフェーズへ進む。

---

## フェーズ3: BLUE - リファクタリング

🔵 BLUEフェーズ: `tdd-refactorer-blue` サブエージェント (`3blue.md`) に委任

### 入力
- GREENフェーズで編集した実装ファイルのみ
- 対応するテストファイル

### コンテキスト制限（厳守）

```
---
STATUS: REFACTOR_DONE / NO_REFACTOR_NEEDED
FILE: src/xxx/yyy.py
CHANGES: 変更内容（1-2行）または「リファクタリング不要」
REASON: 理由（1行）
TEST_STATUS: PASSED
---
```

---

## フェーズ違反

以下を絶対に行わないでください:

- テストより先に実装を書く
- SPEC（test仕様書）なしにREDに進む
- REDの失敗を確認せずにGREENに進む
- BLUE評価をスキップする
- 選択されたディレクトリ以外のファイルを読み書きする
- サブエージェントがログ全文を返す

---

## サイクル完了後

1つのテストに対する0spec-1red-2green-3blueサイクルが完了したら：

1. 完了したテストシナリオをユーザーに報告
2. test仕様書に残りのシナリオがあれば提示
3. ユーザーが次のテストを選択するか、終了するか確認

**推奨**: 複数テストを連続実行する場合、3-5サイクルごとに `/reset` でコンテキストをクリアすることを推奨します。
