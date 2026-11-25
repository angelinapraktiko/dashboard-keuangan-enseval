import plotly.express as px
import streamlit as st
from utils import load_data

# Pengaturan halaman
st.title("Ringkasan Kondisi Keuangan")

st.write(
    """
    Halaman ini menyajikan gambaran umum kondisi keuangan
    PT Enseval Putera Megatrading Tbk berdasarkan laporan
    keuangan konsolidasian kuartalan.
    """
)

st.divider()

# Memuat dan mengurutkan data
df = load_data()
df = df.sort_values("PERIODE")

# Menghitung indikator ringkasan
rata_penjualan = df["PENJUALAN NETO"].mean()
rata_ako = df["ARUS KAS OPERASI"].mean()
rata_laba = df["LABA PERIODE BERJALAN"].mean()

pertumbuhan_penjualan = (
    df["PENJUALAN NETO"].pct_change().mean() * 100
)

# Menampilkan indikator utama
st.subheader("Indikator Keuangan")

# Baris pertama
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Rata-rata Penjualan Neto",
        f"Rp {rata_penjualan / 1_000_000_000_000:.2f} T"
    )

with col2:
    st.metric(
        "Rata-rata Arus Kas Operasi",
        f"Rp {rata_ako / 1_000_000_000:.2f} M"
    )

# Baris kedua
col3, col4 = st.columns(2)

with col3:
    st.metric(
        "Rata-rata Laba Periode Berjalan",
        f"Rp {rata_laba / 1_000_000_000:.2f} M"
    )

with col4:
    st.metric(
        "Rata-rata Pertumbuhan Penjualan",
        f"{pertumbuhan_penjualan:.2f}%"
    )

st.divider()

# Grafik historis penjualan neto
# Mengurutkan data berdasarkan tahun dan kuartal
urutan_kuartal = {
    "Q1": 1,
    "Q2": 2,
    "Q3": 3,
    "Q4": 4
}

df["URUTAN_KUARTAL"] = df["PERIODE"].map(urutan_kuartal)

df = df.sort_values(
    ["TAHUN", "URUTAN_KUARTAL"]
)

# Membuat label periode yang unik
df["PERIODE_LABEL"] = (
    df["TAHUN"].astype(str) + " " + df["PERIODE"]
)

# Membuat grafik
fig = px.line(
    df,
    x="PERIODE_LABEL",
    y="PENJUALAN NETO",
    markers=True,
    title="Tren Penjualan Neto per Kuartal"
)

fig.update_layout(
    xaxis_title="Periode",
    yaxis_title="Penjualan Neto (Rp)",
    hovermode="x unified",
    height=450,
    xaxis=dict(
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

fig.update_traces(
    line=dict(width=3),
    marker=dict(size=7)
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# Gambaran umum analisis
st.subheader("Gambaran Umum Analisis")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("### 📈 Peramalan Penjualan Neto")
        st.write(
            "Memperkirakan penjualan neto pada periode "
            "mendatang berdasarkan pola data historis."
        )

with col2:
    with st.container(border=True):
        st.markdown("### 💰 Risiko Arus Kas Operasi")
        st.write(
            "Mengukur potensi risiko arus kas operasi "
            "menggunakan metode Value at Risk (VaR)."
        )

col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.markdown("### 📊 Regresi Linear Berganda")
        st.write(
            "Menganalisis hubungan beban pokok penjualan "
            "dan beban penjualan terhadap laba periode berjalan."
        )

with col4:
    with st.container(border=True):
        st.markdown("### 🔍 Principal Component Analysis")
        st.write(
            "Mengidentifikasi komponen utama dari "
            "tujuh variabel keuangan perusahaan."
        )