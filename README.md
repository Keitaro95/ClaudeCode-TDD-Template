# Claude Code TDD テンプレート (Python)

## 概要

このプロジェクトは、**Claude Code でテスト駆動開発（TDD）を実践するための Python テンプレート**です。
Red-Green-Refactor サイクルを効率的に回すための環境とスキルが組み込まれています。

## 特徴

- ✅ **TDD専用スキル**: `/tdd` コマンド1つで SPEC → RED → GREEN → BLUE の4フェーズを全自動実行
- ⚡ **高速パッケージ管理**: [uv](https://docs.astral.sh/uv/) による爆速な依存関係管理
- 🔍 **Linter & Formatter**: Ruff + pre-commit による自動コード品質チェック
- 🧪 **pytest 統合**: テスト駆動開発に最適化された構成
- 📝 **プロジェクトルール**: `CLAUDE.md` による Claude Code への指示定義

## 必要要件

- **Python**: 3.12 以上
- **パッケージマネージャー**: [uv](https://docs.astral.sh/uv/)
- **OS**: macOS / Windows / Linux
- **Claude Code**: 最新版を推奨

## セットアップ

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. uv のインストール

```bash
# インストールスクリプト（macOS / Linux）
curl -LsSf https://astral.sh/uv/install.sh | sh

# macOS で Homebrew を使う場合
brew install uv
```

### 3. 依存関係のインストール

```bash
uv sync
```

### 4. pre-commit フックの設定

```bash
# Ruff と pre-commit をツールとしてインストール
uv tool install ruff
uv tool install pre-commit

# git hooks を有効化
pre-commit install
```

## TDD ワークフロー

### Claude Code で TDD を開始

Claude Code で以下のコマンドを実行するだけで、**4フェーズのサイクルが全自動で進みます**：

```
/tdd
```

あとは Claude の質問に答えるだけで、SPEC → RED → GREEN → BLUE の全フェーズを Claude が自律的に実行します。

---

### 全自動で起こること：4フェーズの詳細

#### フェーズ 0: SPEC — test仕様書を生成する（`tdd-spec-writer` エージェント）

1. `docs/**/feature-*.md` を Glob 検索し、feature仕様書の一覧を表示する
2. ユーザーが対象の feature 仕様書を選択する
3. 参考にする既存の実装コードがあればパスを確認する（任意）
4. 開始内容（仕様書パス・出力先・テスト配置先）を表示してユーザーの確認を取る
5. feature仕様書を読み込み、機能の振る舞いをテストシナリオに変換する
6. `docs/**/ test-*.md` としてテスト仕様書を生成・保存する（AAAパターンに対応したシナリオ構造）
7. 生成したテストシナリオ一覧をユーザーに提示し、次フェーズへの進行を確認する

> **出力形式**: `STATUS / FEATURE_FILE / TEST_SPEC_FILE / SCENARIOS件数 / SUMMARY` のみを返す（仕様書全文は返さない）

---

#### フェーズ 1: RED — 失敗するテストを書く（`tdd-test-writer-red` エージェント）

1. フェーズ0で生成したテスト仕様書（`docs/**/test-*.md`）を読み込む
2. テストシナリオから **1つだけ** 選んでユーザーに確認する
3. `tests/{ミラーパス}/test_*.py` にAAAパターン（Arrange / Act / Assert）でテストコードを書く
   - `conftest.py` の共通 fixture を活用する
   - モック・スタブは使わず、実装を前提としたテストを書く
4. `uv run pytest <test-file>` を実行し、**テストが失敗することを確認する**
5. テストファイルパスと失敗出力をサマリーとして返す

> **1テスト1振る舞いの原則**を厳守。テストリスト全体を一度に実装しない。

---

#### フェーズ 2: GREEN — テストを通す最小限の実装（`tdd-implementer-green` エージェント）

1. 失敗しているテストファイルと対応する実装ファイル（`src/{対応パス}`）**のみ**を読み込む
2. テストが期待する振る舞いを理解し、それを満たす**最小限のコード**を実装する
3. `uv run pytest <test-file>` を実行し、**テストが成功することを確認する**
4. 実装の概要とテスト成功のサマリーを返す

> **NG**: アサーション削除・期待値コピー・リファクタリングの混入は禁止。テストを通すことだけに集中する。

途中で以下に気づいた場合はユーザーに確認する：
- 新しいテストが必要になった
- テストコードに抜け漏れがある
- テストリストの消し込みタイミング

---

#### フェーズ 3: BLUE — リファクタリング評価・実施（`tdd-refactorer-blue` エージェント）

1. GREEN フェーズで編集した実装ファイルとテストファイルを読み込む
2. リファクタリングチェックリストで評価する：
   - 関数の抽出（3回以上の重複パターン）
   - 条件分岐の簡略化
   - 命名の改善（意図が不明瞭な変数名・関数名）
   - レイヤー違反（UIにビジネスロジックが含まれているなど）
3. 有益な改善があれば適用する。過剰な抽象化・早すぎる汎用化は行わない
4. `uv run pytest <test-file>` を実行し、**テストが成功し続けることを確認する**
5. 変更サマリーまたは「リファクタリング不要」の理由を返す

> 抽象化の判断が難しい場合はユーザーに確認してから実施する。

---

### 1サイクル完了後

1サイクル（SPEC → RED → GREEN → BLUE）完了後、Claude は：

1. 完了したテストシナリオをユーザーに報告する
2. test仕様書に残りのシナリオがあれば一覧を提示する
3. 次のテストシナリオを続けるか、終了するかをユーザーに確認する

**推奨**: 3〜5サイクル連続実行した場合は `/reset` でコンテキストをクリアする。

---

### ディレクトリのミラールール

`docs/` の構造を `tests/` にそのままミラーしてテストコードを配置します：

| docs パス | tests パス | src パス |
|-----------|------------|----------|
| `docs/backend/services/rag/` | `tests/backend/services/rag/` | `src/backend/services/rag.py` |
| `docs/backend/services/speech/` | `tests/backend/services/speech/` | `src/backend/services/speech.py` |
| `docs/backend/services/stream/` | `tests/backend/services/stream/` | `src/backend/services/stream.py` |
| `docs/frontend/app/pages/officer/` | `tests/frontend/app/pages/officer/` | `src/frontend/app/pages/2_officer_app.py` |
| `docs/frontend/app/pages/operator/` | `tests/frontend/app/pages/operator/` | `src/frontend/app/pages/1_operator_app.py` |

---

### テストの実行

```bash
# 全テスト実行
uv run pytest

# 詳細表示
uv run pytest -v

# 特定のテストファイル
uv run pytest tests/test_example.py
```

## プロジェクト構成

```
.
├── .claude/
│   └── skills/           # TDD スキル定義
├── src/                  # ソースコード
├── tests/                # テストコード
│   ├── backend/
│   └── frontend/
├── CLAUDE.md             # Claude Code へのプロジェクト指示
├── pyproject.toml        # Python プロジェクト設定 + Ruff 設定
├── .pre-commit-config.yaml  # pre-commit 設定
└── README.md
```

## 開発ツール

### テストの実行

```bash
# 全テスト実行
uv run pytest

# 詳細表示
uv run pytest -v

# ディレクトリ単位で実行
uv run pytest tests/backend/
uv run pytest tests/frontend/

# 特定のテストファイル
uv run pytest tests/test_example.py -v

# カバレッジ付きで実行
uv run pytest --cov=src --cov-report=html
```

### コードフォーマット

```bash
# uv 標準のフォーマッター（black 互換）
uv fmt
```

### Linter（Ruff）と pre-commit

Ruff を linter として使用し、pre-commit で git commit 時に自動修正を行います。

#### 手動実行

```bash
# lint チェック
ruff check

# lint チェック + 自動修正
ruff check --fix

# 全ファイルに対して pre-commit を実行
pre-commit run --all-files
```

#### 設定ファイル

- **Ruff 設定**: [pyproject.toml](pyproject.toml) の `[tool.ruff]` セクション
- **pre-commit 設定**: [.pre-commit-config.yaml](.pre-commit-config.yaml)

### 依存関係の追加

```bash
uv add <package-name>

# 開発用依存関係（テストツールなど）
uv add --group dev <package-name>
```

## TDD スキルの使い方

### 利用可能なスキル

| スキル名 | 説明 |
|---------|------|
| `tdd` | SPEC→RED→GREEN→BLUE の4フェーズを全自動で実行 |

### 基本的な使い方

```
# Claude Code で TDD を開始（これだけで全フェーズが全自動で進む）
/tdd
```

### Claude Code への指示

プロジェクト固有のルールは [CLAUDE.md](CLAUDE.md) に記載されています。
Claude Code は自動的にこのファイルを読み込み、ルールに従って動作します。

## オプション: Playwright MCP のセットアップ

E2Eテストやブラウザ操作が必要な場合、Playwright MCP を使用できます。

### インストール

```bash
npm install @playwright/test
npx playwright install
```

### MCP 設定ファイル

**注意**: Playwright MCP は使っていなくてもコンテキストを消費します。
使わない時は `.mcp.json` を削除し、Claude Code を再起動してください。

必要になったらプロジェクトルートに `.mcp.json` を作成：

```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--headless",
        "--isolated",
        "--browser",
        "chromium"
      ]
    }
  }
}
```

## カスタマイズ

### CLAUDE.md の編集

[CLAUDE.md](CLAUDE.md) を編集することで、Claude Code の動作をカスタマイズできます：

- コーディング規約
- 使用するライブラリやフレームワーク
- テスト戦略
- プロジェクト固有のルール

### TDD スキルの調整

`.claude/skills/` 以下のスキル定義をプロジェクトに合わせてカスタマイズできます。

## 技術スタック

| カテゴリ | 技術 |
|---------|------|
| 言語 | Python 3.12+ |
| パッケージ管理 | uv |
| テスティング | pytest |
| Linter | Ruff |
| Formatter | uv fmt (black 互換) |
| pre-commit | pre-commit hooks |
| TDD | Claude Code TDD スキル |

## ライセンス

このテンプレートは自由に使用・改変できます。
プロジェクト固有のライセンスを適用してください。
