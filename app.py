import random
import streamlit as st
import asyncio
import edge_tts
import tempfile, os
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="Kevin老師 字庫複習", page_icon="📚", layout="centered")

words = [
    "本","辞書","雑誌","新聞","ニュース","ノート","手帳","名刺","カード",
    "鉛筆","ボールペン","シャープペン","鍵","キー","時計","腕時計","傘","鞄",
    "CD","テレビ","ビデオ","ラジオ","コンピューター","カメラ",
    "車","自動車","自転車","机","テーブル","椅子",
    "チョコレート","コーヒー","お土産","プレゼント",
    "英語","日本語","中国語"
]

st.title("📚 Kevin老師 字庫複習 APP")
st.caption("第12＋13課｜抽字複習＋AI日文發音（手機/電腦一致）")

APP_VERSION = "v4"  # 換版本號可強制洗 server cache

@st.cache_data(show_spinner=False)
def tts_mp3(text: str, voice: str="ja-JP-NanamiNeural", version: str=APP_VERSION) -> bytes:
    async def _run():
        ssml = f"""
        <speak version="1.0" xml:lang="ja-JP">
          <voice name="{voice}">
            {text}
          </voice>
        </speak>
        """
        communicate = edge_tts.Communicate(ssml, voice=voice, text_type="ssml")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tmp_path = f.name
        await communicate.save(tmp_path)
        data = open(tmp_path, "rb").read()
        os.remove(tmp_path)
        return data

    try:
        return asyncio.run(_run())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(_run())
        finally:
            loop.close()

def play_audio_bytes(audio_bytes: bytes):
    b64 = base64.b64encode(audio_bytes).decode()
    html = f"""
    <audio controls style="width:100%;">
      <source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg">
    </audio>
    """
    components.html(html, height=70)

if "picked" not in st.session_state:
    st.session_state.picked = random.sample(words, 8)

if "audio_text" not in st.session_state:
    st.session_state.audio_text = None

col1, col2 = st.columns([1,1])
with col1:
    if st.button("🎲 重新抽 8 個"):
        st.session_state.picked = random.sample(words, 8)
        st.session_state.audio_text = None
with col2:
    if st.button("🔊 全部朗讀"):
        st.session_state.audio_text = "、".join(st.session_state.picked)

st.divider()
st.subheader("🎯 今日抽出的 8 個單字")

for i, w in enumerate(st.session_state.picked, 1):
    c1, c2 = st.columns([4,1])
    with c1:
        st.write(f"{i}. {w}")
    with c2:
        if st.button("🔊", key=f"spk_{i}_{w}"):
            st.session_state.audio_text = w

if st.session_state.audio_text:
    st.markdown("### 🔈 發音播放")
    audio_bytes = tts_mp3(st.session_state.audio_text)
    play_audio_bytes(audio_bytes)
