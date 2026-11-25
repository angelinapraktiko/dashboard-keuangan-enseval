import streamlit as st
from utils import load_data

st.set_page_config(
    page_title="Dashboard Keuangan Enseval",
    page_icon="📊",
    layout="wide"
)

st.title("Dashboard Analisis Keuangan")
st.subheader("PT Enseval Putera Megatrading Tbk")

st.markdown("---")

st.write(
    """
    Dashboard ini menyajikan hasil analisis data keuangan
    PT Enseval Putera Megatrading Tbk berdasarkan laporan
    keuangan konsolidasian kuartalan.
    """
)

st.info(
    "Silakan pilih halaman analisis melalui menu navigasi "
    "di sebelah kiri."
)

st.divider()

st.subheader("Pemeriksaan Dataset")

df = load_data()

st.success("Dataset berhasil dibaca!")

st.write("Jumlah baris dan kolom:", df.shape)

st.dataframe(
    df,
    use_container_width=True,
    height=600
)
