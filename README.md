## 前提条件

Slideの大体の方針をOCRで組んで  
Claude Codeで要件定義書生成（型にはめなくていい）  
→手を動かしながらClaude Code動かしてどうなるか確かめてみる  
一旦自由にやってみて、どこまで広がりが出るか

[https://docs.google.com/presentation/d/1SlKDv\_NDMpav4LmQy-CVfrKTr3NbImc\_HAltAFkj2iM/edit?slide=id.g3b4e0e84a11\_2\_359\#slide=id.g3b4e0e84a11\_2\_359](https://docs.google.com/presentation/d/1SlKDv_NDMpav4LmQy-CVfrKTr3NbImc_HAltAFkj2iM/edit?slide=id.g3b4e0e84a11_2_359#slide=id.g3b4e0e84a11_2_359)  
スライド1\~17(事前準備ツールは無視)

前提条件

* md共有してcontextで  
* /commands  
* /settings.json で  
* git worktree  
* playwrite MCPで動かしてUIテスト。ブラウザを立ち上げてuser環境を再現。  
  * e2eでテスト。これもできるように。  
  * [https://tech-lab.sios.jp/archives/50319](https://tech-lab.sios.jp/archives/50319)  
* Context7で外部コンテキストを注入する  
  * [https://zenn.dev/aprender/articles/8098609d599215](https://zenn.dev/aprender/articles/8098609d599215)  
* [https://github.com/AFG-Inc/cosmo-ir-2026](https://github.com/AFG-Inc/cosmo-ir-2026) 

## 方針

### 単純にOCR文字起こし

図解の言語化: スライド内の図（アーキテクチャ図やフローチャート）は、Claudeに「この図をMermaid形式のコードに変換して」と頼むと、後のドキュメント管理が非常に楽になります。./SourcePDF/slides.pdf　→　./documents/ocrOutput.md

documents/\~\*.md：タスク一覧

### 要件定義md作成

要件定義書のテンプレを与えて、テンプレの通り作らせてみます  
Claudeから質問を投げてもらうように促すと、より精度の高い定義書になります。  
./documentss/ocrOutput.md　→　./documents/requirements.md

### 要件定義からsubagent .md を生成する

ドメインごとにサブエージェントを作る  
プロンプト例を与えて、例の通り作らせる  
documents/requirements.md　→　.claude/agents/some-subagents.md 

### その他設定ファイル 

CLAUDE.md：プロジェクト固有の情報

.claude/settings.json：ツール許可設定  
settings.json 書く

### /commands　配下にmdを書く。

.claude/commands/：カスタムスラッシュコマンド  
これは自分で書く。  
/commands/\~.md  に use context7 使ってね、と書く

### Context7 ＝ MCPサーバーを立てる

 .mcp.json

### worktreeに分割する

### terminalで実行する

### playwrite \= npx版　MCPサーバーを立てる

### ディレクトリ

SourcePDF/slides.pdf  
documents/ocrOutput.md  
documents/requirements.md  
documents/\~\*.md：タスク一覧

CLAUDE.md：プロジェクト固有の情報  
.claude/agents/：サブエージェント。実装ガイドライン。コード規約など。

.claude/commands/：カスタムスラッシュコマンド  
.claude/settings.json：ツール許可設定  
.mcp.json：MCP サーバー設定

## 情報集

機能に関する情報

## Log

### 1/7 
