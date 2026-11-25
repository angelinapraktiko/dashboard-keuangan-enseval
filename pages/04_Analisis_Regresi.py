import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import load_data

#  ==================================================
# HASIL REGRESI LINEAR BERGANDA
# ==================================================

st.subheader("Hasil Regresi Linear Berganda")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Jumlah Observasi", "44 Kuartal")

with col2:
    st.metric("R-squared", "29,56%")

with col3:
    st.metric("Adjusted R-squared", "26,12%")


# Tabel koefisien

st.markdown("**Hasil Koefisien Regresi**")

df_koefisien = pd.DataFrame({
    "Variabel": [
        "Beban Pokok Penjualan",
        "Beban Penjualan"
    ],
    "Koefisien": [
        0.0621,
        -0.8158
    ],
    "P-value HAC": [
        0.0038,
        0.0522
    ],
    "Kesimpulan": [
        "Positif dan signifikan",
        "Negatif, tidak signifikan"
    ]
})

st.dataframe(
    df_koefisien,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Pengujian koefisien menggunakan standard error "
    "HAC Newey-West dengan 4 lag dan tingkat signifikansi 5%."
)


# Interpretasi koefisien

st.markdown("**Interpretasi Hasil Koefisien**")

st.markdown(
    """
    **1. Beban Pokok Penjualan**

    Memiliki koefisien positif sebesar 0,0621 dengan
    p-value 0,0038. Artinya, setiap kenaikan Beban Pokok
    Penjualan sebesar Rp1, dengan Beban Penjualan tetap,
    berkaitan dengan peningkatan nilai prediksi Laba
    Periode Berjalan sebesar Rp0,0621.

    Hubungan tersebut signifikan secara statistik pada
    tingkat signifikansi 5%.

    **2. Beban Penjualan**

    Memiliki koefisien negatif sebesar -0,8158 dengan
    p-value 0,0522. Artinya, setiap kenaikan Beban Penjualan
    sebesar Rp1, dengan Beban Pokok Penjualan tetap,
    berkaitan dengan penurunan nilai prediksi Laba
    Periode Berjalan sebesar Rp0,8158.

    Namun, hubungan tersebut belum signifikan secara
    statistik pada tingkat signifikansi 5%.
    """
)

st.divider()


# Uji signifikansi simultan

st.markdown("**Signifikansi Model Secara Simultan**")

col1, col2 = st.columns(2)

with col1:
    st.metric("F-statistic", "8,602")

with col2:
    st.metric("Prob (F-statistic)", "0,000759")

st.info(
    "Nilai Prob (F-statistic) sebesar 0,000759 lebih kecil "
    "dari 0,05. Hal ini menunjukkan bahwa Beban Pokok "
    "Penjualan dan Beban Penjualan secara bersama-sama "
    "memiliki hubungan yang signifikan secara statistik "
    "dengan Laba Periode Berjalan."
)

st.divider()


# Kesimpulan analisis

st.subheader("Kesimpulan Analisis")

st.markdown(
    """
    Berdasarkan hasil regresi, Beban Pokok Penjualan
    menunjukkan hubungan positif dan signifikan dengan
    Laba Periode Berjalan. Sementara itu, Beban Penjualan
    menunjukkan hubungan negatif, tetapi belum signifikan
    secara statistik pada tingkat signifikansi 5%.

    Model mampu menjelaskan 29,56% variasi Laba Periode
    Berjalan, sedangkan 70,44% lainnya berkaitan dengan
    faktor-faktor di luar model.
    """
)

st.warning(
    "Hasil regresi menggambarkan hubungan statistik, bukan "
    "hubungan sebab-akibat. Interpretasi koefisien juga "
    "mempertimbangkan bahwa kedua variabel beban merupakan "
    "komponen dalam perhitungan laba."
)
