import streamlit as st
import asyncio
import edge_tts
import os
import tempfile

# Coqui
from TTS.api import TTS

st.set_page_config(page_title="Voice AI PRO MAX", page_icon="🎙️")

st.title("🎙️ Voice AI PRO MAX")
st.write("🔥 Edge TTS + Clone giọng AI (Coqui XTTS v2)")

# ================= MODE =================
mode = st.radio("Chọn chế độ:", ["⚡ Nhanh (Edge TTS)", "🧠 Clone giọng (AI)"])

text = st.text_area("Nhập nội dung:", height=200)

# ================= EDGE TTS =================
async def generate_edge(text, voice, rate, file):
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await communicate.save(file)

# ================= CLONE VOICE =================
@st.cache_resource
def load_model():
    return TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

# ================= RUN =================
if st.button("🚀 Generate"):

    if not text:
        st.warning("Nhập text trước!")
        st.stop()

    # ================= EDGE MODE =================
    if mode == "⚡ Nhanh (Edge TTS)":
        voices = {
            "Nữ VN": "vi-VN-HoaiMyNeural",
            "Nam VN": "vi-VN-NamMinhNeural"
        }

        voice_name = st.selectbox("Chọn giọng", list(voices.keys()))
        voice = voices[voice_name]

        file_path = "edge_output.mp3"

        with st.spinner("Đang tạo giọng..."):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(generate_edge(text, voice, "+15%", file_path))

        st.audio(file_path)

    # ================= CLONE MODE =================
    else:
        uploaded = st.file_uploader("🎤 Upload giọng mẫu (.wav)", type=["wav"])

        if not uploaded:
            st.warning("Upload file giọng trước!")
            st.stop()

        # lưu file tạm
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_audio.write(uploaded.read())
        temp_audio.close()

        output_path = "clone_output.wav"

        with st.spinner("🧠 AI đang clone giọng..."):
            tts = load_model()

            tts.tts_to_file(
                text=text,
                speaker_wav=temp_audio.name,
                language="vi",
                file_path=output_path
            )

        st.success("✅ Done clone giọng!")
        st.audio(output_path)

        os.remove(temp_audio.name)
