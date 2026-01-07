# Streamlit UI/UX 実装指南

本ドキュメントは、株主総会支援システムのStreamlit実装におけるUI/UX設計の指針を示します。

---

## 1. 基本方針

### 1.1 デザイン原則

- **シンプルさ優先**: 役員画面は特に、必要最小限の要素のみを表示
- **視認性重視**: 高齢者でも読みやすい大きな文字サイズ（デフォルト24px）
- **即時性**: アニメーションは最小限にし、情報の表示は瞬時に切り替え
- **タッチ操作対応**: タブレット操作を前提とした大きなボタン・タップ領域

### 1.2 レスポンシブ対応

```python
# デバイス検出とレイアウト調整の例
import streamlit as st

# タブレット向けの設定
st.set_page_config(
    page_title="株主総会支援システム",
    layout="wide",  # 画面幅を最大限活用
    initial_sidebar_state="collapsed"  # サイドバーは基本非表示
)
```

---

## 2. 役員画面の実装

### 2.1 画面構成

役員画面は以下の要素で構成されます：

#### 1.1 役員画面

```
┌─────────────────────────────────────────────┐
│ 株主総会支援システム - 役員画面              │
│                                             │
│  [A-] フォントサイズ [━━●━━] [A+]          │
│                                             │
│  [●チェックモード] [○ダイレクトモード]      │
│                                             │
├─────────────────────────────────────────────┤
│ 質問                                        │
├─────────────────────────────────────────────┤
│                                             │
│  株主様からの質問がここに表示されます。      │
│  長い質問の場合はスクロール可能です。        │
│                                             │
│                                             │
├─────────────────────────────────────────────┤
│ 回答                                        │
│ [要約] [詳細]                               │
├─────────────────────────────────────────────┤
│                                             │
│  回答内容がここに表示されます。              │
│  タブを切り替えることで要約/詳細を           │
│  確認できます。                             │
│  長い回答の場合はスクロール可能です。        │
│                                             │
│                                             │
│                                             │
└─────────────────────────────────────────────┘
```

### 2.2 文字サイズ変更機能の実装

**要件定義書 1.1.2より:**
- スライダー形式（連続可変）
- 範囲: 最小16px、デフォルト24px、最大48px
- localStorage相当の永続化が必要

#### 実装例

```python
import streamlit as st

# セッションステートで文字サイズを管理（初期値: 24px）
if 'font_size' not in st.session_state:
    st.session_state.font_size = 24

# ヘッダーエリア
with st.container():
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        st.markdown("### 文字サイズ")

    with col2:
        # スライダーで文字サイズを調整
        font_size = st.slider(
            label="フォントサイズ調整",
            min_value=16,
            max_value=48,
            value=st.session_state.font_size,
            step=1,
            label_visibility="collapsed"  # ラベルを非表示
        )
        st.session_state.font_size = font_size

    with col3:
        st.markdown(f"**{font_size}px**")

# カスタムCSSで文字サイズを適用
st.markdown(f"""
<style>
    .question-text {{
        font-size: {st.session_state.font_size}px;
        line-height: 1.6;
        padding: 20px;
        background-color: #f0f2f6;
        border-radius: 10px;
        margin-bottom: 20px;
    }}

    .answer-text {{
        font-size: {st.session_state.font_size}px;
        line-height: 1.6;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
    }}
</style>
""", unsafe_allow_html=True)
```

#### 永続化の実装

Streamlitでは `st.session_state` はページリロードでリセットされるため、クエリパラメータやカスタムJSで永続化します：

```python
# クエリパラメータから文字サイズを復元
query_params = st.query_params
if 'font_size' in query_params:
    st.session_state.font_size = int(query_params['font_size'])

# 文字サイズ変更時にクエリパラメータを更新
if font_size != st.session_state.font_size:
    st.query_params['font_size'] = font_size
```

**より堅牢な実装（推奨）:**

```python
# JavaScriptでlocalStorageを使用
st.markdown("""
<script>
    // ページロード時にlocalStorageから復元
    const savedFontSize = localStorage.getItem('officer_font_size');
    if (savedFontSize) {
        // Streamlitに値を送信する処理
    }

    // 文字サイズ変更時にlocalStorageに保存
    function saveFontSize(size) {
        localStorage.setItem('officer_font_size', size);
    }
</script>
""", unsafe_allow_html=True)
```

### 2.3 質問表示エリア

```python
# 質問表示
st.markdown("### 質問")
question_text = st.session_state.get('current_question', '質問が表示されます...')

st.markdown(f"""
<div class="question-text">
    {question_text}
</div>
""", unsafe_allow_html=True)
```

### 2.4 回答表示エリア（タブ切り替え）

**要件定義書より:**
- タブUIで要約/詳細を切り替え
- アニメーションなし（即座に表示）

```python
# タブでの回答表示
tab_summary, tab_detail = st.tabs(["📋 要約", "📄 詳細"])

with tab_summary:
    summary_text = st.session_state.get('answer_summary', '要約回答が表示されます...')
    st.markdown(f"""
    <div class="answer-text">
        {summary_text}
    </div>
    """, unsafe_allow_html=True)

with tab_detail:
    detail_text = st.session_state.get('answer_detail', '詳細回答が表示されます...')
    st.markdown(f"""
    <div class="answer-text">
        {detail_text}
    </div>
    """, unsafe_allow_html=True)
```

**注意点:**
- Streamlitのタブは若干のアニメーションがあるため、CSSで無効化する：

```python
st.markdown("""
<style>
    /* タブ切り替えのアニメーションを無効化 */
    .stTabs [data-baseweb="tab-panel"] {
        transition: none !important;
    }

    /* タブボタンを大きく */
    .stTabs [data-baseweb="tab"] {
        font-size: 20px;
        padding: 15px 30px;
    }
</style>
""", unsafe_allow_html=True)
```

### 2.5 回答モード選択

```python
# 回答モード選択（チェック/ダイレクト）
st.markdown("### 回答モード")
col1, col2 = st.columns(2)

with col1:
    if st.button("✓ チェックモード", use_container_width=True, type="primary" if st.session_state.get('response_mode') == 'check' else "secondary"):
        st.session_state.response_mode = 'check'

with col2:
    if st.button("⚡ ダイレクトモード", use_container_width=True, type="primary" if st.session_state.get('response_mode') == 'direct' else "secondary"):
        st.session_state.response_mode = 'direct'
```

---

## 3. オペレータ画面の実装

### 3.1 画面構成

オペレータ画面は情報密度が高いため、縦スクロール構成とします：

```
┌─────────────────────────────────────────────┐
│ 株主総会支援システム - オペレータ画面        │
├─────────────────────────────────────────────┤
│ 音声認識                                    │
│ ┌─────────────────────────────────────────┐ │
│ │ 株主: ○○についてお聞きしたい...         │ │
│ │ ナレーター: ○○について...              │ │
│ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│ メモ・質問入力                              │
│ ┌─────────────────────────────────────────┐ │
│ │                                         │ │
│ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│ 回答レベル設定                              │
│  要約: [100] 文字 [-] [+]                  │
│  詳細: [1000] 文字 [-] [+]                 │
│                                             │
│  [回答生成] [●チェック] [○ダイレクト]      │
├─────────────────────────────────────────────┤
│ 質問確認                                    │
│ ┌─────────────────────────────────────────┐ │
│ │                                         │ │
│ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│ 回答確認・編集 [要約] [詳細]                │
│ ┌─────────────────────────────────────────┐ │
│ │                                         │ │
│ │                                         │ │
│ └─────────────────────────────────────────┘ │
│                      [回答送信]             │
└─────────────────────────────────────────────┘
```──────────────────────────────────────┘
```

### 3.2 音声認識エリア

```python
st.markdown("## 音声認識")

# リアルタイム文字起こし結果を表示
with st.container(height=200):
    transcription_text = st.session_state.get('transcription', '')

    # 話者ごとに色分け
    st.markdown(f"""
    <div style="font-size: 14px; line-height: 1.8;">
        {transcription_text}
    </div>
    """, unsafe_allow_html=True)
```

### 3.3 メモ・質問入力エリア

```python
st.markdown("## メモ・質問入力")

memo_text = st.text_area(
    label="メモや質問を入力",
    value=st.session_state.get('memo', ''),
    height=150,
    max_chars=2000,
    label_visibility="collapsed"
)
st.session_state.memo = memo_text

# 文字数カウンター
st.caption(f"{len(memo_text)} / 2000 文字")
```

### 3.4 回答レベル文字数設定機能

**要件定義書 1.2.4より:**
- 要約: 50-300文字（50文字刻み）、デフォルト100文字
- 詳細: 500-2000文字（250文字刻み）、デフォルト1000文字
- ±ボタンまたは直接入力
- データベースに保存（次回起動時も維持）

#### 実装例

```python
st.markdown("## 回答レベル設定")

# セッションステートで初期化
if 'summary_length' not in st.session_state:
    st.session_state.summary_length = 100
if 'detail_length' not in st.session_state:
    st.session_state.detail_length = 1000

# 要約文字数設定
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown("### 要約")
with col2:
    if st.button("➖", key="summary_minus"):
        st.session_state.summary_length = max(50, st.session_state.summary_length - 50)
with col3:
    if st.button("➕", key="summary_plus"):
        st.session_state.summary_length = min(300, st.session_state.summary_length + 50)

summary_length = st.number_input(
    label="要約文字数",
    min_value=50,
    max_value=300,
    value=st.session_state.summary_length,
    step=50,
    label_visibility="collapsed"
)
st.session_state.summary_length = summary_length
st.caption(f"範囲: 50-300文字（50文字刻み）")

st.divider()

# 詳細文字数設定
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown("### 詳細")
with col2:
    if st.button("➖", key="detail_minus"):
        st.session_state.detail_length = max(500, st.session_state.detail_length - 250)
with col3:
    if st.button("➕", key="detail_plus"):
        st.session_state.detail_length = min(2000, st.session_state.detail_length + 250)

detail_length = st.number_input(
    label="詳細文字数",
    min_value=500,
    max_value=2000,
    value=st.session_state.detail_length,
    step=250,
    label_visibility="collapsed"
)
st.session_state.detail_length = detail_length
st.caption(f"範囲: 500-2000文字（250文字刻み）")
```

#### 永続化の実装

```python
import asyncio
import httpx

# 文字数設定をバックエンドに保存
async def save_answer_length_settings():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/settings/answer-length",
            json={
                "summary_length": st.session_state.summary_length,
                "detail_length": st.session_state.detail_length
            }
        )
        return response.json()

# 画面初回ロード時にバックエンドから設定を取得
@st.cache_data(ttl=60)
def load_answer_length_settings():
    response = httpx.get("http://localhost:8000/api/settings/answer-length")
    return response.json()

# 初期化時に設定を読み込み
if 'settings_loaded' not in st.session_state:
    settings = load_answer_length_settings()
    st.session_state.summary_length = settings.get('summary_length', 100)
    st.session_state.detail_length = settings.get('detail_length', 1000)
    st.session_state.settings_loaded = True
```

### 3.5 回答生成ボタン

```python
# 回答モード選択
col1, col2 = st.columns(2)
with col1:
    response_mode = st.radio(
        "回答モード",
        options=["check", "direct"],
        format_func=lambda x: "✓ チェックモード" if x == "check" else "⚡ ダイレクトモード",
        horizontal=True
    )
    st.session_state.response_mode = response_mode

# 回答生成ボタン（大きく目立つように）
if st.button("🚀 回答生成", type="primary", use_container_width=True):
    with st.spinner("回答を生成中...（目標: 15秒以内）"):
        # バックエンドAPIを呼び出し
        # 実装例は後述
        pass
```

### 3.6 回答確認・編集エリア

```python
st.markdown("## 回答確認・編集")

tab_summary, tab_detail = st.tabs(["📋 要約", "📄 詳細"])

with tab_summary:
    summary_answer = st.text_area(
        label="要約回答",
        value=st.session_state.get('generated_summary', ''),
        height=200,
        label_visibility="collapsed"
    )
    st.session_state.generated_summary = summary_answer
    st.caption(f"{len(summary_answer)} 文字")

with tab_detail:
    detail_answer = st.text_area(
        label="詳細回答",
        value=st.session_state.get('generated_detail', ''),
        height=400,
        label_visibility="collapsed"
    )
    st.session_state.generated_detail = detail_answer
    st.caption(f"{len(detail_answer)} 文字")
```

### 3.7 回答送信ボタン

```python
# チェックモードの場合のみ送信ボタンを表示
if st.session_state.response_mode == 'check':
    if st.button("📤 回答送信", type="primary", use_container_width=True):
        # 確認ダイアログ
        with st.dialog("確認"):
            st.write("この回答を全役員画面に送信しますか？")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("キャンセル", use_container_width=True):
                    st.rerun()
            with col2:
                if st.button("送信", type="primary", use_container_width=True):
                    # バックエンドAPIを呼び出し
                    send_answer_to_officers()
                    st.success("回答を送信しました！")
                    st.rerun()
```

---

## 4. リアルタイム同期の実装

### 4.1 Server-Sent Events (SSE) の実装

役員画面で回答をリアルタイムに受信するために、SSEを使用します。

```python
import streamlit as st
import httpx
import asyncio

# SSEストリームを受信
async def listen_to_sse():
    async with httpx.AsyncClient() as client:
        async with client.stream('GET', f"http://localhost:8000/api/stream/officer/{st.session_state.session_id}") as response:
            async for line in response.aiter_lines():
                if line.startswith('data: '):
                    data = json.loads(line[6:])
                    st.session_state.current_question = data.get('question')
                    st.session_state.answer_summary = data.get('answer_summary')
                    st.session_state.answer_detail = data.get('answer_detail')
                    st.rerun()

# バックグラウンドでSSEを受信
if 'sse_started' not in st.session_state:
    asyncio.create_task(listen_to_sse())
    st.session_state.sse_started = True
```

**注意:** Streamlitは標準でSSEをサポートしていないため、`streamlit-autorefresh` や `st.rerun()` を使って定期的に更新する方法も検討してください。

### 4.2 定期的な更新（ポーリング方式）

```python
from streamlit_autorefresh import st_autorefresh

# 5秒ごとに自動更新
count = st_autorefresh(interval=5000, key="officer_refresh")

# バックエンドから最新の質問・回答を取得
@st.cache_data(ttl=5)
def fetch_latest_qa(session_id):
    response = httpx.get(f"http://localhost:8000/api/qa/latest/{session_id}")
    return response.json()

qa_data = fetch_latest_qa(st.session_state.session_id)
st.session_state.current_question = qa_data.get('question')
st.session_state.answer_summary = qa_data.get('answer_summary')
st.session_state.answer_detail = qa_data.get('answer_detail')
```

---

## 5. スタイリング・UI/UX Tips

### 5.1 タブレット向けの大きなボタン

```python
st.markdown("""
<style>
    /* ボタンを大きく */
    .stButton > button {
        font-size: 18px;
        padding: 15px 30px;
        border-radius: 10px;
    }

    /* プライマリボタンを目立たせる */
    .stButton > button[kind="primary"] {
        background-color: #0066cc;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)
```

### 5.2 スクロール可能なエリア

```python
# 固定高さでスクロール可能なコンテナ
with st.container(height=300):
    st.markdown("""
    長いテキストがここに表示されます。
    コンテナの高さを超えると自動的にスクロールバーが表示されます。
    """)
```

### 5.3 タッチ操作の最適化

```python
st.markdown("""
<style>
    /* タッチ操作しやすいように余白を確保 */
    .stTabs [data-baseweb="tab"] {
        min-width: 150px;
        min-height: 60px;
    }

    /* スライダーのつまみを大きく */
    .stSlider > div > div > div > div {
        width: 30px;
        height: 30px;
    }
</style>
""", unsafe_allow_html=True)
```

### 5.4 高齢者向けの視認性向上

```python
st.markdown("""
<style>
    /* コントラストを高める */
    .question-text {
        color: #000000;
        background-color: #f0f2f6;
        border: 2px solid #cccccc;
    }

    /* 行間を広げる */
    .answer-text {
        line-height: 1.8;
        letter-spacing: 0.05em;
    }

    /* フォントをゴシック体に */
    body {
        font-family: "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Meiryo", sans-serif;
    }
</style>
""", unsafe_allow_html=True)
```

---

## 6. パフォーマンス最適化

### 6.1 キャッシュの活用

```python
# データ取得はキャッシュする
@st.cache_data(ttl=60)
def fetch_qa_history(session_id):
    response = httpx.get(f"http://localhost:8000/api/qa/history/{session_id}")
    return response.json()

# 重い計算はキャッシュする
@st.cache_data
def process_transcription(audio_data):
    # 音声認識処理
    return transcription_result
```

### 6.2 非同期処理

```python
import asyncio

# 複数のAPIリクエストを並列実行
async def fetch_all_data(session_id):
    async with httpx.AsyncClient() as client:
        qa_task = client.get(f"http://localhost:8000/api/qa/latest/{session_id}")
        settings_task = client.get(f"http://localhost:8000/api/settings/answer-length")

        qa_response, settings_response = await asyncio.gather(qa_task, settings_task)

        return qa_response.json(), settings_response.json()
```

---

## 7. エラーハンドリング

### 7.1 接続エラーの処理

```python
try:
    response = httpx.get("http://localhost:8000/api/qa/latest", timeout=10.0)
    response.raise_for_status()
    data = response.json()
except httpx.TimeoutException:
    st.error("⏱️ サーバーへの接続がタイムアウトしました。再試行してください。")
except httpx.HTTPStatusError as e:
    st.error(f"❌ エラーが発生しました: {e.response.status_code}")
except Exception as e:
    st.error(f"❌ 予期しないエラーが発生しました: {str(e)}")
```

### 7.2 ユーザーフレンドリーなエラーメッセージ

```python
# 回答生成に失敗した場合
if generation_failed:
    st.error("""
    ⚠️ 回答の生成に失敗しました。

    以下をお試しください：
    - 質問文が正しく入力されているか確認
    - インターネット接続を確認
    - しばらく待ってから再度「回答生成」ボタンをクリック

    問題が解決しない場合は、システム管理者にお問い合わせください。
    """)
```

---

## 8. テスト・デバッグ

### 8.1 デバッグモード

```python
# デバッグ情報を表示
if st.session_state.get('debug_mode', False):
    with st.expander("🔧 デバッグ情報"):
        st.write("Session State:", st.session_state)
        st.write("Current Font Size:", st.session_state.font_size)
        st.write("Summary Length:", st.session_state.summary_length)
        st.write("Detail Length:", st.session_state.detail_length)
```

### 8.2 モックデータでのテスト

```python
# 開発環境ではモックデータを使用
if st.session_state.get('use_mock_data', False):
    st.session_state.current_question = "株主優待の拡充について、今後の方針を教えてください。"
    st.session_state.answer_summary = "株主優待の拡充を検討しており、来期中に新制度を導入予定です。"
    st.session_state.answer_detail = "株主優待制度の拡充について、取締役会で検討を進めております。具体的には、保有株数に応じた段階的な優待内容の見直しを行い、長期保有の株主様にはさらに魅力的な特典をご用意する方向で調整中です。来期中には新制度を導入し、株主の皆様にご案内する予定です。"
```

---

## 9. まとめ

### チェックリスト

- [ ] 文字サイズ調整機能を実装（16-48px、スライダー、永続化）
- [ ] 回答レベル文字数設定機能を実装（要約: 50-300文字、詳細: 500-2000文字、±ボタン、永続化）
- [ ] タブUIで要約/詳細を切り替え（アニメーションなし）
- [ ] 回答モード選択（チェック/ダイレクト）
- [ ] リアルタイム同期（SSEまたはポーリング）
- [ ] タブレット向けの大きなボタン・タップ領域
- [ ] スクロール可能なエリア
- [ ] 高齢者向けの視認性向上（大きな文字、高コントラスト）
- [ ] エラーハンドリング
- [ ] パフォーマンス最適化（キャッシュ、非同期処理）

### 参考リンク

- [Streamlit公式ドキュメント](https://docs.streamlit.io/)
- [Streamlit レイアウトガイド](https://docs.streamlit.io/library/api-reference/layout)
- [Streamlit カスタムCSS](https://docs.streamlit.io/library/api-reference/utilities/st.markdown)

---

**作成日**: 2026/01/07
**対象システム**: 株主総会支援システム
**対象画面**: 役員画面、オペレータ画面
