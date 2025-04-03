import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import re
import community.community_louvain as community_louvain
from textblob import TextBlob
import swifter

# =====================
# 📌 1. Load Dataset (Cache)
# =====================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("clean_twitter_data.csv", low_memory=False)
        if df.empty:
            st.warning("Dataset kosong! Pastikan file telah dimuat dengan benar.")
            return pd.DataFrame()
        
        # Konversi waktu & hapus "WIB"
        if "created_at" in df.columns:
            df["created_at"] = df["created_at"].astype(str).str.replace(" WIB", "", regex=False)
            df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        
        # Isi nilai kosong dengan "Unknown"
        df.fillna("Unknown", inplace=True)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

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
    if not df.empty:
        st.subheader("📌 Preview Data")
        st.dataframe(df.head(1000))

        st.subheader("📌 Statistik Data")
        st.write(df.describe())

        # 🔹 Tweet Volume Over Time
        if "created_at" in df.columns and pd.api.types.is_datetime64_any_dtype(df["created_at"]):
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
        
        # 🔹 Top 10 Pengguna Paling Aktif
        if "username" in df.columns:
            st.subheader("👤 Top 10 Pengguna Paling Aktif")
            top_users = df["username"].value_counts().head(10)
            st.bar_chart(top_users)
    else:
        st.warning("Dataset kosong atau tidak dimuat dengan benar.")

# =====================================
# 📌 4. Sentiment Analysis
# =====================================
elif menu == "Sentiment Analysis":
    st.title("😊 Sentiment Analysis")
    
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
        return texts.apply(get_sentiment)
    
    if "tweet" in df.columns and not df.empty:
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
        sample_size = min(5, len(df[df["sentiment"] == sentiment_choice]))
        if sample_size > 0:
            st.write(df[df["sentiment"] == sentiment_choice][["username", "tweet"]].sample(sample_size))
        else:
            st.warning("Tidak ada tweet dengan sentimen yang dipilih.")
    else:
        st.warning("Dataset kosong atau tidak memiliki kolom 'tweet'.")

# ========================================
# 📌 5. Social Network Analysis (SNA)
# ========================================
elif menu == "Social Network Analysis":
    st.title("🌐 Social Network Analysis (SNA)")
    
    def extract_mentions(text):
        return re.findall(r"@(\w+)", text)
    
    def extract_retweets(text):
        match = re.match(r"RT @(\w+)", text)
        return match.group(1) if match else None
    
    if "tweet" in df.columns and "username" in df.columns:
        df["mentions"] = df["tweet"].fillna("").astype(str).apply(extract_mentions)
        df["retweets"] = df["tweet"].fillna("").astype(str).apply(extract_retweets)
        
        G = nx.DiGraph()

        for _, row in df.iterrows():
            user = row["username"]
            mentions = row["mentions"]
            for mentioned_user in mentions:
                G.add_edge(user, mentioned_user, type="mention")
        
        for _, row in df.iterrows():
            user = row["username"]
            retweeted_user = row["retweets"]
            if retweeted_user:
                G.add_edge(user, retweeted_user, type="retweet")
        
        st.subheader("📌 Social Network Graph (Mentions & Retweets)")
        fig, ax = plt.subplots(figsize=(12, 8))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=500, font_size=8, ax=ax)
        st.pyplot(fig)
        
        st.subheader("👑 Top Influencers Berdasarkan Degree Centrality")
        degree_centrality = nx.degree_centrality(G)
        top_influencers = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        st.dataframe(pd.DataFrame(top_influencers, columns=["Username", "Centrality Score"]))
    else:
        st.warning("Dataset tidak memiliki kolom tweet atau username.")

st.sidebar.info("Aplikasi ini dibuat menggunakan **Streamlit** untuk analisis data Twitter.")
