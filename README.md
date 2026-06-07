# Bike Sharing Analysis

## 📌 Deskripsi

Dashboard ini dirancang untuk menganalisis data penggunaan sistem berbagi sepeda guna mengidentifikasi pola, tren, dan berbagai faktor yang memengaruhi jumlah penyewaan. Melalui eksplorasi data historis, sistem ini memetakan volume penyewaan berdasarkan pengaruh kondisi cuaca, parameter waktu, serta variasi musim. Hasil analisis dari dashboard ini ditujukan untuk membantu pengelola dalam memahami fluktuasi permintaan daya angkut sepeda guna mendukung manajemen operasional dan efisiensi distribusi armada di area perkotaan.

---

## 💾 Dataset

Dataset yang digunakan dalam dashboard ini memuat catatan riwayat aktivitas penyewaan sepeda yang dikorelasikan dengan kondisi cuaca dan waktu. Data terstruktur ini terbagi menjadi dua basis pencatatan, yaitu data harian yang memuat hasil agregasi aktivitas penyewaan per hari serta data per jam yang merekam aktivitas secara mendetail setiap jamnya. Kedua bagian data tersebut memuat parameter penting seperti indeks cuaca, musim, temperatur, kelembapan, kecepatan angin, keterangan hari kerja atau hari libur, serta jumlah total penyewaan baik dari pengguna biasa maupun pengguna yang telah terdaftar.

---

## 🛠️ Tech Stack

| Kategori                    | Teknologi yang Digunakan                    |
| :-------------------------- | :------------------------------------------ |
| 🌐 **Programming Language** | `Python`                                    |
| 🌱 **Environment**          | `Jupyter Notebook`                          |
| 🧩 **Framework**            | `Streamlit`                                 |
| ⚛️ **Libraries**            | `pandas`, `Matplotlib`, `seaborn`, `Plotly` |
| ⚡ **Tool**                 | `Google Colab`                              |
| 🚀 **Deployment**           | `Streamlit Community Cloud`                 |

---

## ⚙️ Petunjuk Pengaturan

1. **Prasyarat**
   - Python 3.11 atau lebih baru.
   - Git terinstal di komputer.

2. **Clone Repositori**

```bash
git clone https://github.com/Fikri-Rouzan/bike-sharing-analysis.git
cd bike-sharing-analysis
```

3. **Buat Virtual Environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

4. **Install Dependensi**

```bash
pip install -r requirements.txt
```

5. **Menjalankan Dashboard Streamlit**

```bash
streamlit run dashboard/dashboard.py
```
