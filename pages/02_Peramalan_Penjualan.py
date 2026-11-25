
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import load_data


# ==========================================
# 1. KONFIGURASI DAN DATA
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

# Mengurutkan data historis
urutan_kuartal = {
    "Q1": 1,
    "Q2": 2,
    "Q3": 3,
    "Q4": 4
}

df_historis = df.copy()

df_historis["PERIODE"] = (
    df_historis["PERIODE"].astype(str)
)

df_historis["URUTAN_KUARTAL"] = (
    df_historis["PERIODE"].map(urutan_kuartal)
)

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
    ],

    "APE": [
        1.31,
        7.62,
        1.81,
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

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Model Terpilih",
        "SARIMA",
        help="ARIMA(0,1,0)(1,0,0)₄"
    )

with col2:
    st.metric(
        "MAPE Rolling-Origin",
        "3,64%"
    )

col3, col4 = st.columns(2)

with col3:
    st.metric(
        "MAE",
        "278,15 M"
    )

with col4:
    st.metric(
        "RMSE",
        "368,54 M"
    )

st.caption(
    "Evaluasi menggunakan expanding-window rolling-origin "
    "periode 2023 Q1–2025 Q4 dengan horizon satu kuartal. "
    "M = miliar rupiah."
)



# ==========================================
# 4. GRAFIK HISTORIS DAN FORECAST
# ==========================================

st.divider()

st.subheader("Grafik Historis dan Hasil Peramalan")

fig = go.Figure()

# Garis penjualan historis
fig.add_trace(go.Scatter(
    x=df_historis["PERIODE_LABEL"],
    y=df_historis["PENJUALAN NETO"],
    mode="lines+markers",
    name="Penjualan Historis"
))

# Garis hasil forecast SARIMA
fig.add_trace(go.Scatter(
    x=df_forecast["PERIODE_LABEL"],
    y=df_forecast["FORECAST"],
    mode="lines+markers",
    name="Forecast SARIMA",
    line=dict(dash="dash")
))

# Garis penjualan aktual 2026
fig.add_trace(go.Scatter(
    x=df_forecast["PERIODE_LABEL"],
    y=df_forecast["AKTUAL"],
    mode="lines+markers",
    name="Penjualan Aktual 2026"
))

# Pengaturan tampilan grafik
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
    "Garis putus-putus menunjukkan hasil forecast SARIMA. "
    "Data aktual Q4 2026 belum tersedia."
)


# ==========================================
# 5. PERBANDINGAN EVALUASI MODEL
# ==========================================

st.divider()

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
        "MAE (M)": "{:.2f}",
        "RMSE (M)": "{:.2f}",
        "MAPE (%)": "{:.2f}%",
        "Std MAPE Tahunan": "{:.2f}"
    }),
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Seluruh nilai MAE dan RMSE dinyatakan dalam miliar rupiah. "
    "Evaluasi dilakukan menggunakan rolling-origin."
)


# ==========================================
# 6. DASAR PEMILIHAN MODEL
# ==========================================

st.divider()

st.subheader("Dasar Pemilihan Model")

st.write(
    """
    Model SARIMA ditetapkan sebagai model peramalan akhir
    berdasarkan kombinasi hasil evaluasi akurasi, kestabilan
    kesalahan, dan diagnostik residual.
    """
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "MAPE",
        "3,64%"
    )

with col2:
    st.metric(
        "MAE",
        "278,15 M"
    )

with col3:
    st.metric(
        "Std. MAPE Tahunan",
        "0,57"
    )

st.info(
    """
    SARIMA, Holt-Winters, dan Holt Linear memiliki tingkat
    MAPE yang relatif berdekatan. Uji Diebold-Mariano dengan
    koreksi Holm juga tidak menunjukkan perbedaan akurasi
    yang signifikan antar model.

    SARIMA dipilih karena memiliki MAE dan simpangan baku
    MAPE tahunan terendah serta residual yang tidak
    menunjukkan autokorelasi signifikan.
    """
)


# ==========================================
# 7. EVALUASI TERHADAP AKTUAL 2026
# ==========================================

st.divider()

st.subheader("Evaluasi terhadap Data Aktual 2026")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "MAE Aktual 2026",
        "326,86 M"
    )

with col2:
    st.metric(
        "RMSE Aktual 2026",
        "421,52 M"
    )

with col3:
    st.metric(
        "MAPE Aktual 2026",
        "3,58%"
    )


# ==========================================
# 8. TABEL HASIL FORECAST 2026
# ==========================================

st.divider()

st.subheader("Hasil Peramalan Penjualan Neto 2026")

df_hasil_forecast = pd.DataFrame({
    "Kuartal": [
        "Q1 2026",
        "Q2 2026",
        "Q3 2026",
        "Q4 2026"
    ],

    "Forecast (T)": [
        8.94,
        8.51,
        8.99,
        9.10
    ],

    "Aktual (T)": [
        9.06,
        9.21,
        8.83,
        None
    ],

    "APE (%)": [
        1.31,
        7.62,
        1.81,
        None
    ]
})

st.dataframe(
    df_hasil_forecast,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "T = triliun rupiah. Aktual Q4 2026 belum tersedia."
)


# ==========================================
# 9. INTERPRETASI HASIL PERAMALAN
# ==========================================

st.divider()

st.subheader("Interpretasi Hasil Peramalan")

st.markdown(
    """
    **1. Pola hasil peramalan**

    Penjualan neto diproyeksikan mencapai Rp8,94 triliun
    pada Q1 2026, kemudian turun menjadi Rp8,51 triliun
    pada Q2. Selanjutnya, penjualan diperkirakan meningkat
    menjadi Rp8,99 triliun pada Q3 dan Rp9,10 triliun
    pada Q4 2026.

    **2. Perbandingan dengan data aktual**

    Aktual Q1 dan Q3 relatif dekat dengan hasil peramalan,
    masing-masing memiliki APE sebesar 1,31% dan 1,81%.
    Sementara itu, Q2 menunjukkan selisih lebih besar
    dengan APE sebesar 7,62%.

    **3. Kinerja model**

    Evaluasi terhadap aktual Q1–Q3 2026 menghasilkan
    MAPE sebesar 3,58%. Hasil tersebut relatif dekat
    dengan MAPE rolling-origin sebesar 3,64%, meskipun
    keduanya berasal dari periode evaluasi berbeda.

    **4. Perkiraan penjualan Q4 2026**

    Model SARIMA memperkirakan penjualan neto Q4 2026
    sebesar Rp9,10 triliun. Nilai tersebut merupakan
    hasil peramalan dan belum merupakan realisasi penjualan.
    """
)
