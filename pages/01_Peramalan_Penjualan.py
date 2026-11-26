
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import load_data


# ==========================================
# FUNGSI FORMAT ANGKA
# ==========================================

def format_angka_id(nilai, desimal=2):
    angka = f"{nilai:,.{desimal}f}"
    angka = angka.replace(",", "X")
    angka = angka.replace(".", ",")
    angka = angka.replace("X", ".")
    return angka


def format_miliar(nilai):
    return f"{format_angka_id(nilai / 1e9)} M"


# ==========================================
# 1. JUDUL DAN DATA
# ==========================================

st.title("Peramalan Penjualan Neto")

df = load_data()

st.write(
    """
    Halaman ini menyajikan hasil peramalan penjualan neto
    PT Enseval Putera Megatrading Tbk berdasarkan data
    keuangan konsolidasian kuartalan.
    """
)

urutan_kuartal = {
    "Q1": 1,
    "Q2": 2,
    "Q3": 3,
    "Q4": 4
}

df_historis = df.copy()

df_historis["TAHUN"] = pd.to_numeric(
    df_historis["TAHUN"]
)

df_historis["PERIODE"] = (
    df_historis["PERIODE"].astype(str)
)

df_historis["URUTAN_KUARTAL"] = (
    df_historis["PERIODE"].map(urutan_kuartal)
)

# Data historis dibatasi sampai Q4 2025
df_historis = df_historis[
    df_historis["TAHUN"] <= 2025
].copy()

df_historis = df_historis.sort_values(
    ["TAHUN", "URUTAN_KUARTAL"]
)

df_historis["PERIODE_LABEL"] = (
    df_historis["TAHUN"].astype(str)
    + " "
    + df_historis["PERIODE"]
)


# ==========================================
# 2. DATA FORECAST DAN AKTUAL 2026
# ==========================================

df_forecast = pd.DataFrame({
    "TAHUN": [2026, 2026, 2026, 2026],
    "PERIODE": ["Q1", "Q2", "Q3", "Q4"],
    "FORECAST": [
        8938550820255,
        8512022648545,
        8992013270189,
        9104962679681
    ],
    "AKTUAL": [
        9057132801049,
        9214551912263,
        8832539051375,
        None
    ]
})

df_forecast["PERIODE_LABEL"] = (
    df_forecast["TAHUN"].astype(str)
    + " "
    + df_forecast["PERIODE"]
)


# ==========================================
# 3. RINGKASAN HASIL PERAMALAN
# ==========================================

st.divider()

st.subheader("Ringkasan Hasil Peramalan")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Model Terpilih",
        "SARIMA"
    )

with col2:
    st.metric(
        "Ordo SARIMA",
        "(0,1,0)(1,0,0)₄"
    )

with col3:
    st.metric(
        "MAPE Rolling-Origin",
        "3,64%"
    )

col4, col5 = st.columns(2)

with col4:
    st.metric(
        "MAE",
        "278,15 M"
    )

with col5:
    st.metric(
        "RMSE",
        "368,54 M"
    )

st.caption(
    """
    Evaluasi model dilakukan menggunakan rolling-origin
    dengan skema expanding window dan horizon satu kuartal.
    """
)

st.divider()


# ==========================================
# 4. GRAFIK HISTORIS DAN FORECAST
# ==========================================

st.subheader("Grafik Historis dan Hasil Peramalan")

fig = go.Figure()

# Data historis sampai Q4 2025
fig.add_trace(
    go.Scatter(
        x=df_historis["PERIODE_LABEL"],
        y=df_historis["PENJUALAN NETO"],
        mode="lines+markers",
        name="Penjualan Historis"
    )
)

# Forecast 2026
fig.add_trace(
    go.Scatter(
        x=df_forecast["PERIODE_LABEL"],
        y=df_forecast["FORECAST"],
        mode="lines+markers",
        name="Forecast SARIMA",
        line=dict(dash="dash")
    )
)

# Aktual 2026
fig.add_trace(
    go.Scatter(
        x=df_forecast["PERIODE_LABEL"],
        y=df_forecast["AKTUAL"],
        mode="lines+markers",
        name="Penjualan Aktual 2026"
    )
)

periode_grafik = (
    df_historis["PERIODE_LABEL"].tolist()
    + df_forecast["PERIODE_LABEL"].tolist()
)

fig.update_layout(
    title="Penjualan Historis dan Hasil Peramalan SARIMA",
    xaxis_title="Periode",
    yaxis_title="Penjualan Neto (Rp)",
    hovermode="x unified",
    height=500,
    xaxis=dict(
        type="category",
        categoryorder="array",
        categoryarray=periode_grafik,
        tickangle=-45,
        automargin=True
    ),
    margin=dict(
        l=60,
        r=30,
        t=60,
        b=100
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.caption(
    """
    Garis historis menunjukkan realisasi penjualan sampai
    Q4 2025. Garis putus-putus menunjukkan hasil forecast
    SARIMA 2026, sedangkan garis aktual menunjukkan realisasi
    Q1–Q3 2026. Data aktual Q4 2026 belum tersedia.
    """
)

st.divider()


# ==========================================
# 5. PERBANDINGAN EVALUASI MODEL
# ==========================================

st.subheader("Perbandingan Evaluasi Model")

df_evaluasi = pd.DataFrame({
    "Model": [
        "SARIMA",
        "Holt-Winters",
        "Holt Linear",
        "Holt Damped",
        "SARIMAX",
        "Naive Drift"
    ],
    "MAE (M)": [
        278.15,
        278.45,
        279.81,
        286.60,
        300.71,
        328.13
    ],
    "RMSE (M)": [
        368.54,
        380.83,
        336.32,
        344.39,
        412.98,
        385.67
    ],
    "MAPE (%)": [
        3.64,
        3.65,
        3.65,
        3.74,
        3.98,
        4.26
    ],
    "Std MAPE Tahunan": [
        0.57,
        1.02,
        0.58,
        0.66,
        1.46,
        0.84
    ]
})

st.dataframe(
    df_evaluasi.style.format({
        "MAE (M)": lambda x: format_angka_id(x),
        "RMSE (M)": lambda x: format_angka_id(x),
        "MAPE (%)": lambda x: format_angka_id(x) + "%",
        "Std MAPE Tahunan": lambda x: format_angka_id(x)
    }),
    use_container_width=True,
    hide_index=True
)

st.caption(
    """
    MAE dan RMSE dinyatakan dalam miliar rupiah.
    MAPE menunjukkan rata-rata persentase kesalahan,
    sedangkan Std MAPE Tahunan menggambarkan variasi
    MAPE antarperiode tahunan.
    """
)

st.divider()


# ==========================================
# 6. DASAR PEMILIHAN MODEL
# ==========================================

st.subheader("Dasar Pemilihan Model")

st.markdown(
    """
    Pemilihan model dilakukan melalui seleksi konfigurasi
    SARIMA dan perbandingan performa dengan beberapa
    metode peramalan lainnya.
    """
)

st.markdown("**1. Seleksi konfigurasi SARIMA**")

st.write(
    """
    Kandidat konfigurasi SARIMA dievaluasi berdasarkan
    keberhasilan estimasi dan nilai Bayesian Information
    Criterion (BIC). Konfigurasi dengan BIC terendah
    dipilih di antara kandidat yang memenuhi kriteria
    estimasi.
    """
)

st.info(
    """
    Model SARIMA final yang digunakan untuk meramalkan
    penjualan neto tahun 2026 adalah SARIMA
    (0,1,0)(1,0,0)₄.
    """
)

st.markdown("**2. Perbandingan performa antar-model**")

st.write(
    """
    Berdasarkan evaluasi rolling-origin, SARIMA menghasilkan
    MAPE, MAE, dan simpangan baku MAPE tahunan terendah.
    Sementara itu, RMSE terendah diperoleh model Holt Linear.
    """
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "MAPE SARIMA",
        "3,64%"
    )

with col2:
    st.metric(
        "MAE SARIMA",
        "278,15 M"
    )

with col3:
    st.metric(
        "Std. MAPE Tahunan",
        "0,57"
    )

st.markdown("**3. Pertimbangan pemilihan model akhir**")

st.write(
    """
    Uji Diebold-Mariano dengan koreksi Holm tidak
    menunjukkan perbedaan akurasi yang signifikan
    antar-model. Oleh karena itu, SARIMA dipilih
    berdasarkan pertimbangan performa pada beberapa
    metrik evaluasi dan kestabilan kesalahan peramalan.

    Pemilihan tersebut tidak berarti SARIMA terbukti
    secara statistik lebih unggul daripada seluruh
    model pembanding.
    """
)

st.divider()


# ==========================================
# 7. EVALUASI TERHADAP AKTUAL 2026
# ==========================================

st.subheader("Evaluasi terhadap Data Aktual 2026")

df_evaluasi_aktual = df_forecast.dropna(
    subset=["FORECAST", "AKTUAL"]
).copy()

df_evaluasi_aktual["ERROR"] = (
    df_evaluasi_aktual["AKTUAL"]
    - df_evaluasi_aktual["FORECAST"]
)

df_evaluasi_aktual["APE (%)"] = (
    abs(df_evaluasi_aktual["ERROR"])
    / df_evaluasi_aktual["AKTUAL"]
    * 100
)

mae_aktual = abs(
    df_evaluasi_aktual["ERROR"]
).mean()

rmse_aktual = (
    df_evaluasi_aktual["ERROR"] ** 2
).mean() ** 0.5

mape_aktual = df_evaluasi_aktual["APE (%)"].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "MAE Aktual",
        format_miliar(mae_aktual)
    )

with col2:
    st.metric(
        "RMSE Aktual",
        format_miliar(rmse_aktual)
    )

with col3:
    st.metric(
        "MAPE Aktual",
        format_angka_id(mape_aktual) + "%"
    )

st.caption(
    f"""
    Evaluasi aktual dihitung berdasarkan
    {len(df_evaluasi_aktual)} kuartal yang telah memiliki
    data realisasi, yaitu Q1–Q3 2026.
    """
)

st.divider()


# ==========================================
# 8. TABEL FORECAST DAN AKTUAL
# ==========================================

st.subheader("Hasil Peramalan Penjualan Neto 2026")

df_tabel_forecast = df_forecast[
    ["PERIODE_LABEL", "FORECAST", "AKTUAL"]
].copy()

df_tabel_forecast["APE (%)"] = (
    abs(
        df_tabel_forecast["AKTUAL"]
        - df_tabel_forecast["FORECAST"]
    )
    / df_tabel_forecast["AKTUAL"]
    * 100
)

df_tabel_forecast["FORECAST (T)"] = (
    df_tabel_forecast["FORECAST"] / 1e12
)

df_tabel_forecast["AKTUAL (T)"] = (
    df_tabel_forecast["AKTUAL"] / 1e12
)

df_tabel_forecast = df_tabel_forecast[
    [
        "PERIODE_LABEL",
        "FORECAST (T)",
        "AKTUAL (T)",
        "APE (%)"
    ]
].copy()

df_tabel_forecast.columns = [
    "Kuartal",
    "Forecast (T)",
    "Aktual (T)",
    "APE (%)"
]

st.dataframe(
    df_tabel_forecast.style.format(
        {
            "Forecast (T)": lambda x: format_angka_id(x),
            "Aktual (T)": lambda x: format_angka_id(x),
            "APE (%)": lambda x: format_angka_id(x) + "%"
        },
        na_rep="—"
    ),
    use_container_width=True,
    hide_index=True
)

st.caption(
    """
    Nilai disajikan dalam triliun rupiah. APE merupakan
    persentase kesalahan absolut antara hasil forecast
    dan data aktual. Tanda — menunjukkan data aktual
    yang belum tersedia.
    """
)

st.divider()


# ==========================================
# 9. INTERPRETASI HASIL PERAMALAN
# ==========================================

st.subheader("Interpretasi Hasil Peramalan")

st.markdown(
    """
    **1. Pola penjualan neto**

    Hasil peramalan SARIMA menunjukkan bahwa penjualan neto
    diproyeksikan sebesar Rp8,94 triliun pada Q1 2026.
    Penjualan kemudian diperkirakan sebesar Rp8,51 triliun
    pada Q2, Rp8,99 triliun pada Q3, dan Rp9,10 triliun
    pada Q4 2026.

    **2. Perbandingan hasil peramalan dengan aktual**

    Hasil aktual Q1–Q3 2026 dapat dibandingkan dengan
    proyeksi model untuk melihat besarnya kesalahan
    peramalan pada periode yang telah terealisasi.
    Rincian kesalahan setiap kuartal ditampilkan pada
    tabel hasil peramalan di atas.

    **3. Kinerja peramalan**

    Evaluasi rolling-origin menghasilkan MAPE sebesar
    3,64%. Sementara itu, evaluasi terhadap aktual
    Q1–Q3 2026 menghasilkan MAPE sebesar
    """
    + f"**{format_angka_id(mape_aktual)}%**."
)

st.write(
    """
    Kedua nilai tersebut berasal dari periode evaluasi
    yang berbeda sehingga tidak dapat dianggap sebagai
    pengujian yang sama.

    **4. Proyeksi Q4 2026**

    Model memperkirakan penjualan neto Q4 2026 sebesar
    Rp9,10 triliun. Nilai tersebut merupakan proyeksi,
    bukan realisasi penjualan.
    """
)

st.warning(
    """
    Hasil peramalan merupakan estimasi berdasarkan pola
    historis dan asumsi model. Perubahan kondisi bisnis
    maupun faktor eksternal dapat menyebabkan realisasi
    berbeda dari hasil proyeksi.
    """
)
