import pandas as pd
import streamlit as st
import plotly.express as px


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

st.markdown("---")
st.caption("© 2026 Muhammad Fikri Rouzan Ash Shidik")
