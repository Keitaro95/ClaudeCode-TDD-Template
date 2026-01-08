## オペレーター画面
### fe sidebar:全体設定
	要約の文字数 -+
	詳細の文字数 -+
	設定を適用ボタン
	
### 音声認識
fe停止/ req開始 ボタン押下でモックアップの音声データ送信
	SSEでストリーミングで文字起こしが起こる
be fastapi REST API
/ 音声認識 Azure Speech
	音声認識のボタン押下で起こるやつ
	res 一旦はazureで認識してres返るように
    res API keyがない場合はmock 返信
    reactive なデータストリーミングは [スタブ作成doc](documents/tasks/backend/db-api-stub.md) の通りでいい

### RAG
fe 回答作成ボタン押下
	req回答作成textboxの質問を送信
		文字起こし内容を質問としてRAGバックエンドに投げる
		質問 textboxに文字が移る
	res回答textboxにRAGの回答が来る
		要約/詳細ボタンでres表示切り替え
	req回答送信
		res役員画面に回答送信
be fastapi REST API
/ RAG 
	textboxの質問が来たら返すエンドポイント
	ベクトルdbがない場合はmockデータres
		res json要約：簡単なやつ
		res json詳細：詳細な回答


## 役員画面
fe 文字サイズ -文字/+文字
fe 質問 textboxに/ 音声認識 Azure Speechのres 
fe 要約 tab / RAG res json要約：簡単なやつ
fe 詳細 tab / RAG res json詳細：詳細な回答
