
## fastapi
```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import time

app = FastAPI()

def fake_speech_recognition():
    # 本来はここで Azure Speech SDK など
    texts = ["こんにちは", "、", "これは", "リアルタイム", "音声認識", "です"]
    for t in texts:
        yield f"data: {t}\n\n"   # SSEフォーマット
        time.sleep(0.5)

@app.post("/recognize")
async def recognize(request: Request):
    return StreamingResponse(
        fake_speech_recognition(),
        media_type="text/event-stream"
    )

Azure Speech に差し替える時の考え方
def azure_stream():
    for partial_text in azure_recognizer():
        yield f"data: {partial_text}\n\n"
```

## fastapi
```python
import streamlit as st
import requests
import sseclient

st.title("リアルタイム音声認識（モック）")

if "listening" not in st.session_state:
    st.session_state.listening = False
if "transcription" not in st.session_state:
    st.session_state.transcription = ""

start_clicked = st.button("🎙️ 開始")
stop_clicked = st.button("⏹ 停止")

placeholder = st.empty()

if start_clicked:
    st.session_state.listening = True
    st.session_state.transcription = ""

    api_url = "http://localhost:8000/recognize"

    response = requests.post(
        api_url,
        stream=True,
        headers={"Accept": "text/event-stream"}
    )

    client = sseclient.SSEClient(response)

    for event in client.events():
        if not st.session_state.listening:
            break

        if event.data:
            st.session_state.transcription += event.data
            placeholder.text(st.session_state.transcription)

    client.close()
    st.session_state.listening = False

if stop_clicked:
    st.session_state.listening = False

より簡潔には、ジェネレータを用意して st.write_stream に渡すことで
一連のテキストストリームをタイプライター表示させることもできます
# ジェネレータを用意する例
def stream_text_from_sse(response):
    for line in response.iter_lines():
        if line:
            yield line.decode("utf-8")
# ...
# 開始ボタン処理内で:
response = requests.post(api_url, stream=True, headers={"Accept": "text/event-stream"})
st.session_state.transcription = st.write_stream(stream_text_from_sse(response))
```