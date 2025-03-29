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
    df = pd.read_csv("twitter_data_cleaned.csv.gz", compression="gzip", low_memory=False)
    
    # Konversi waktu & hapus "WIB"
    df["created_at"] = df["created_at"].astype(str).str.replace(" WIB", "", regex=False)
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    # Isi nilai kosong dengan "Unknown"
    df.fillna("Unknown", inplace=True)

df = load_data()  # Panggil fungsi setelah definisi

    df = pd.read_csv("twitter_data_cleaned.csv.gz", compression="gzip", low_memory=False)
print(df.head())
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
    st.subheader("📌 Kolom dalam Dataset")
st.write(df.columns.tolist())  # Menampilkan daftar nama kolom yang tersedia
st.write(df.head())

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

    
    print(df.columns)

    # 🔹 Top 10 Pengguna Paling Aktif
    st.subheader("👤 Top 10 Pengguna Paling Aktif")
    top_users = df["username"].value_counts().head(10)
    st.bar_chart(top_users)

# =====================================
# 📌 4. Sentiment Analysis (Swifter + TextBlob)
# =====================================
elif menu == "Sentiment Analysis":
    st.title("😊 Sentiment & Emotion Analysis")

    @st.cache_data
    def analyze_sentiment_fast(texts):
        def get_sentiment(text):
            analysis = TextBlob(text)
            if analysis.sentiment.polarity > 0:
                return "Positive"
            elif analysis.sentiment.polarity < 0:
                return "Negative"
            else:
                return "Neutral"

        return texts.swifter.apply(get_sentiment)

    if "sentiment" not in df.columns:
        df["sentiment"] = analyze_sentiment_fast(df["tweet"].astype(str))

    # 🔹 Distribusi Sentimen
    st.subheader("📊 Distribusi Sentimen")
    sentiment_counts = df["sentiment"].value_counts()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%1.1f%%", colors=["green", "red", "gray"])
    ax.set_title("Sentiment Distribution")
    st.pyplot(fig)

    # 🔹 Contoh Tweet Berdasarkan Sentimen
    st.subheader("📌 Contoh Tweet Berdasarkan Sentimen")
    sentiment_choice = st.radio("Pilih Sentimen:", ["Positive", "Negative", "Neutral"])
    st.write(df[df["sentiment"] == sentiment_choice][["username", "tweet"]].sample(5))

# ========================================
# 📌 5. Social Network Analysis (SNA)
# ========================================
elif menu == "Social Network Analysis":
    st.title("🌐 Social Network Analysis (SNA)")

    df_rt = df.dropna(subset=["user_rt"])  # Hanya ambil data dengan retweet

    if len(df_rt) == 0:
        st.warning("❌ Tidak ada data retweet dalam dataset.")
    else:
        MAX_NODES = 50  # Batasi jumlah node agar tidak berat
        G = nx.DiGraph()
        edge_count = 0

        for _, row in df_rt.iterrows():
            if edge_count >= MAX_NODES:
                break
            G.add_edge(row["user_rt"], row["username"])
            edge_count += 1

        st.subheader(f"📌 Retweet Network Graph (dibatasi {MAX_NODES} node)")
        
        fig, ax = plt.subplots(figsize=(12, 8))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=500, font_size=8, ax=ax)
        st.pyplot(fig)

        # 🔹 Degree Centrality untuk Influencer Analysis
        st.subheader("👑 Top Influencers Berdasarkan Degree Centrality")
        centrality = nx.degree_centrality(G)
        top_influencers = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        influencer_df = pd.DataFrame(top_influencers, columns=["Username", "Centrality Score"])
        st.dataframe(influencer_df)

# ================================
# 📌 Footer Information
# ================================
st.sidebar.info("Aplikasi ini dibuat menggunakan **Streamlit** untuk analisis data Twitter.")

