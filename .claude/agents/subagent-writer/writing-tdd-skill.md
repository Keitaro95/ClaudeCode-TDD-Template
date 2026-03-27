
prompt：
```sh
以下の"""テンプレートプロンプト"""を書き換えましょう。
具体的には
## 日本語でpython用に書く。ただし、テンプレートは厳格すぎるので、強度については私に聞いてください。
これは英語web記事のvueプロジェクトの例です。
テンプレートと全く同じ構成で
フェーズごとTDDデリバリーになるようなskillを**日本語で**書きます。
subagentの名前もそのままです。
ただし、テンプレートは厳格すぎるので、強度については私に聞いてください。

1. phase1: red code用 subagent
2. phase2: green code用 subagent
3. phase3: blue code用 subagent

各フェーズには「…まで先に進まないでください」という明確なゲートがある。
これは大事なのでそのまま残す。
🔴🟢🔵の絵文字で、出力で進捗状況を簡単に把握できるのも残す。

## トリガーフレーズが含まれているdescriptionフィールドの厳格さを排除
「新しいfeatureやfunctionを実装するように指示すると、クロードは自動的にこのスキルを起動します。」
とあるけど、そこまで厳格じゃなくていい。
「このスキルを使ってね」claudeに指示した時に、実行されればいい。
```



"""テンプレートプロンプト"""：
```sh
---
name: tdd-integration
description: Enforce Test-Driven Development with strict Red-Green-Refactor cycle using integration tests. Auto-triggers when implementing new features or functionality. Trigger phrases include "implement", "add feature", "build", "create functionality", or any request to add new behavior. Does NOT trigger for bug fixes, documentation, or configuration changes.
---

# TDD Integration Testing

Enforce strict Test-Driven Development using the Red-Green-Refactor cycle with dedicated subagents.

## Mandatory Workflow

Every new feature MUST follow this strict 3-phase cycle. Do NOT skip phases.

### Phase 1: RED - Write Failing Test

🔴 RED PHASE: Delegating to tdd-test-writer...

Invoke the `tdd-test-writer` subagent with:
- Feature requirement from user request
- Expected behavior to test

The subagent returns:
- Test file path
- Failure output confirming test fails
- Summary of what the test verifies

**Do NOT proceed to Green phase until test failure is confirmed.**

### Phase 2: GREEN - Make It Pass

🟢 GREEN PHASE: Delegating to tdd-implementer...

Invoke the `tdd-implementer` subagent with:
- Test file path from RED phase
- Feature requirement context

The subagent returns:
- Files modified
- Success output confirming test passes
- Implementation summary

**Do NOT proceed to Refactor phase until test passes.**

### Phase 3: REFACTOR - Improve

🔵 REFACTOR PHASE: Delegating to tdd-refactorer...

Invoke the `tdd-refactorer` subagent with:
- Test file path
- Implementation files from GREEN phase

The subagent returns either:
- Changes made + test success output, OR
- "No refactoring needed" with reasoning

**Cycle complete when refactor phase returns.**

## Multiple Features

Complete the full cycle for EACH feature before starting the next:

Feature 1: 🔴 → 🟢 → 🔵 ✓
Feature 2: 🔴 → 🟢 → 🔵 ✓
Feature 3: 🔴 → 🟢 → 🔵 ✓

## Phase Violations

Never:
- Write implementation before the test
- Proceed to Green without seeing Red fail
- Skip Refactor evaluation
- Start a new feature before completing the current cycle
```