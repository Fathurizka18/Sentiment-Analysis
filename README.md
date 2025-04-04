# Analisis Data Twitter: EDA, Sentiment & Emotion Analysis, dan Social Network Analysis

## **Deskripsi Proyek**
Proyek ini bertujuan untuk menganalisis data Twitter menggunakan beberapa teknik utama:
1. **Exploratory Data Analysis (EDA)**: Menyediakan ringkasan statistik, distribusi tweet, dan aktivitas pengguna.
2. **Sentiment & Emotion Analysis (SEA)**: Mengklasifikasikan tweet berdasarkan sentimen (positif, negatif, netral) serta emosi yang terkandung.
3. **Social Network Analysis (SNA)**: Mengidentifikasi pengguna berpengaruh dan pola interaksi dalam jaringan Twitter.

Aplikasi ini dikembangkan menggunakan **Streamlit** untuk visualisasi yang interaktif dan user-friendly.

---

## **Struktur Proyek**
```
|-- dataset/
|   |-- twitter_data.csv  # Dataset utama yang digunakan
|
|-- notebooks/
|   |-- eda.ipynb                 # Notebook EDA
|   |-- sentiment_emotion.ipynb    # Notebook Sentiment & Emotion Analysis
|   |-- sna.ipynb                  # Notebook Social Network Analysis
|
|-- app/
|   |-- main.py                    # Aplikasi Streamlit
|   |-- utils.py                    # Fungsi bantu untuk analisis dan visualisasi
|
|-- reports/
|   |-- sentiment_distribution.png  # Grafik distribusi sentimen
|   |-- emotion_distribution.png    # Grafik distribusi emosi
|   |-- social_network.png          # Visualisasi jaringan sosial
|
|-- README.md                       # Dokumentasi proyek ini
```

---

## **Instalasi**
### **Persyaratan**
Sebelum menjalankan proyek ini, pastikan Anda telah menginstal dependensi yang diperlukan:
- Python 3.8+
- Jupyter Notebook
- Streamlit
- Pandas, NumPy, Matplotlib, Seaborn
- Scikit-learn
- NetworkX
- Tweepy (jika mengambil data real-time dari Twitter API)

### **Cara Instalasi**
1. Clone repository ini:
   ```bash
   git clone https://github.com/username/twitter-analysis.git
   cd twitter-analysis
   ```
2. Buat virtual environment (opsional):
   ```bash
   python -m venv env
   source env/bin/activate  # Untuk Linux/macOS
   env\Scripts\activate     # Untuk Windows
   ```
3. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Cara Penggunaan**
1. Jalankan **Jupyter Notebook** untuk eksplorasi awal data:
   ```bash
   jupyter notebook
   ```
2. Jalankan aplikasi **Streamlit** untuk analisis interaktif:
   ```bash
   streamlit run app/main.py
   ```
3. Hasil analisis akan ditampilkan dalam aplikasi web interaktif.

---

## **Hasil Analisis**
### **1. Sentiment Analysis**
- Mayoritas tweet bersifat **netral (95.2%)**, sedangkan **sentimen positif (3.3%) dan negatif (1.5%)** sangat kecil.
- Ini menunjukkan bahwa percakapan di Twitter terkait topik ini lebih banyak berupa informasi tanpa ekspresi emosi yang kuat.

### **2. Emotion Analysis**
- **Tidak ada emosi yang terdeteksi dalam dataset ini**.
- terlalu singkat pesan yang dikirimkan sehingga sulit menganalisis emosi user
- Kemungkinan besar terjadi kesalahan dalam pemrosesan data atau model yang digunakan kurang sesuai.

### **3. Social Network Analysis**
- **RestyResseh** adalah akun dengan pengaruh tertinggi berdasarkan **centrality score**.
- Struktur jaringan menunjukkan bahwa ada **beberapa akun utama yang menjadi pusat percakapan**.
- Percakapan bersifat **padat dan terhubung erat**, menunjukkan diskusi yang aktif dan terorganisir.

---

## **Kesimpulan**
- **Percakapan di Twitter cenderung bersifat informatif dan netral** tanpa ekspresi emosi yang kuat.
- **Analisis jaringan sosial mengidentifikasi akun-akun berpengaruh** yang menjadi pusat percakapan.
- **Model analisis emosi perlu dievaluasi ulang** untuk memastikan deteksi yang lebih akurat.

---

**Dibuat oleh:** Fathu Rizka
📧 Email: Fathurizka9@gmail.com
