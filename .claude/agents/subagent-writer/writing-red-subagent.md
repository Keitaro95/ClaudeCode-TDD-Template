
red code

prompt：
```sh
以下の"""テンプレートプロンプト"""を書き換えましょう。
具体的には以下のことを盛り込むこと

## 日本語でpython用に書く
これは英語web記事のvueプロジェクトの例です。
テンプレートと全く同じ構成で**日本語で**書きます。
さらにuvなど決まったコマンドを使う
**コマンドはCLAUDE.md　にあるものを使うよう従うこと。**
**テストlistは ./testsにおく**

## red code用のsubagent
**失敗するテストをひとつ書く red code**
テストには実装したいコードの**振る舞い**を記述する。  
コードが期待する動作をリストアップする。  

「正常系はこうで、もしもサービスがタイムアウトしたらこうして、データベースにキーがまだないときはこうする。あとは……」
コード変更後、満たすべき振る舞い・様々な動作を網羅的に考えよう。  
同時に、振る舞いの変更が既存の動作を壊さないようにもする。

それらがある一つのスクリプトについて、テストリストになります。

テストをひとつ。準備と実行と検証（アサーション）が備わった、本当の本当に自動化されたテストを「ひとつだけ」書く
assertErrorを吐くコードを書く
テストコードを
まず起こしたいアサーションエラーから書き始める
そうして
上に向かってred code テストコードを書く逆向きに書き進めてみる


NG: コードカバレッジを上げるためだけに、アサーションのないテストコードを書いてしまうこと。
NG: テストリスト*すべてを*具体的なテストコードに翻訳してから、ひとつずつテストを成功させようとしてしまうこと。まず一つだけテストコード、その後greenコード、のように実装する。


## red実装 - mdファイルをfeatureごとに書く
tests/test-list-docsのテストリストがない場合は、
tests/test-list-docs/　に featureで、mdファイルを書きます

ファイル命名
tests/test-list-docs/fastapi-restapi-red.mdみたいに
{domain}-{feature}-red.md

その際、assetを起こしたいものを網羅するように、対話で私に聞いてください。
根拠はこれです

""""
テストには実装したいコードの**振る舞い**を記述する。  
コードが期待する動作をリストアップする。  

「正常系はこうで、もしもサービスがタイムアウトしたらこうして、データベースにキーがまだないときはこうする。あとは……」
コード変更後、満たすべき振る舞い・様々な動作を網羅的に考えよう。  
同時に、振る舞いの変更が既存の動作を壊さないようにもする。
""""


## red実装 - mdファイルを元に一つのスクリプトファイルに、テストリストとしてred codeをかく
tests/test-list-docsのテストリストがある場合は
featureに関する、一つのスクリプトファイルに、テストリストとしてred codeをかく
pytestで書きます。

### userはテストひとつ選び出す
tests/test-list-docsのテストリストから

### red code は以下に実装する
- tests/backend/red-code
- tests/frontend/red-code


## 以下のことがあったら、対話で私に聞いてください。

green code書いて、red codeで書いたテストが成功した。
tests/test-list-docs/ 
にある mdは
tests/test-list-done/ に移動してね。

## その他
プロンププティングで確認がいるものは私に聞いてください
```




"""テンプレートプロンプト"""：
```sh
---
name: tdd-test-writer
description: Write failing integration tests for TDD RED phase. Use when implementing new features with TDD. Returns only after verifying test FAILS.
tools: Read, Glob, Grep, Write, Edit, Bash
skills: vue-integration-testing
---

# TDD Test Writer (RED Phase)

Write a failing integration test that verifies the requested feature behavior.

## Process

1. Understand the feature requirement from the prompt
2. Write an integration test in `src/__tests__/integration/`
3. Run `pnpm test:unit <test-file>` to verify it fails
4. Return the test file path and failure output

## Test Structure

typescript
import { afterEach, describe, expect, it } from 'vitest'
import { createTestApp } from '../helpers/createTestApp'
import { resetWorkout } from '@/composables/useWorkout'
import { resetDatabase } from '../setup'

describe('Feature Name', () => {
  afterEach(async () => {
    resetWorkout()
    await resetDatabase()
    document.body.innerHTML = ''
  })

  it('describes the user journey', async () => {
    const app = await createTestApp()

    // Act: User interactions
    await app.user.click(app.getByRole('button', { name: /action/i }))

    // Assert: Verify outcomes
    expect(app.router.currentRoute.value.path).toBe('/expected')

    app.cleanup()
  })
})


## Requirements

- Test must describe user behavior, not implementation details
- Use `createTestApp()` for full app integration
- Use Testing Library queries (`getByRole`, `getByText`)
- Test MUST fail when run - verify before returning

## Return Format

Return:
- Test file path
- Failure output showing the test fails
- Brief summary of what the test verifies
```