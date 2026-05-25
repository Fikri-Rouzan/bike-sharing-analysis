import pandas as pd
import streamlit as st
import plotly.express as px


@st.cache_data
def load_data():
    day_df = pd.read_csv("data/bike_sharing_day.csv")
    hour_df = pd.read_csv("data/bike_sharing_hour.csv")

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

    date_range = st.date_input(
        label="Pilih Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        st.warning(
            "⚠️ Silakan pilih tanggal mulai dan tanggal akhir untuk memproses data."
        )
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
st.title("Dashboard Analisis Penyewaan Sepeda 🚲")
st.markdown("Menampilkan insight dan visualisasi dari Bike Sharing Dataset.")

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
season_weather_df = (
    main_day_df.groupby(["season", "weathersit"])["cnt"].mean().reset_index()
)

fig1 = px.bar(
    season_weather_df,
    x="season",
    y="cnt",
    color="weathersit",
    barmode="group",
    category_orders={"season": ["Semi", "Panas", "Gugur", "Dingin"]},
    title="Rata-Rata Penyewaan Berdasarkan Musim dan Cuaca",
    labels={
        "season": "Musim",
        "cnt": "Rata-Rata Penyewaan",
        "weathersit": "Kondisi Cuaca",
    },
    color_discrete_sequence=px.colors.sequential.Blues_r,
)

# Posisi legend
fig1.update_layout(
    legend=dict(
        title="Kondisi Cuaca",
        orientation="h",
        yanchor="top",
        y=-0.4,
        xanchor="center",
        x=0.5,
    )
)
st.plotly_chart(fig1, width="stretch")

# Insight visualisasi 1
with st.expander("Lihat Insight"):
    st.markdown("""
    - Dari grafik terlihat jelas bahwa musim gugur menyumbang jumlah penyewaan sepeda tertinggi dibandingkan musim lainnya. Sebaliknya, musim semi adalah waktu yang paling sepi penyewa.
    - Terlepas dari apa pun musimnya, cuaca cerah selalu menjadi kondisi favorit pelanggan untuk menyewa sepeda. Saat cuaca berubah menjadi berawan, terjadi penurunan jumlah penyewa. Penurunan ini semakin tajam dan drastis saat cuaca buruk seperti hujan/bersalju. Hal ini menunjukkan bahwa operasional bisnis ini sangat rentan terhadap perubahan cuaca.
    """)

st.markdown("---")

# Visualisasi 2
st.subheader("Pola Penyewaan Sepeda Berdasarkan Jam di Hari Kerja dan Hari Libur")
hourly_trend_df = (
    main_hour_df.groupby(["hr", "Keterangan Hari"])["cnt"].mean().reset_index()
)

fig2 = px.line(
    hourly_trend_df,
    x="hr",
    y="cnt",
    color="Keterangan Hari",
    markers=True,
    title="Tren Penyewaan Berdasarkan Jam Operasional",
    labels={"hr": "Jam (0 - 23)", "cnt": "Rata-Rata Penyewaan"},
    color_discrete_map={"Hari Libur/Akhir Pekan": "#ff7f0e", "Hari Kerja": "#1f77b4"},
)

# Posisi legend
fig2.update_layout(
    legend=dict(
        title="Keterangan Hari",
        orientation="h",
        yanchor="top",
        y=-0.4,
        xanchor="center",
        x=0.5,
    )
)

fig2.update_xaxes(dtick=1, tickangle=-45)
st.plotly_chart(fig2, width="stretch")

# Insight visualisasi 2
with st.expander("Lihat Insight"):
    st.markdown("""
    - Terdapat dua puncak lonjakan aktivitas yang sangat menonjol, yaitu **sekitar pukul 08:00 pagi** dan rentang **pukul 17:00 hingga 18:00 sore** pada hari kerja. Pola ini mengonfirmasi bahwa pada hari kerja, mayoritas sepeda disewa oleh para pelanggan untuk mobilitas berangkat dan pulang bekerja atau bersekolah.
    - Grafik penyewaan membentuk kurva cembung tunggal pada hari libur/akhir pekan. Penyewaan mulai stabil meningkat sejak pagi hari dan mencapai puncaknya pada siang hingga sore hari (**sekitar pukul 12:00 - 16:00**). Hal ini mengindikasikan bahwa pada hari libur, pelanggan menyewa sepeda untuk keperluan rekreasi, jalan-jalan santai, atau berolahraga, bukan untuk mobilitas yang terburu-buru.
    """)

st.markdown("---")

# Visualisasi 3
st.subheader("Rata-Rata Penyewaan Sepeda Berdasarkan Cluster Waktu")
time_cluster_df = (
    main_hour_df.groupby("time_category", observed=True)["cnt"].mean().reset_index()
)

max_value = time_cluster_df["cnt"].max()
colors = [
    "#1f77b4" if val == max_value else "#aec7e8" for val in time_cluster_df["cnt"]
]

fig3 = px.bar(
    time_cluster_df,
    x="time_category",
    y="cnt",
    title="Cluster Waktu (Binning) Penyewaan Sepeda",
    labels={"time_category": "Cluster Waktu (Binning)", "cnt": "Rata-Rata Penyewaan"},
)

fig3.update_traces(marker_color=colors)
st.plotly_chart(fig3, width="stretch")

# Insight visualisasi 3
with st.expander("Lihat Insight"):
    st.markdown("""
    - Melalui teknik pengelompokan (*Binning*), rentang waktu 24 jam berhasil disederhanakan menjadi 4 *cluster* utama, yaitu Pagi (03:00 - 10:00), Siang (11:00 - 14:00), Sore (15:00 - 19:00), dan Malam (20:00 - 02:00).
    - Visualisasi mengonfirmasi bahwa periode **Sore** memiliki rata-rata penyewaan sepeda tertinggi, diikuti oleh waktu siang dan pagi. Dominasi pada waktu sore ini sangat selaras dengan lonjakan aktivitas komuter masyarakat saat pulang kerja atau sekolah. Sebaliknya, waktu malam mencatat aktivitas penyewaan terendah seiring dengan menurunnya mobilitas masyarakat di luar ruangan.
    """)

st.markdown("---")

# Kesimpulan
st.subheader("Kesimpulan")

# Kesimpulan visualisasi 1
with st.expander("Kesimpulan Visualisasi 1"):
    st.info("""
    Musim dan cuaca memiliki dampak yang sangat signifikan terhadap bisnis penyewaan sepeda. Musim gugur adalah waktu 
    yang paling menguntungkan dengan rata-rata penyewaan tertinggi, sedangkan musim semi merupakan titik terendah. Dari 
    segi cuaca, mayoritas pelanggan sangat memilih untuk menyewa sepeda pada cuaca cerah. Sebaliknya, terjadi penurunan 
    penyewaan yang sangat drastis ketika cuaca berubah menjadi buruk (hujan/bersalju). Oleh karena itu, persiapan 
    operasional dan perawatan sepeda paling baik difokuskan pada saat cuaca buruk ketika permintaan sedang rendah.
    """)

# Kesimpulan visualisasi 2
with st.expander("Kesimpulan Visualisasi 2"):
    st.info("""
    Terdapat perbedaan pola perilaku pelanggan yang sangat kontras antara hari kerja dan hari libur. Pada hari kerja, 
    pola penyewaan membentuk dua puncak lonjakan pada jam 08:00 pagi dan 17:00-18:00 sore, yang merupakan jam berangkat 
    dan pulang bekerja atau bersekolah. Hal ini menunjukkan bahwa sepeda digunakan sebagai alat transportasi komuter harian. 
    Sebaliknya, pada hari libur, polanya berubah menjadi satu puncak yang landai di siang hingga sore hari 
    (pukul 12:00-16:00), mengindikasikan bahwa penggunaan sepeda lebih condong untuk rekreasi atau olahraga santai.
    """)

# Kesimpulan visualisasi 3
with st.expander("Kesimpulan Visualisasi 3"):
    st.info("""
    Melalui teknik pengelompokan waktu (binning), dapat disimpulkan bahwa "Sore" (15:00 - 19:00) merupakan periode puncak 
    operasional dengan tingkat penyewaan tertinggi. Tingginya permintaan di rentang waktu ini mengonfirmasi besarnya porsi 
    pelanggan komuter. Sebagai rekomendasi operasional, pihak pengelola perlu memastikan ketersediaan armada sepeda yang 
    maksimal di stasiun-stasiun penyewaan menjelang sore hari. Sementara itu, periode "Malam" yang menjadi titik terendah 
    penyewaan dapat dimanfaatkan secara optimal untuk penataan ulang sepeda atau pemeliharaan ringan.
    """)

# Footer
st.markdown("---")
st.caption("© 2026 Muhammad Fikri Rouzan Ash Shidik")
