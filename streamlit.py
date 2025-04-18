import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

# Koneksi MongoDB
client = MongoClient("mongodb+srv://abrisamgrup:man12345@cluster0.vddzxpx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["health_monitoring"]         # Nama database
collection = db["sensor_data"]        # Nama koleksi

gemini_collection = db["gemini_responses"]  # Koleksi jawaban Gemini


st.set_page_config(page_title="Heart Rate & Temperature Monitor", layout="wide")

st.title("📊 Real-Time Heart Rate & Temperature Dashboard")

# Ambil data dari MongoDB
data = list(collection.find().sort("timestamp", -1).limit(50))  # Ambil 50 data terbaru
if not data:
    st.warning("Belum ada data tersedia dari sensor.")
else:
    # Format data ke DataFrame
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by="timestamp", ascending=True)

    # Tampilkan dalam tabel
    st.subheader("📋 Data Terbaru")
    st.dataframe(df[["timestamp", "heart_rate", "temperature"]].tail(10), use_container_width=True)

    # Chart Heart Rate
    st.subheader("❤️ Heart Rate (BPM)")
    st.line_chart(df.set_index("timestamp")["heart_rate"])

    # Chart Temperature
    st.subheader("🌡️ Temperature (°C)")
    st.line_chart(df.set_index("timestamp")["temperature"])

    # Menampilkan Jawaban AI Gemini
    st.subheader("🧠 Jawaban AI Gemini")

    # Ambil data Gemini dari MongoDB
    gemini_data = list(gemini_collection.find().sort("timestamp", -1).limit(10))

    if not gemini_data:
        st.info("Belum ada jawaban dari AI Gemini.")
    else:
        gemini_df = pd.DataFrame(gemini_data)
        gemini_df["timestamp"] = pd.to_datetime(gemini_df["timestamp"])
        gemini_df = gemini_df.sort_values(by="timestamp", ascending=False)

    # ✅ Pengecekan kolom
    if all(col in gemini_df.columns for col in ["timestamp", "question", "answer"]):
        st.dataframe(gemini_df[["timestamp", "question", "answer"]], use_container_width=True)
    else:
        st.warning("Data Gemini tidak memiliki format yang sesuai.")
    


