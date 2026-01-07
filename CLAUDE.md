# プロジェクト基本情報

このプロジェクトは Python (uv) と Streamlit を使用した Web アプリケーションのプロトタイプです。
高速なビルドと実行を優先し、テストコード（pytest等）は含めない運用とします。

# 共通コマンド

- `uv run streamlit run app.py`: アプリケーションの起動
- `uv add <package>`: 新規パッケージの追加
- `uv run python <script>.py`: スクリプトの直接実行
- `uv fmt`: コードフォーマットの適用（black互換）

# コードスタイル

- `st.session_state` を活用したシンプルな状態管理
- UIコンポーネントは `with st.sidebar:` 等を使って構造化する
- 変数名は `snake_case` で統一し、型ヒントは必要最小限に留める
- ロジックは別ファイルの関数として切り出し、`app.py` は表示に専念させる

# ワークフロー

- パッケージ管理はすべて `uv` で完結させ、`requirements.txt` は使用しない
- 画面の「Always rerun」を有効にし、ライブプレビューで開発を進める
- エラー時は Streamlit のスタックトレースを読み、即座に修正・リロードを行う

# 重要な制約

**重要**: Streamlit の再実行特性を考慮し、データの読み込みや重い計算には必ず `@st.cache_data` を使用してください。
**必須**: プロトタイプですが、APIキー等の秘密情報は `.env` または `streamlit secrets` を使用し、ハードコードを避けてください。
