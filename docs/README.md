このリポジトリでは、TDD原則に基づいたClaude Code開発ができるようになっています。

ここでは実行手順を書いていきます。

テスト駆動開発の実践のお手本になったのは[こちらの海外の記事です](https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/)

こちらの記事の通り python実装用の、skill　と subagentを配置しています。
- TDD全体をコントロールする skill
- RED CODEをライティングする　red-subagent
- GREEN CODEをライティングする　green-subagent
- BLUE CODEをライティングする　blue-subagent

実装は全てClaude Codeが担います。

プロンプトの手順を大まかに述べると
1. 下準備：テストリストmdを用意する
   1. documents/配下のmdファイルに、実装したいタスクを書く
      1. 実装したいものは言語化しておきます。
      2. 「APIエンドポイントはこれ」「関数の振る舞いはこれ」等、実装したい振る舞いをmdに書きます。
      3. コードの雛形があるとなお良いです。
      4. これを実装タスクとします。
        ```
        要件定義書, コード例, 実装させたいことメモ → Claude Codeでタスク一覧にする
        
        タスクmdの例：documents/backend/speech/azure-speech-service-spec.md

        仕様書みたいに書いておくと、Claude Codeがテストを言語化しやすくなるのでおすすめです。
        ```
   2. 実装タスクから、テストリストを作ります。
      1. 具体的には、「実装タスクmdから、想像されるテストを全て列挙してください」と、送ります
      2. こうしてClaude Codeにテストを全て言語化させます。
      3. こうして、テストリストがmdファイルとして言語化されています。
   
        ```
        documents/backend/speech/azure-speech-service-spec.md がある。
        これを元にTDD用にテストを列挙してください
        ```

2. TDD実行
   1. テストリストmdを与えて、skillを実行してください。
   2. あとはskillが自動でRED→GREEN→BLUEを進行してくれます。
   
         ```
         @.claude/skills/tdd-integration/skill.md の通り
         @tests/test-list-docs/backend/test_stream_api.md にあるredテストから順次実行してください
         ```

こうして自動でTDDが回ります。
![TDD実行の様子](../context-resources/claude-tdd.png)


### TDD に使うファイルの詳細
**ファイル**: [.claude/skills/tdd-integration/skill.md](.claude/skills/tdd-integration/skill.md)

3つのフェーズを順番に実行するワークフローを自動化しています：
```
🔴 RED → 🟢 GREEN → 🔵 REFACTOR
```
各フェーズには明確なゲートがあり、前のフェーズが完了するまで次に進みません。


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



### テスト用ヘルパー関数
red-subagentに、helper関数とかconftestを使うように指示してます。

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



## 使い方

1. **新機能を実装する場合**:
   1. テストの仕様を書いておく
   
   ```
   実装の設計書から、このバックエンドエンドポイントが担うべき振る舞いを
   ~*.mdにテストリスト形式で書いてください
   ```
   2. red testに振る舞いを書かせる
   ```
   tdd skillを使って〇〇機能を実装してください
   red testは tests/~*/~*.py に書いてください
   テストが規定するべき振る舞いについては @/tasks/backend/*~md　にあります
   ```


2. **各フェーズを個別に実行する場合**:
   サブエージェントを個別に呼び出してください
   - RED: `tdd-test-writer-red` エージェントを起動
   - GREEN: `tdd-implementer-green` エージェントを起動
   - BLUE: `tdd-refactorer-blue` エージェントを起動


## 補足
### skillには新旧あります
**.claude/skills/tdd-integration：旧**

旧skillは、[こちらの海外の記事](https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/)

そのままskillを書いたものになります。

これは、失敗したテストのエラーログを全てコンテキスト履歴に残します。

そのためトークン消費量が大きいです。

体感、TDDを回して60分でレートリミットがきます。(Proプラン)

そのため、コンテキスト消費を抑えたのが　新 スキルになります。

**.claude/skills/tdd-integration-new/skill.md：新**

こちらは、コンテキスト消費を抑えたTDDを実行できるskillになります。

具体的には、TDD実行前に、Claude Codeがコンテキストに入れるディレクトリを絞ります。

これによって、余計なディレクトリを覗かないようにできます。

そのほか、 pytest のエラーログを全文コンテキストに送らないようにする工夫もしてあります。

TDD実装の際はこちらを使ってください。



### タスク整理用カスタムコマンド
カスタムコマンド(.claude/commands/tdd-style-commands/red-from-sample.md)

このカスタムコマンドはサンプルコードから仕様書を書かせるものです。

- セクション1-実装内容の設計とか仕様
- セクション2-実装したいコードの内容

みたいに、タスクmdを書かせられます。