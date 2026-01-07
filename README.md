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

### OCR文字起こし

.claude/skills/pdf-ocr-skill.mdにOCRのAgent Skillsを登録しました。

「pdf-ocr」スキルを使って、cosmo-ir-slides.pdf の OCR を実行してください  
実行結果は　./documents/ocrOutput.md　にライティングしてください

### 要件定義md作成

要件定義書のテンプレを与えて、テンプレの通り作らせてみます

./documents/[ocrOutput.md](http://ocrOutput.md)　は今回のPJの骨子です。  
SourceSample/[requirements-sample.md](http://requirements-sample.md) は要件定義のサンプルです。  
足りないものがあったら、Claudeから質問を投げてください  
より精度の高い定義書を作りましょう。  
要件定義書は　./documents/requirements.md　に書いてください。

### 要件定義からsubagent .md を生成する

要件定義書はdocuments/[requirements.md](http://requirements.md)に作りました。  
これを読んで、個別のドメインごとにランニングさせるサブエージェントを複数作ってください。  
\#\#作り方の手順  
\#\#\#1要件定義書から、ドメインを分割する。  
fastapiならfastapiドメイン   
streamlitならstreamlitドメイン  
その他、  
このようにドメインに応じた専門性でサブエージェントを立ててください。  
mdファイル生成の際は、私に確認をとってください。

\#\#\#2 実装担当のsubagent.mdの書き方は以下のようになる  
場所：ファイル名称はこのように書く　.claude/agents/{domain}-{language}-expert.md   
{domain}は担当ドメイン名　{language}は使用する言語やフレームワーク

\#\#\#3template：以下は .claude/agents/[fastapi-python-expert.md](http://fastapi-python-expert.md) の例です。  
実装担当のsubagentを作る際はこの例を使って書いてください。

| .claude/agents/fastapi-python-expert.md \--- name: fastapi-python-expert description: Use this agent when you need to design, implement, or optimize FastAPI backend applications. This includes API endpoint creation, database … model: sonnet color: cyan \--- \*\*always ultrathink\*\* あなたは FastAPI を使用した Python バックエンド開発のエキスパートです。FastAPI フレームワークの深い知識、クラウドアーキテクチャ、ビジネスロジックの実装において豊富な経験を持っています。 \#\# コーディング規約 \#\# パッケージ管理 \#\# git 管理 \#\# コメント・ドキュメント方針 \#\# プロジェクト構造 \#\# 開発ガイドライン \#\# あなたの専門分野 \#\# 問題解決アプローチ |
| :---- |

2-2クオリティチェック担当のsubagentは作成済み.agents/quality-check-exprert.md

### その他設定ファイル 

[CLAUDE.md](http://CLAUDE.md)：プロジェクト固有の情報

| \# プロジェクト基本情報 このプロジェクトは Python (uv) と Streamlit を使用した Web アプリケーションのプロトタイプです。 高速なビルドと実行を優先し、テストコード（pytest等）は含めない運用とします。 \# 共通コマンド \- \`uv run streamlit run app.py\`: アプリケーションの起動 \- \`uv add \<package\>\`: 新規パッケージの追加 \- \`uv run python \<script\>.py\`: スクリプトの直接実行 \- \`uv fmt\`: コードフォーマットの適用（black互換） \# コードスタイル \- \`st.session\_state\` を活用したシンプルな状態管理 \- UIコンポーネントは \`with st.sidebar:\` 等を使って構造化する \- 変数名は \`snake\_case\` で統一し、型ヒントは必要最小限に留める \- ロジックは別ファイルの関数として切り出し、\`app.py\` は表示に専念させる \# ワークフロー \- パッケージ管理はすべて \`uv\` で完結させ、\`requirements.txt\` は使用しない \- 画面の「Always rerun」を有効にし、ライブプレビューで開発を進める \- エラー時は Streamlit のスタックトレースを読み、即座に修正・リロードを行う \# 重要な制約 \*\*重要\*\*: Streamlit の再実行特性を考慮し、データの読み込みや重い計算には必ず \`@st.cache\_data\` を使用してください。 \*\*必須\*\*: プロトタイプですが、APIキー等の秘密情報は \`.env\` または \`streamlit secrets\` を使用し、ハードコードを避けてください。 |
| :---- |

### 

### /commands　配下にmdを書く。

subagentファイルは.claude/agents/{domain}-{language}-expert.md   
に作りました。これを読んで、個別のドメインごとにランニングさせるカスタムコマンドmdを複数作ってください。

\#\#作り方の手順  
\#\#\#1 実装担当の.claude/agents/{domain}-{language}-expert.md があります。  
これを実行するカスタムコマンドファイルを場所に作ってください  
場所：ファイル名称はこのように書く　.claude/commands/subagent-{domain}.md   
ここの{domain}は.claude/agents/{domain}-{language}-expert.md　にあるドメイン名です

\#\#\#3template：カスタムコマンド用subagentを作る際はこの例を使って書いてください。  
以下は  .claude/commands/subagent-fastapi.md の例です。  
\#\#\#\#template構成の留意  
description: カスタムコマンドの説明  
ultrathinkをつける。  
Context7で外部ライブラリのコンテキストを注入できるようにmdにも書いておく  
(後ほどContext7でmcpサーバーを立てる予定です)

| \# .claude/commands/subagent-fastapi.md \--- description: FastAPIの実装タスクを、Context7でコンテキストを取得しつつ、実装とレビューのループで完遂します。 \--- \*\*ultrathink\*\* 指定されたタスクに対して、以下の手順で進めてください。 各ステップでは、必要に応じて MCP サーバー \`context7\`（\`use\_context7\` 等のツール）を呼び出し、プロジェクトの最新の構造や依存関係を正確に把握した上で実行してください。 1\. \*\*プロジェクトコンテキストの把握\*\* \- \`context7\` を使用して、関連するファイル、関数、クラスの定義を読み取る \- 現在の実装状況を詳細に理解し、タスクの修正範囲を特定する 2\. \*\*機能実装（fastapi-python-expert）\*\* \- 必ず \`fastapi-python-expert\` エージェントを起動して実装を行う \- \`context7\` から得た情報を元に、既存のコードと整合性の取れた実装を行う \- テストが通過するまで、または要件を満たすまでこのステップを繰り返す 3\. \*\*品質検証（quality-check-expert）\*\* \- 必ず \`quality-check-expert\` エージェントを起動してレビューを行う \- 実装内容に抜け漏れがないか、\`context7\` で確認できる他のファイルへの影響（破壊的変更）がないか徹底的にチェックする \- 問題があればステップ 2 に戻り、すべてのレビューをクリアするまでループする |
| :---- |

### .claude/settings.json

blocked\_commands を追加

### Context7 ＝ MCPサーバーを立てる 

 .mcp.json  
外部APIキーが必要なので割愛

### worktreeに分割する 16時

### terminalで実行する 17時

### playwrite \= npx版　MCPサーバーを立てる 明日想定

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

[Databricks Apps(Streamlit)からLangChainモデルをストリーミング呼び出しする \- Qiita](https://qiita.com/taka_yayoi/items/5b31bb8a079623de84ec)

## Log

### 1/7 