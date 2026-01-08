## TDDについてt-wadaの記事

[https://t-wada.hatenablog.jp/entry/canon-tdd-by-kent-beck](https://t-wada.hatenablog.jp/entry/canon-tdd-by-kent-beck)  

1. 網羅したいテストシナリオのリスト（テストリスト）を書く  
2. テストリストの中から「ひとつだけ」選び出し、実際に、具体的で、実行可能なテストコードに翻訳し、テストが失敗することを確認する red  
3. プロダクトコードを変更し、いま書いたテスト（と、それまでに書いたすべてのテスト）を成功させる（その過程で気づいたことはテストリストに追加する）green  
4. 必要に応じてリファクタリングを行い、実装の設計を改善する blue  
5. テストリストが空になるまでステップ2に戻って繰り返す

### **概要**

テスト駆動開発（TDD: Test-Driven Development）はプログラミングのワークフローだ。あるプログラマが、あるシステム（まだ無いかもしれないが）の振る舞いを変更する必要があるとする。TDDの狙いは、そのプログラマを支援して、システムを下記のような新たな状態に導くことだ。

* それまで動作していたものは引き続き全て動作する  
* 新しい振る舞いは期待通りに動作する  
* システムはさらなる変更の準備ができている  
* プログラマとその同僚は、上記の点に自信を持っている

### インターフェイスと実装の分離

設計には2種類ある。

* 物理設計・インターフェイス  
  * システムはその振る舞いをどう実装するべきかの設計=設計書・dbスキーマなどのスキーマ  
* 論理設計・実装  
  * ある**振る舞い**はどのように呼び出されるべきかの設計＝**TDD**

### **ステップ1. テストリスト**

テストには実装したいコードの**振る舞い**を記述する。  
コードが期待する動作をリストアップする。  
「正常系はこうで、もしもサービスがタイムアウトしたらこうして、データベースにキーがまだないときはこうする。あとは……」

コード変更後、満たすべき振る舞い・様々な動作を網羅的に考えよう。  
同時に、振る舞いの変更が既存の動作を壊さないようにもする。  
それらをテストリストに追加する。

NG: 実装の設計判断を混ぜ込んでしまうこと。テスト駆動開発は設計を担当しない。設計がある状態でTDDするのが望ましい。

### **ステップ2. 失敗するテストをひとつ書く red code**

テストをひとつ。準備と実行と検証（アサーション）が備わった、本当の本当に自動化されたテストを「ひとつだけ」書く

assertErrorを吐くコードを書く

（テストコードをアサーションから書き始めて、上に向かって逆向きに書き進めてみるやり方もある）

NG: コードカバレッジを上げるためだけに、アサーションのないテストコードを書いてしまうこと。

NG: テストリスト*すべてを*具体的なテストコードに翻訳してから、ひとつずつテストを成功させようとしてしまうこと。まず一つだけテストコード、その後greenコード、のように実装する。

テストリストから次に書くテスト項目をひとつ選び出すのは重要なスキル。  
それは経験によってのみ得られるものだ。  
テストを選ぶ順番は、プログラミングの快適さと最終的な成果の両方に重大な影響を及ぼす。  
テストを適切な順番に実行する。これによって、デグレが少ない、制御された実装になる、ということか。

### **ステップ3. テストを成功させるコードを実装する green code**

失敗するテストをひとつ書けたら、今度はテストを成功させるコードを実装する。

NG: アサーションを削除して、テストが成功したふりをしてしまうこと。

NG: テスト対象を実際に動かしたときの値をコピーして、テストコードの中の期待値にペーストしてしまうこと。これではダブルチェックにならず、TDDの妥当性確認（validation）としての価値が台無しになってしまう。

NG: green codeを書くと同時にリファクタリングを混ぜ込んでしまうこと。  
まずはred codeが通る動くもの、その後リファクタリング。  
このやりかたが結局は脳にも優しい。

レッド（テスト失敗）からグリーン（テスト成功）にする過程で新しいテストの必要性に気づいたら、それをテストリストに追加する。

もし、green codeを書いていてテストコードに抜け漏れがあると気づいたら、レッドコード初めからやり直すのがおすすめ。

テストが成功したら「済」マークをつけてテストリストから消し込む。

### ステップ4. 必要に応じてリファクタリングを行う blue code

*ここまで来たら、ようやく*実装の設計判断を行えるようになる。

NG: この段階で必要以上に[リファクタリング](https://www.ohmsha.co.jp/book/9784274224546/)してしまうこと。

NG: 早すぎる抽象化。コードに重複があるとしても、重複を無くさなければいけないわけではない。

### ステップ5. テストリストが空になるまでステップ2に戻って繰り返す

コードの動作に対する不安が退屈に変わるまで、テストとコーディングを続ける。

## Claude Code でTDD

TDD原則

* テストファーストを強制する- 失敗するテストの前に実装は存在しない  
* フェーズを集中させる- テスト作成者は実装の詳細について考えるべきではない  
* リファクタリングを確実に行う- 機能がすでに動作している場合は簡単にスキップできる

TDDでテストを最初に書く最大のポイントは、実装がまだわからないということです。  
つまり、red code実装の際は、すでに計画している実装を見せないということです。  
こうして、意図しない「ズル」を防ぎます。

### テスト作成用Skills, Subagent

テスト作成用Skills, Subagentを立てる。  
これにより独立したコンテキストでテスト作成できます。  
機能実装のコンテキストを与えないため。  
これにより、red code実装フェーズは完全に独立して実行されます。  
実装者は失敗したテストだけを見ることができます。

### TDD skill.md

.claude/skills/tdd-integration/skill.md  
[https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/\#the-tdd-skill](https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/#the-tdd-skill) 

このdescriptionフィールドにはトリガーフレーズが含まれている。  
新しいfeatureやfunctionを実装するように指示すると、クロードは自動的にこのスキルを起動します。

```sh  
次の3つのphaseに従って新しい機能を実装してください。  
フェーズをスキップしないでください  
🔴 RED PHASE: Delegating to tdd-test-writer...  
Invoke the \`tdd-test-writer\` subagent with: tdd-test-writerサブエージェントを起動

\*\*Do NOT proceed to Green phase until test failure is confirmed.\*\*

🟢 GREEN PHASE: Delegating to tdd-implementer...  
Invoke the \`tdd-implementer\` subagent with:　tdd-implementerサブエージェントを起動

\*\*Do NOT proceed to Refactor phase until test passes.\*\*

🔵 REFACTOR PHASE: Delegating to tdd-refactorer...  
Invoke the \`tdd-refactorer\` subagent with:　tdd-refactorerサブエージェントを起動

\*\*Cycle complete when refactor phase returns.\*\*  
```

各フェーズには「…まで先に進まないでください」という明確なゲートがある。  
🔴🟢🔵の絵文字のおかげで、出力で進捗状況を簡単に把握できます。

### red code 実装 subagent

[https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/\#the-test-writer-agent-red-phase](https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/#the-test-writer-agent-red-phase)  
.claude/agents/tdd-test-writer.md:  
test code exampleを載せてる  
Use \`createTestApp()\` for full app integration  
これは[テスト用のhelper関数](https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/#the-test-helper)。作者が用意したもの。　

### green code 実装 subagent

[https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/\#the-implementer-agent-green-phase](https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/#the-implementer-agent-green-phase)  
.claude/agents/tdd-style-subagents/tdd-implementer.md  
テストに通過するためだけの最小限の実装をしてください、と書いてる。  
そのほか、手順と原則。

### blue code 実装 subagent

[https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/\#the-refactorer-agent-refactor-phase](https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/#the-refactorer-agent-refactor-phase)  
.claude/agents/tdd-refactorer.md:  
テストコードをみて、実装リファクタリングをしてください　と書いてる

* 必要以上のリファクタリング  
* 早すぎる抽象化  
* コードに重複があるとしても、重複を無くさなければいけないわけではない

ことを盛り込んだ方が良さそう。

### テスト用skillmdを確実にアクティブにするためにhookを使う→これは毎回実行されてしまうので、なし、/skillmd指定して名指しで起こせばいい。

.claude/settings.jsonにhookを設定
**UserPromptSubmit：「送信ボタンを押した直後」npx コマンドを実行。**
(スクリプトは.claude/hooks/user-prompt-skill-eval.tsに書いてる)
このフックにより、スキルのアクティベーションが約20%から約84%に飛躍的に向上しました。
```json
{
  "hooks": {
    **"UserPromptSubmit": \[**
      {
        "matcher": "",
        "hooks": \[
          {
            "type": "command",
            **"command": "npx tsx \\"$CLAUDE\_PROJECT\_DIR/.claude/hooks/user-prompt-skill-eval.py\\"",**
            "timeout": 5
          }
        \]
      }
    \]
  }
}
```
---

## このリポジトリの実装例

このリポジトリでは、上記のTDD原則に基づいたClaude Code開発環境が実装済みです。

### TDD用エージェント（Subagent）

3つのフェーズに対応したサブエージェントを用意しています：

#### 1. RED Phase: テスト作成エージェント
**ファイル**: [.claude/agents/tdd-style-subagents/tdd-test-writer-red.md](.claude/agents/tdd-style-subagents/tdd-test-writer-red.md)

- 失敗するテストを書くことに特化
- `tests/` 配下に統合テストを作成
- テストが**必ず失敗すること**を確認してから完了
- 実装の詳細を知らない状態でテストを書く

#### 2. GREEN Phase: 実装エージェント
**ファイル**: [.claude/agents/tdd-style-subagents/tdd-implementer-green.md](.claude/agents/tdd-style-subagents/tdd-implementer-green.md)

- テストを通過させる最小限の実装のみを行う
- テストが**すべて通過すること**を確認してから完了
- リファクタリングは行わない（次フェーズに委ねる）

#### 3. BLUE Phase: リファクタリングエージェント
**ファイル**: [.claude/agents/tdd-style-subagents/tdd-refactorer-blue.md](.claude/agents/tdd-style-subagents/tdd-refactorer-blue.md)

- テストが通った状態で、コードの品質を向上
- 早すぎる抽象化を避ける
- 必要最小限のリファクタリングのみ実施

### TDD統合スキル

**ファイル**: [.claude/skills/tdd-integration/skill.md](.claude/skills/tdd-integration/skill.md)

3つのフェーズを順番に実行するワークフローを自動化：

```
🔴 RED → 🟢 GREEN → 🔵 REFACTOR
```

各フェーズには明確なゲートがあり、前のフェーズが完了するまで次に進みません。

### テスト用ヘルパー関数

**ファイル**: [tests/frontend/helpers.py](tests/frontend/helpers.py)

Streamlit AppTestを使った統合テストを簡単に記述するためのヘルパー関数を提供：

- `create_streamlit_runner()`: Streamlitアプリの初期化とモック設定
- `mock_backend_api()`: FastAPIバックエンドのモック化
- `mock_azure_speech_result()`: Azure Speech Serviceのモック化

**使用例**:
```python
def test_operator_button(mocker):
    mocker.patch("requests.post", return_value=mock_backend_api())
    at = create_streamlit_runner("src/frontend/app/pages/1_operator_app.py")
    at.button[0].click().run()
    assert "expected text" in at.text_area[0].value
```

### 使い方

1. **新機能を実装する場合**:
   ```
   /tdd-integration を使って〇〇機能を実装してください
   ```

2. **各フェーズを個別に実行する場合**:
   - RED: `tdd-test-writer` エージェントを起動
   - GREEN: `tdd-implementer` エージェントを起動
   - BLUE: `tdd-refactorer` エージェントを起動

3. **テストヘルパーを使う場合**:
   ```python
   from tests.frontend.helpers import create_streamlit_runner, mock_backend_api
   ```

このテンプレートを使うことで、TDDの原則に従った堅牢な開発が可能になります。