# app.py
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Kevin老師 字庫複習", page_icon="📚", layout="centered")

# ====== 字庫（第12＋13課全部）======
words = [
    "本","辞書","雑誌","新聞","ニュース","ノート","手帳","名刺","カード",
    "鉛筆","ボールペン","シャープペン","鍵","キー","時計","腕時計","傘","鞄",
    "CD","テレビ","ビデオ","ラジオ","コンピューター","カメラ",
    "車","自動車","自転車","机","テーブル","椅子",
    "チョコレート","コーヒー","お土産","プレゼント",
    "英語","日本語","中国語"
]

st.title("📚 Kevin老師 字庫複習 APP")
st.caption("第12＋13課｜抽字複習＋AI日文發音（0成本）")

st.write(f"目前字庫共有 **{len(words)}** 個單字。")

# 抽 8 個
if "picked" not in st.session_state:
    st.session_state.picked = random.sample(words, 8)

col1, col2 = st.columns([1,1])
with col1:
    if st.button("🎲 重新抽 8 個"):
        st.session_state.picked = random.sample(words, 8)
with col2:
    if st.button("🔊 全部朗讀"):
        # 用 JS 一次朗讀 8 個
        speak_all_js = """
        <script>
        function speak(text){
          const u = new SpeechSynthesisUtterance(text);
          u.lang = "ja-JP";
          u.rate = 0.9;
          speechSynthesis.speak(u);
        }
        const words = %s;
        words.forEach(w => speak(w));
        </script>
        """ % (str(st.session_state.picked))
        components.html(speak_all_js, height=0)

st.divider()
st.subheader("🎯 今日抽出的 8 個單字")

# 單字列表＋逐字朗讀按鈕
for i, w in enumerate(st.session_state.picked, 1):
    components.html(f"""
    <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
      <div style="font-size:20px;">{i}. {w}</div>
      <button onclick="speak('{w}')" style="
        border:none; padding:6px 10px; border-radius:8px;
        background:#f1f1f1; cursor:pointer; font-size:16px;
      ">🔊</button>
    </div>

    <script>
    function speak(text){{
      const u = new SpeechSynthesisUtterance(text);
      u.lang = "ja-JP";
      u.rate = 0.9;
      u.pitch = 1.0;
      speechSynthesis.speak(u);
    }}
    </script>
    """, height=45)
