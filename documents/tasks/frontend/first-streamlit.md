# Streamlit 初期実装タスク

本ドキュメントは、株主総会支援システムのStreamlit実装における具体的なタスクリストです。
[ui-ux.md](./ui-ux.md)の設計を元に、段階的に実装を進めます。

---

## Phase 1: 基本セットアップ

### タスク 1.1: プロジェクト初期化
- [ ] `uv` で Streamlit プロジェクトをセットアップ
- [ ] 必要なパッケージをインストール
  - `uv add streamlit`
  - `uv add httpx`
  - `uv add python-dotenv`
- [ ] `app.py` を作成し、基本的なページ構成を確認
- [ ] `uv run streamlit run app.py` で起動確認

### タスク 1.2: 画面分離の基本構造
- [ ] `pages/` ディレクトリを作成
- [ ] `pages/1_officer.py` (役員画面) を作成
- [ ] `pages/2_operator.py` (オペレータ画面) を作成
- [ ] 各ページに `st.set_page_config()` を設定
  - `page_title`, `layout="wide"`, `initial_sidebar_state="collapsed"`

---

## Phase 2: 役員画面の実装

### タスク 2.1: 文字サイズ調整機能
- [ ] `st.session_state` で `font_size` を管理（初期値: 24px）
- [ ] スライダーUIを実装
  - 範囲: 16-48px
  - ステップ: 1px
  - ラベル: "A-", "[スライダー]", "A+"
- [ ] カスタムCSSで `.question-text` と `.answer-text` に文字サイズを適用
- [ ] クエリパラメータまたは localStorage で永続化
  - クエリパラメータ方式: `st.query_params` を使用
  - localStorage方式: JavaScript埋め込みで実装

### タスク 2.2: 質問表示エリア
- [ ] "質問" セクションを作成
- [ ] `st.session_state.current_question` を表示
- [ ] カスタムCSSで背景色、パディング、角丸を適用
- [ ] 長文の場合にスクロール可能にする

### タスク 2.3: 回答表示エリア（タブUI）
- [ ] `st.tabs()` で "要約" と "詳細" タブを作成
- [ ] 各タブに `st.session_state.answer_summary` と `answer_detail` を表示
- [ ] カスタムCSSでタブ切り替えのアニメーションを無効化
- [ ] タブボタンを大きく（`font-size: 20px`, `padding: 15px 30px`）

### タスク 2.4: 回答モード選択
- [ ] ラジオボタンまたはトグルボタンで "チェックモード" と "ダイレクトモード" を選択
- [ ] 選択状態を `st.session_state.response_mode` に保存
- [ ] ボタンのスタイルを大きく、タッチ操作しやすくする

### タスク 2.5: リアルタイム同期（受信側）
- [ ] SSE または ポーリング方式でバックエンドから質問・回答を受信
- [ ] `streamlit-autorefresh` を使った定期更新の実装（5秒間隔）
- [ ] 受信データを `st.session_state` に反映し、`st.rerun()` で再描画

---

## Phase 3: オペレータ画面の実装

### タスク 3.1: 音声認識エリア
- [ ] "音声認識" セクションを作成
- [ ] `st.container(height=200)` でスクロール可能なエリアを作成
- [ ] `st.session_state.transcription` をリアルタイム表示
- [ ] 話者ごとの色分け（株主、ナレーターなど）を実装

### タスク 3.2: メモ・質問入力エリア
- [ ] "メモ・質問入力" セクションを作成
- [ ] `st.text_area()` でメモ入力フィールドを作成
  - `height=150`
  - `max_chars=2000`
- [ ] 文字数カウンター (`st.caption(f"{len(memo_text)} / 2000 文字")`)

### タスク 3.3: 回答レベル文字数設定機能
- [ ] `st.session_state` で `summary_length` (初期値: 100) と `detail_length` (初期値: 1000) を管理
- [ ] 要約文字数設定
  - `st.number_input()` で直接入力（範囲: 50-300、ステップ: 50）
  - `➖` / `➕` ボタンで増減
  - 範囲の表示: "50-300文字（50文字刻み）"
- [ ] 詳細文字数設定
  - `st.number_input()` で直接入力（範囲: 500-2000、ステップ: 250）
  - `➖` / `➕` ボタンで増減
  - 範囲の表示: "500-2000文字（250文字刻み）"
- [ ] バックエンドAPIに設定を保存（POST `/api/settings/answer-length`）
- [ ] 画面初回ロード時にバックエンドから設定を取得（GET `/api/settings/answer-length`）

### タスク 3.4: 回答生成ボタン
- [ ] ラジオボタンで "チェックモード" / "ダイレクトモード" を選択
- [ ] `st.button("🚀 回答生成")` を実装
  - `type="primary"`
  - `use_container_width=True`
- [ ] クリック時に `st.spinner()` で "回答を生成中...（目標: 15秒以内）" を表示
- [ ] バックエンドAPIを呼び出し（POST `/api/generate-answer`）
  - リクエストボディ: `{ "question": "...", "summary_length": 100, "detail_length": 1000, "mode": "check" }`
- [ ] 生成結果を `st.session_state.generated_summary` と `generated_detail` に保存

### タスク 3.5: 回答確認・編集エリア
- [ ] "回答確認・編集" セクションを作成
- [ ] `st.tabs()` で "要約" と "詳細" タブを作成
- [ ] 各タブに編集可能な `st.text_area()` を配置
  - 要約: `height=200`
  - 詳細: `height=400`
- [ ] 文字数カウンター (`st.caption(f"{len(answer)} 文字")`)

### タスク 3.6: 回答送信ボタン
- [ ] チェックモードの場合のみ "📤 回答送信" ボタンを表示
- [ ] クリック時に確認ダイアログ (`st.dialog()`) を表示
  - "この回答を全役員画面に送信しますか？"
  - "キャンセル" / "送信" ボタン
- [ ] "送信" をクリックしたらバックエンドAPIを呼び出し（POST `/api/send-answer`）
- [ ] 送信成功時に `st.success("回答を送信しました！")` を表示

---

## Phase 4: スタイリング・UI/UX調整

### タスク 4.1: タブレット向けの大きなボタン
- [ ] カスタムCSSで `.stButton > button` のフォントサイズとパディングを調整
  - `font-size: 18px`
  - `padding: 15px 30px`
  - `border-radius: 10px`
- [ ] プライマリボタンを目立たせる
  - `background-color: #0066cc`
  - `font-weight: bold`

### タスク 4.2: 高齢者向けの視認性向上
- [ ] カスタムCSSでコントラストを高める
  - `.question-text`: `color: #000000`, `background-color: #f0f2f6`, `border: 2px solid #cccccc`
- [ ] 行間を広げる
  - `.answer-text`: `line-height: 1.8`, `letter-spacing: 0.05em`
- [ ] フォントをゴシック体に
  - `font-family: "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Meiryo", sans-serif`

### タスク 4.3: タッチ操作の最適化
- [ ] カスタムCSSでタブを大きく
  - `.stTabs [data-baseweb="tab"]`: `min-width: 150px`, `min-height: 60px`
- [ ] スライダーのつまみを大きく
  - `.stSlider > div > div > div > div`: `width: 30px`, `height: 30px`

---

## Phase 5: リアルタイム同期・バックエンド連携

### タスク 5.1: ポーリング方式のリアルタイム同期
- [ ] `streamlit-autorefresh` をインストール (`uv add streamlit-autorefresh`)
- [ ] 役員画面で5秒ごとに自動更新
  - `st_autorefresh(interval=5000, key="officer_refresh")`
- [ ] バックエンドから最新の質問・回答を取得
  - GET `/api/qa/latest/{session_id}`
- [ ] 取得データを `st.session_state` に反映

### タスク 5.2: SSE方式のリアルタイム同期（オプション）
- [ ] `httpx` の `stream()` を使ってSSEストリームを受信
- [ ] バックエンドのSSEエンドポイント（GET `/api/stream/officer/{session_id}`）に接続
- [ ] 受信したデータを `st.session_state` に反映し、`st.rerun()` で再描画
- [ ] バックグラウンドタスクとして実行（`asyncio.create_task()`）

### タスク 5.3: エラーハンドリング
- [ ] `httpx.TimeoutException` のハンドリング
  - `st.error("⏱️ サーバーへの接続がタイムアウトしました。再試行してください。")`
- [ ] `httpx.HTTPStatusError` のハンドリング
  - `st.error(f"❌ エラーが発生しました: {e.response.status_code}")`
- [ ] その他の例外のハンドリング
  - `st.error(f"❌ 予期しないエラーが発生しました: {str(e)}")`

---

## Phase 6: パフォーマンス最適化

### タスク 6.1: キャッシュの活用
- [ ] データ取得関数に `@st.cache_data(ttl=60)` を適用
  - `fetch_qa_history(session_id)`
  - `load_answer_length_settings()`
- [ ] 重い計算に `@st.cache_data` を適用
  - `process_transcription(audio_data)`

### タスク 6.2: 非同期処理
- [ ] 複数のAPIリクエストを並列実行
  - `asyncio.gather()` で QA取得と設定取得を同時実行
- [ ] 非同期関数を `asyncio.run()` で実行

---

## Phase 7: テスト・デバッグ

### タスク 7.1: デバッグモード
- [ ] `st.session_state.debug_mode` でデバッグ情報を表示
- [ ] `st.expander("🔧 デバッグ情報")` 内に Session State を表示
  - `st.write("Session State:", st.session_state)`
  - フォントサイズ、要約文字数、詳細文字数など

### タスク 7.2: モックデータでのテスト
- [ ] `st.session_state.use_mock_data` でモックデータを使用
- [ ] モック質問・回答を設定
  - 質問: "株主優待の拡充について、今後の方針を教えてください。"
  - 要約: "株主優待の拡充を検討しており、来期中に新制度を導入予定です。"
  - 詳細: "株主優待制度の拡充について、取締役会で検討を進めております。具体的には、保有株数に応じた段階的な優待内容の見直しを行い、長期保有の株主様にはさらに魅力的な特典をご用意する方向で調整中です。来期中には新制度を導入し、株主の皆様にご案内する予定です。"

---

## Phase 8: 最終チェック

### タスク 8.1: 機能チェックリスト
- [ ] 文字サイズ調整機能（16-48px、スライダー、永続化）
- [ ] 回答レベル文字数設定機能（要約: 50-300文字、詳細: 500-2000文字、±ボタン、永続化）
- [ ] タブUIで要約/詳細を切り替え（アニメーションなし）
- [ ] 回答モード選択（チェック/ダイレクト）
- [ ] リアルタイム同期（SSEまたはポーリング）
- [ ] タブレット向けの大きなボタン・タップ領域
- [ ] スクロール可能なエリア
- [ ] 高齢者向けの視認性向上（大きな文字、高コントラスト）
- [ ] エラーハンドリング
- [ ] パフォーマンス最適化（キャッシュ、非同期処理）

### タスク 8.2: UI/UX確認
- [ ] タブレット（iPad等）での動作確認
- [ ] タッチ操作の確認（ボタン、スライダー、タブ）
- [ ] 文字サイズ変更時の表示確認
- [ ] 長文表示時のスクロール確認
- [ ] リアルタイム同期の動作確認

### タスク 8.3: ドキュメント整備
- [ ] `README.md` に起動方法を記載
- [ ] 環境変数の設定方法を記載（`.env.example`）
- [ ] バックエンドAPIのエンドポイント一覧を記載

---

## 優先順位

### 最優先（Phase 1-2）
- プロジェクトセットアップ
- 役員画面の基本実装（文字サイズ調整、質問表示、回答表示）

### 高優先（Phase 3-4）
- オペレータ画面の基本実装（メモ入力、回答生成、回答送信）
- スタイリング・UI/UX調整

### 中優先（Phase 5-6）
- リアルタイム同期
- パフォーマンス最適化

### 低優先（Phase 7-8）
- デバッグ機能
- 最終チェック

---

## 参考リンク

- [ui-ux.md](./ui-ux.md) - UI/UX実装指南
- [Streamlit公式ドキュメント](https://docs.streamlit.io/)
- [CLAUDE.md](../../CLAUDE.md) - プロジェクト基本情報

---

**作成日**: 2026/01/07
**対象システム**: 株主総会支援システム
**対象画面**: 役員画面、オペレータ画面
