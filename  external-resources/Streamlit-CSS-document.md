## **2\. DOM構造の解剖：data-testid属性の戦略的利用**

Streamlitは公式にCSS APIを提供していないが、自動テスト（E2Eテスト）のために安定した識別子であるdata-testid属性を主要なコンテナ要素に付与している。これらは「Shadow API（隠れたAPI）」として機能し、CSSセレクタのアンカーポイントとなる。ユーザーが列挙した4つの主要セレクタについて、その役割と制御範囲を解析する。

### **2.1 stAppViewContainer：アプリケーションのルートビュー**

セレクタ：\[data-testid="stAppViewContainer"\]

これはアプリケーションの表示領域全体を包み込むルートコンテナである。従来のHTMLにおける\<body\>タグに近い役割を果たすが、Streamlit特有のスクロール挙動を管理している点で異なる3。

* **主な用途**: アプリケーション全体の背景色変更、背景画像の配置。  
* **技術的洞察**: Streamlitのメインコンテンツはiframeやネストされたdiv構造内にあるため、単にbodyタグに背景を設定しても、stAppViewContainerのデフォルト背景（通常は白またはダークグレー）によって遮蔽されることが多い。したがって、全画面のスタイル変更は必ずこの要素をターゲットにする必要がある4。

**実装例（全画面背景画像）:**

CSS

\[data-testid="stAppViewContainer"\] {  
    background-image: url("https://example.com/bg.jpg");  
    background-size: cover;  
    background-repeat: no-repeat;  
    background-attachment: fixed;  
}

### **2.2 stSidebar：ナビゲーションと制御領域**

セレクタ：\`\`

左側に配置されるサイドバー領域である。デフォルトではドラッグによる幅調整が可能だが、CSSを用いることでこの挙動をオーバーライドできる3。

* **主な用途**: 幅の固定（ドラッグ無効化）、特定の背景色適用、非表示化。  
* **構造的特徴**: aria-expanded属性を持ち、開閉状態に応じたスタイル適用が可能である。

**実装例（サイドバーの幅を350pxに固定）:**

CSS

\[aria-expanded="true"\] \> div:first\-child {  
    width: 350px;  
}  
\[aria-expanded="false"\] \> div:first\-child {  
    width: 350px;  
    margin-left: \-350px;  
}

3

### **2.3 stHeader：トップバーとシステム制御**

セレクタ：\[data-testid="stHeader"\]

画面上部に固定され、ハンバーガーメニュー、実行状況インジケータ（Running Man）、およびデプロイボタンを含む領域である。

* **主な用途**: 透明化（背景画像との融合）、非表示化（キオスクモード）、装飾（ロゴの追加）。  
* **注意点**: 完全に非表示（display: none）にすると、ユーザーが設定メニュー（ダークモード切替など）にアクセスできなくなるため、運用上のリスクを考慮する必要がある5。

**実装例（ヘッダーの透明化）:**

CSS

\[data-testid="stHeader"\] {  
    background-color: transparent;  
}

7

### **2.4 stMain：メインコンテンツ領域**

セレクタ：\[data-testid="stMain"\]

サイドバーを除く、アプリケーションの主要なコンテンツが表示される領域である。バージョン1.38/1.40付近のアップデートにより、クラス名が.mainから変更された経緯があるため、data-testidの使用が強く推奨される8。

* **主な用途**: コンテンツ幅の最大値（max-width）の制御、パディング調整。  
* **構造的洞察**: Streamlitはデフォルトでコンテンツを中央揃えにし、一定の幅制限を設けている。ダッシュボードのような情報密度の高いアプリでは、この制限を解除するためにstMain配下のブロックコンテナを操作する必要がある。

**実装例（コンテンツ幅の最大化）:**

CSS

\[data-testid="stMain"\].block-container {  
    max-width: 100vw;  
    padding-left: 1rem;  
    padding-right: 1rem;  
}

### **3.2 手法B：Keyパラメータによるクラス生成（モダン/推奨）**

Streamlitの最近のアップデート（v1.39以降を含む）により、st.containerにkeyパラメータを付与することで、そのキー名に基づいた安定したCSSクラスがDOMに生成されるようになった。これは、ユーザーが求めている「人間が骨格を作り、そこに特別なCSSを当てる」という要件に対する、公式かつ堅牢な解である11。

**Pythonコードの修正:**

Python

import streamlit as st

\# コンテナにkeyを付与して「名前付きコンテキスト」を作成  
with st.container(key="main\_panel\_skeleton"):  
    col1, col2, col3 \= st.columns()  
    with col2:  
        \# さらに内部のコンテンツをラップすることも可能  
        with st.container(key="content\_card"):  
            st.title("Main Panel")  
            st.write("content")

**生成されるDOMの変化:**

key="main\_panel\_skeleton"を指定したコンテナのdiv要素には、.st-key-main\_panel\_skeletonというクラスが付与される。

**CSS実装:**

Python

css \= """  
\<style\>  
/\* 特定のキーを持つコンテナを直接ターゲットにする \*/  
.st-key-content\_card {  
    background-color: \#ffffff;  
    border: 2px solid \#4e4eff; /\* ブランドカラーの枠線 \*/  
    border-radius: 12px;  
    padding: 2rem;  
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);  
}

/\* スケルトン全体の調整（必要に応じて） \*/  
.st-key-main\_panel\_skeleton {  
    margin-top: 50px;  
}  
\</style\>  
"""  
st.markdown(css, unsafe\_allow\_html=True)

14

**利点**:

* **スコープの明確化**: ページ内のどこに配置されても、キーが一致する限りスタイルは正しく適用される。  
* **分離性**: ユーザーが意図した「コンテキスト」に対してのみCSSが作用し、他のウィジェットへの副作用がない。

## ---

**4\. 高度なレイアウトパターンの構築とデータ分析**

ユーザーが示した\`\`というカラム比率は、典型的な「センタリングされたカードレイアウト」を示唆している。この構造を、実際のアプリケーションでどのように活用・拡張できるか、データ駆動型アプリケーションの視点から分析する。

### **4.1 グリッドシステムの挙動とレスポンシブ対応**

Streamlitのst.columnsはFlexboxベースで実装されている。CSSで骨格を制御する際、レスポンシブ挙動（モバイル端末での表示）を考慮する必要がある。

| 画面サイズ | Streamlitのデフォルト挙動 | CSSによる制御の可能性 |
| :---- | :---- | :---- |
| **デスクトップ (\> 992px)** | 指定された比率（2:6:2）で横並び | flex-direction: row の維持、ギャップ（隙間）の微調整17 |
| **タブレット** | 横並びを維持しようとする | メディアクエリ（@media）を用いて強制的に縦並びに変更可能 |
| **モバイル (\< 576px)** | 自動的に縦積み（スタック）される | 各コンテナのマージンやパディングをモバイル用に縮小する調整が必要 |

**モバイル最適化のためのCSS注入例:**

CSS

@media (max-width: 576px) {  
    /\* モバイルでは余白カラム（col1, col3）を非表示にする戦略 \*/  
    \> div:nth-of-type(1),  
    \> div:nth-of-type(3) {  
        display: none;  
    }  
    /\* メインパネルを全幅にする \*/  
    \> div:nth-of-type(2) {  
        min-width: 100%;  
    }  
}

### **4.2 視覚的階層構造の強化（Visual Hierarchy）**

st.containerを用いた骨格作りは、単なるレイアウトだけでなく、情報の優先順位を視覚的に明示するために重要である。

* **Z軸の活用（シャドウと深度）**:  
  ユーザーのコードにある「Main Panel」を浮き上がらせるために、CSSのbox-shadowを用いる。フラットデザインのStreamlitにおいて、重なり（elevation）を表現する唯一の手段である。  
* **境界線と余白（マイクロスペーシング）**: Streamlitのデフォルトのコンポーネント間隔（gap）は1remである。st.columns(gap="small")などの引数もあるが、CSSを用いればgap: 0pxに設定し、完全に結合したダッシュボードパネルを作成できる17。

## ---

**5\. CSS注入のメカニズムとベストプラクティス**

CSSをStreamlitに適用する方法には、歴史的な変遷と技術的なトレードオフが存在する。

### **5.1 st.markdown vs st.html**

従来はst.markdown("\<style\>...\</style\>", unsafe\_allow\_html=True)が唯一の方法であったが、これは本来マークダウンを表示するための関数の「誤用」に近い。最新バージョンではst.html("\<style\>...\</style\>")が導入され、より意味的に正しいHTML注入が可能となった14。

* **st.markdown**: コンテナの中に不可視のdivを作成し、その中に\<style\>タグを展開する。Markdownパーサーを通すため、特定の文字がエスケープされるリスクがある。  
* **st.html**: HTMLを直接レンダリングする。CSS注入においては副作用が少なく、推奨される。

### **5.2 実行タイミングと再レンダリングの影響**

StreamlitはPythonスクリプトが上から下へ実行されるたびにフロントエンドを更新する。CSS注入コードは、それが適用される要素よりも\*\*前（コードの上部）\*\*に記述することが望ましい。

**推奨されるコード構成:**

Python

def load\_css():  
    st.html("""\<style\>... \</style\>""")

def main():  
    st.set\_page\_config(...)  
    load\_css()  \# 最初にスタイルを読み込む  
      
    \# 以下、アプリケーションの本体  
    with st.container(key="skeleton"):  
       ...

### **5.3 トラブルシューティング：CSSが適用されない場合**

1. **詳細度（Specificity）の不足**: Streamlitのデフォルトスタイルは詳細度が高い場合がある。\!importantの使用はやむを得ない場合が多い（例：color: red\!important;）。  
2. **セレクタの変更**: バージョンアップによりcss-xxxハッシュが変わっていないか、ブラウザの開発者ツール（F12）で確認する。  
3. **キャッシュの干渉**: ブラウザが古いCSSをキャッシュしている場合がある。

## ---

以下に **Streamlit のコード \+ CSS の例** をまとめた `.md` 形式ドキュメントを示します。  
各セクションには **Python 側 (Streamlit)** と **CSS 側 (埋め込み CSS)** のセットで載せています。

---

\# Streamlit \+ カスタム CSS: 安定識別子 & key ベースのクラス例

\#\# 1\. 使い方の前提

Streamlit に公式の CSS API はありません。    
しかし、E2E テスト用に付与される \`data-testid="..."\` 属性をターゲットにして CSS を当てることが可能です。これらは比較的安定した識別子として実務で使われています。:contentReference\[oaicite:0\]{index=0}

また、\`st.container(key="...")\` で指定した key には    
\`.st-key-\<key\>\` という CSS クラスが付与されるようになりました（v1.39 以降）。:contentReference\[oaicite:1\]{index=1}

\---

\#\# 2\. 全体構成 — Streamlit 側

\`\`\`python  
import streamlit as st

\# ヘッダー  
st.title("Streamlit Custom CSS Example")

\# セクション  
st.write("これは通常のテキストです。")

\# カスタマイズ対象の container  
with st.container(key="main\_section"):  
    st.write("This is the main section.")

\# カラム  
col1, col2 \= st.columns(2)  
with col1:  
    st.write("Column A")

with col2:  
    st.write("Column B")

\# チャット入力を強制的に表示してみる（存在すれば）  
st.chat\_input("Enter text...")

\# 下部ブロック（単体では明示しないが DOM には存在）  
st.write("アプリ下部のテキストです。")

\# CSS を挿入  
st.markdown("""  
\<style\>  
/\* CSS は次のセクションにまとめてあります \*/  
\</style\>  
""", unsafe\_allow\_html=True)

---

## **3\. CSS 側 — data-testid ベース**

### **3.1 全体のアプリビュー**

div\[data-testid="stAppViewContainer"\] {  
  background-color: \#f8f9fa;  
  padding: 20px;  
}

---

### **3.2 ヘッダー部分**

div\[data-testid="stHeader"\] {  
  background-color: \#005f73;  
  color: white;  
  padding: 10px;  
}

---

### **3.3 下部ブロックコンテナ**

div\[data-testid="stBottomBlockContainer"\] {  
  border-top: 1px solid \#ccc;  
  padding-top: 10px;  
}

---

### **3.4 チャット入力コンテナ**

div\[data-testid="stChatInput"\] {  
  border: 2px dashed \#4e4eff;  
  padding: 10px;  
  margin-top: 10px;  
}

---

### **3.5 カラム要素**

div\[data-testid="column"\] {  
  background-color: \#e0fbfc;  
  padding: 8px;  
  border-radius: 4px;  
}

---

### **3.6 垂直ブロックコンテナ**

div\[data-testid="stVerticalBlock"\] {  
  margin: 15px 0;  
  background: \#f0efeb;  
}

---

### **3.7 垂直ブロックラッパー**

div\[data-testid="stVerticalBlockBorderWrapper"\] {  
  border: 2px solid \#dfdfdf;  
  padding: 8px;  
}

---

### **3.8 汎用内部要素コンテナ**

div\[data-testid="element-container"\] {  
  padding: 0.75rem;  
}

---

## **4\. CSS 側 — key から生成されるクラス `.st-key-...`**

### **4.1 main\_section セクションだけをスタイル**

.st-key-main\_section {  
  border: 2px solid \#4e4eff;  
  background-color: \#ffffff;  
  border-radius: 10px;  
  padding: 15px;  
  box-shadow: 0px 4px 10px rgba(0,0,0,0.1);  
}

---

## **5\. まとめ**

`data-testid="..."` 属性は公式ドキュメントに明示された CSS API ではありませんが、E2E テストなどで安定して DOM に出現する属性です。  
対して `st.container(key="...")` で生成される `.st-key-...` クラスは公式的にサポートされている CSS クラス名です。([docs.streamlit.io](https://docs.streamlit.io/develop/api-reference/layout/st.container?utm_source=chatgpt.com))

| ターゲット | セレクタ |
| ----- | ----- |
| アプリ全体 | `[data-testid="stAppViewContainer"]` |
| ヘッダー | `[data-testid="stHeader"]` |
| 下部ブロック | `[data-testid="stBottomBlockContainer"]` |
| チャット入力 | `[data-testid="stChatInput"]` |
| カラム | `[data-testid="column"]` |
| 垂直ブロック | `[data-testid="stVerticalBlock"]` |
| 垂直ブロックラッパー | `[data-testid="stVerticalBlockBorderWrapper"]` |
| 内部一般コンテナ | `[data-testid="element-container"]` |
| キー指定コンテナ | `.st-key-<your_key>` |

