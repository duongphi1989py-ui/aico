import streamlit as st
st.set_page_config(page_title="Voice AI TikTok PRO", page_icon="🎙️")
import asyncio
import edge_tts
import re
import hashlib
import os



st.title("🎙️ Voice AI TikTok PRO")
st.caption("🔥 Giọng mượt – style TikTok – chạy web 100%")

# ================= SESSION =================
if "text_input" not in st.session_state:
    st.session_state.text_input = ""

# ================= UTILS =================
def clear_text():
    st.session_state.text_input = ""

def get_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

# ================= STYLE ENGINE =================
def tiktok_style(text):
    text = text.strip()

    # xuống dòng -> pause
    text = text.replace("\n", "... ")

    # dấu câu
    text = text.replace(".", "... ")
    text = text.replace("!", "... ")
    text = text.replace("?", "... ")

    # clean space
    text = re.sub(r'\s+', ' ', text)

    return text

# ================= TTS =================
async def generate_voice(text, voice, rate, pitch, file):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch
    )
    await communicate.save(file)

# ================= UI =================
text = st.text_area("Nhập nội dung:", height=300, key="text_input")

col1, col2 = st.columns(2)

with col1:
    st.button("🗑️ Xóa nhanh", on_click=clear_text)

with col2:
    st.button("📋 Copy nhanh", on_click=lambda: st.toast("👉 Ctrl + C để copy"))

# ================= PRESET =================
preset = st.selectbox("🎭 Chọn style:", [
    "🔥 TikTok nữ viral",
    "📖 Kể chuyện",
    "🎬 Drama",
    "📢 Quảng cáo"
])

# ================= CONFIG =================
if preset == "🔥 TikTok nữ viral":
    voice = "vi-VN-HoaiMyNeural"
    rate = "+25%"
    pitch = "+3Hz"

elif preset == "📖 Kể chuyện":
    voice = "vi-VN-NamMinhNeural"
    rate = "-5%"
    pitch = "-2Hz"

elif preset == "🎬 Drama":
    voice = "vi-VN-HoaiMyNeural"
    rate = "+10%"
    pitch = "+1Hz"

else:
    voice = "vi-VN-HoaiMyNeural"
    rate = "+20%"
    pitch = "+2Hz"

# ================= RUN =================
if st.button("🚀 Generate Voice"):

    if not text:
        st.warning("Nhập nội dung trước!")
        st.stop()

    # xử lý text
    final_text = tiktok_style(text)

    file_name = f"voice_{get_hash(final_text)}.mp3"

    with st.spinner("🎧 Đang tạo giọng..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            generate_voice(final_text, voice, rate, pitch, file_name)
        )

    st.success("✅ Done!")
    st.audio(file_name)

    with open(file_name, "rb") as f:
        st.download_button("📥 Tải MP3", f, file_name="voice.mp3")
