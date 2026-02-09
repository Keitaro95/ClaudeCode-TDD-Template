# Claude Code TDD テンプレート (Python)

## 概要

このプロジェクトは、**Claude Code でテスト駆動開発（TDD）を実践するための Python テンプレート**です。
Red-Green-Refactor サイクルを効率的に回すための環境とスキルが組み込まれています。

## 特徴

- ✅ **TDD専用スキル**: Claude Code の TDD スキル (`tdd-integration-new`) を使った対話型開発
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

1. Claude Code で以下のコマンドを実行：

```
/tdd-integration-new
```

2. Claude がテスト対象を対話的に絞り込みます
3. **RED フェーズ**: 失敗するテストを書く
4. **GREEN フェーズ**: テストを通す最小限の実装
5. **BLUE (Refactor) フェーズ**: コード品質を改善

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
| `tdd-integration-new` | TDD の Red-Green-Refactor サイクルを対話的に実行 |
| `tdd-style-commands:red-from-sample` | サンプルコードから仕様を言語化し、RED スケルトンを生成 |
| `tdd-style-commands:start-from-red` | RED テスト仕様書から TDD を開始 |

### 基本的な使い方

```
# Claude Code で TDD を開始
/tdd-integration-new

# サンプルコードから TDD を始める
/tdd-style-commands:red-from-sample

# 既存の RED 仕様書から始める
/tdd-style-commands:start-from-red
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
