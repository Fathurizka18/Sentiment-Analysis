import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from textblob import TextBlob
import swifter
import os

# =======================
# 📌 1. Load Dataset (Cache)
# =======================
@st.cache_data
def load_data():
    file_path = "twitter_data_cleaned.csv.gz"

    if not os.path.exists(file_path):
        st.error(f"❌ File '{file_path}' tidak ditemukan. Pastikan file ada di repositori GitHub!")
        return None

    df = pd.read_csv(file_path, compression="gzip", low_memory=False)
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df.fillna("Unknown", inplace=True)
    
    return df

    df = pd.read_csv(file_path, compression="gzip", low_memory=False)
    
    # Konversi waktu & hapus "WIB"
    df["created_at"] = df["created_at"].astype(str).str.replace(" WIB", "", regex=False)
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    # Isi nilai kosong dengan "Unknown"
    df.fillna("Unknown", inplace=True)
    
    return df

df = load_data()
if df is None:
    st.stop()

# =====================
# 📌 2. Sidebar Navigation
# =====================
st.sidebar.title("📊 Twitter Data Analysis")
menu = st.sidebar.radio("🔍 Pilih Analisis:", ["EDA", "Sentiment Analysis", "Social Network Analysis"])

# ============================
# 📌 3. Exploratory Data Analysis (EDA)
# ============================
if menu == "EDA":
    st.title("📊 Exploratory Data Analysis (EDA)")

    st.subheader("📌 Preview Data")
    st.dataframe(df.head(1000))

    st.subheader("📌 Statistik Data")
    st.write(df.describe(include=["number"]))

    # 🔹 Tweet Volume Over Time
    st.subheader("📈 Jumlah Tweet per Tanggal")
    df["date"] = df["created_at"].dt.date
    tweet_counts = df["date"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(tweet_counts.index, tweet_counts.values, marker="o", linestyle="-", color="b")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Tweet")
    ax.set_title("Tweet Volume Over Time")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # 🔹 Distribusi Retweets & Likes
    st.subheader("📊 Distribusi Retweets & Likes")
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    sns.histplot(df["retweets"], bins=30, kde=True, ax=ax[0], color="blue")
    ax[0].set_title("Distribusi Retweets")
    sns.histplot(df["likes"], bins=30, kde=True, ax=ax[1], color="green")
    ax[1].set_title("Distribusi Likes")
    st.pyplot(fig)

    # 🔹 Top 10 Pengguna Paling Aktif
    st.subheader("👤 Top 10 Pengguna Paling Aktif")
