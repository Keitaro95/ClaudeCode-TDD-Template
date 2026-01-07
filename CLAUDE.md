# CLAUDE.md - プロジェクト固有の情報

## プロジェクト概要

このプロジェクトは、スライドPDFから要件定義書を生成し、Claude Codeを活用して開発を進めるプロジェクトです。

## プロジェクト構成

- `SourcePDF/`: スライドPDFの格納場所
- `documents/`: OCR出力、要件定義書、タスク一覧などのドキュメント
- `.claude/agents/`: ドメインごとのサブエージェント定義
- `.claude/commands/`: カスタムスラッシュコマンド
- `.claude/settings.json`: ツール許可設定
- `.mcp.json`: MCPサーバー設定

## ワークフロー

1. OCR文字起こし: `SourcePDF/slides.pdf` → `documents/ocrOutput.md`
2. 要件定義書作成: `documents/ocrOutput.md` → `documents/requirements.md`
3. サブエージェント生成: `documents/requirements.md` → `.claude/agents/*.md`
4. 開発実装

## 使用技術・ツール

- Claude Code
- Context7 (MCP)
- Playwright (E2Eテスト用MCP)
- Git worktree

## 参考リンク

- スライド: https://docs.google.com/presentation/d/1SlKDv_NDMpav4LmQy-CVfrKTr3NbImc_HAltAFkj2iM/edit
- リポジトリ: https://github.com/AFG-Inc/cosmo-ir-2026
