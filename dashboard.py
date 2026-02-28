import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


@st.cache_data
def load_data():
    day_df = pd.read_csv("bike_sharing_day_dataset.csv")
    hour_df = pd.read_csv("bike_sharing_hour_dataset.csv")

    # Mengubah tipe data dteday
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

    # Memetakan nilai numerik menjadi keterangan teks
    season_mapping = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}
    weather_mapping = {
        1: "Cerah",
        2: "Berawan",
        3: "Hujan/Bersalju",
        4: "Badai",
    }

    day_df["season"] = day_df["season"].map(season_mapping)
    day_df["weathersit"] = day_df["weathersit"].map(weather_mapping)
    hour_df["season"] = hour_df["season"].map(season_mapping)
    hour_df["weathersit"] = hour_df["weathersit"].map(weather_mapping)

    # Memetakan keterangan hari untuk data penyewaan sepeda per jam
    hour_df["Keterangan Hari"] = hour_df["workingday"].map(
        {0: "Hari Libur/Akhir Pekan", 1: "Hari Kerja"}
    )

    # Binning pada data penyewaan sepeda per jam
    def categorize_time(hour):
        if 3 <= hour <= 10:
            return "Pagi"
        elif 11 <= hour <= 14:
            return "Siang"
        elif 15 <= hour <= 19:
            return "Sore"
        else:
            return "Malam"

    # Kolom baru
    hour_df["time_category"] = hour_df["hr"].apply(categorize_time)
    hour_df["time_category"] = pd.Categorical(
        hour_df["time_category"],
        categories=["Pagi", "Siang", "Sore", "Malam"],
        ordered=True,
    )

    return day_df, hour_df


day_df, hour_df = load_data()

# Dashboard
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# Rentang tanggal dari dataset
min_date = day_df["dteday"].dt.date.min()
max_date = day_df["dteday"].dt.date.max()

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2972/2972185.png", width=150)
    st.title("Bike Sharing Data")

    try:
        start_date, end_date = st.date_input(
            label="Pilih Rentang Waktu",
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date],
        )
    except ValueError:
        st.error("Silakan pilih tanggal akhir untuk memproses data.")
        st.stop()

    st.caption(
        "Dashboard ini dibuat untuk menganalisis pola penyewaan sepeda berdasarkan faktor cuaca, musim, dan jam operasional."
    )

# Memfilter dataset berdasarkan rentang tanggal yang dipilih
main_day_df = day_df[
    (day_df["dteday"].dt.date >= start_date) & (day_df["dteday"].dt.date <= end_date)
]

main_hour_df = hour_df[
    (hour_df["dteday"].dt.date >= start_date) & (hour_df["dteday"].dt.date <= end_date)
]

# Header
st.title("🚲 Dashboard Analisis Penyewaan Sepeda")
st.markdown("Menampilkan insight dan visualisasi  dari Bike Sharing Dataset.")

# Metrik ringkasan
col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = main_day_df["cnt"].sum()
    st.metric("Total Penyewaan Sepeda", value=f"{total_rentals:,}")
with col2:
    max_rentals_day = main_day_df["cnt"].max() if not main_day_df.empty else 0
    st.metric("Rekor Harian Tertinggi", value=f"{max_rentals_day:,}")
with col3:
    avg_rentals_day = int(main_day_df["cnt"].mean()) if not main_day_df.empty else 0
    st.metric("Rata-Rata Penyewaan Harian", value=f"{avg_rentals_day:,}")

st.markdown("---")

# Visualisasi 1
st.subheader("Pengaruh Musim dan Cuaca Terhadap Penyewaan Sepeda Harian")
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="season",
    y="cnt",
    hue="weathersit",
    data=main_day_df,
    palette="viridis",
    errorbar=None,
    ax=ax1,
)
ax1.set_title("Rata-Rata Penyewaan Berdasarkan Musim dan Cuaca", fontsize=14)
ax1.set_xlabel("Musim")
ax1.set_ylabel("Rata-Rata Penyewaan")
ax1.legend(title="Kondisi Cuaca")
st.pyplot(fig1)

st.markdown("---")

# Visualisasi 2
st.subheader("Pola Penyewaan Sepeda Berdasarkan Jam di Hari Kerja dan Hari Libur")
fig2, ax2 = plt.subplots(figsize=(12, 6))
custom_color = {"Hari Libur/Akhir Pekan": "red", "Hari Kerja": "blue"}
sns.lineplot(
    x="hr",
    y="cnt",
    hue="Keterangan Hari",
    data=main_hour_df,
    palette=custom_color,
    marker="o",
    linewidth=2,
    ax=ax2,
)
ax2.set_title("Tren Penyewaan Berdasarkan Jam Operasional", fontsize=14)
ax2.set_xlabel("Jam (0 - 23)")
ax2.set_ylabel("Rata-rata Penyewaan")
ax2.set_xticks(range(0, 24))
st.pyplot(fig2)

st.markdown("---")

# Visualisasi 3
st.subheader("Rata-Rata Penyewaan Sepeda Berdasarkan Cluster Waktu")
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="time_category",
    y="cnt",
    hue="time_category",
    data=main_hour_df,
    palette="magma",
    errorbar=None,
    legend=False,
    ax=ax3,
)
ax3.set_title("Cluster Waktu (Binning) Penyewaan Sepeda", fontsize=14)
ax3.set_xlabel("Cluster Waktu (Binning)")
ax3.set_ylabel("Rata-Rata Penyewaan")
st.pyplot(fig3)

st.markdown("---")
st.caption("© 2026 Muhammad Fikri Rouzan Ash Shidik")
