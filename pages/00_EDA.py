
import streamlit as st
import pandas as pd
from utils import load_data

st.title("Exploratory Data Analysis (EDA)")

st.write(
    """
    Halaman ini menyajikan eksplorasi awal terhadap data
    keuangan kuartalan PT Enseval Putera Megatrading Tbk.
    Eksplorasi dilakukan untuk memahami struktur,
    karakteristik, dan kualitas data sebelum analisis lanjutan.
    """
)

df = load_data()

# ==========================================
# 1. MENYIAPKAN DATA
# ==========================================

urutan_kuartal = {
    "Q1": 1,
    "Q2": 2,
    "Q3": 3,
    "Q4": 4
}

df["PERIODE"] = (
    df["PERIODE"].astype(str).str.strip().str.upper()
)

df["TAHUN"] = pd.to_numeric(
    df["TAHUN"], errors="coerce"
)

df["URUTAN_KUARTAL"] = df["PERIODE"].map(
    urutan_kuartal
)

df = df.sort_values(
    ["TAHUN", "URUTAN_KUARTAL"]
).reset_index(drop=True)

# ==========================================
# 2. INFORMASI DATASET
# ==========================================

st.divider()
st.subheader("Informasi Dataset")

jumlah_baris = len(df)
jumlah_kolom = len(df.columns) - 1  # Tidak menghitung kolom bantuan URUTAN_KUARTAL

periode_awal = (
    str(int(df["TAHUN"].min()))
    + " "
    + df.loc[df["TAHUN"].idxmin(), "PERIODE"]
)

periode_akhir = (
    str(int(df["TAHUN"].max()))
    + " "
    + df.loc[df["TAHUN"].idxmax(), "PERIODE"]
)

# Baris pertama: jumlah observasi dan kolom
col1, col2 = st.columns(2)

with col1:
    st.metric("Jumlah Observasi", jumlah_baris)

with col2:
    st.metric("Jumlah Kolom", jumlah_kolom)

# Baris kedua: rentang periode menggunakan lebar penuh
st.markdown("**Rentang Periode**")
st.write(f"{periode_awal} – {periode_akhir}")

st.caption(
    "Satu observasi merepresentasikan satu periode kuartalan."
)


# ==========================================
# 3. STRUKTUR DATASET
# ==========================================

st.divider()
st.subheader("Struktur Dataset")

df_info = pd.DataFrame({
    "Nama Kolom": df.columns,
    "Tipe Data": [
        str(df[kolom].dtype) for kolom in df.columns
    ],
    "Jumlah Data Terisi": [
        df[kolom].notna().sum() for kolom in df.columns
    ],
    "Missing Value": [
        df[kolom].isna().sum() for kolom in df.columns
    ]
})

st.dataframe(
    df_info,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# 4. PEMERIKSAAN KUALITAS DATA
# ==========================================

st.divider()
st.subheader("Pemeriksaan Kualitas Data")

total_missing = df.isna().sum().sum()
total_duplikat = df.duplicated().sum()

duplikat_periode = df.duplicated(
    subset=["TAHUN", "PERIODE"]
).sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Missing Value", int(total_missing))

with col2:
    st.metric("Baris Duplikat", int(total_duplikat))

with col3:
    st.metric("Periode Duplikat", int(duplikat_periode))

if total_missing == 0 and total_duplikat == 0 and duplikat_periode == 0:
    st.success(
        "Tidak ditemukan missing value maupun data duplikat."
    )
else:
    st.warning(
        "Terdapat data yang perlu diperiksa lebih lanjut."
    )

# ==========================================
# 5. PEMERIKSAAN KELENGKAPAN PERIODE
# ==========================================

st.divider()
st.subheader("Kelengkapan Periode Kuartal")

df_periode = df.groupby(
    "TAHUN"
)["PERIODE"].agg(list).reset_index()

df_periode["Jumlah Kuartal"] = (
    df_periode["PERIODE"].apply(len)
)

df_periode["Kelengkapan"] = (
    df_periode["Jumlah Kuartal"].apply(
        lambda x: "Lengkap" if x == 4 else "Tidak Lengkap"
    )
)

df_periode["Periode Tersedia"] = (
    df_periode["PERIODE"].apply(
        lambda x: ", ".join(x)
    )
)

st.dataframe(
    df_periode[
        ["TAHUN", "Periode Tersedia",
         "Jumlah Kuartal", "Kelengkapan"]
    ],
    use_container_width=True,
    hide_index=True
)

# ==========================================
# 6. DATA AWAL DAN AKHIR
# ==========================================


# ==========================================
# 7. INDIKATOR KEUANGAN
# ==========================================

st.divider()
st.subheader("Indikator Keuangan")

rata_penjualan = df["PENJUALAN NETO"].mean()
rata_ako = df["ARUS KAS OPERASI"].mean()
rata_laba = df["LABA PERIODE BERJALAN"].mean()

pertumbuhan_penjualan = (
    df["PENJUALAN NETO"].pct_change().mean() * 100
)

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


# ==========================================
# 8. GAMBARAN UMUM ANALISIS
# ==========================================

st.divider()
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
            "enam variabel keuangan perusahaan."
        )

