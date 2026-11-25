
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import load_data


# ==================================================
# 1. JUDUL DAN PENJELASAN
# ==================================================

st.title("Principal Component Analysis (PCA)")

df = load_data()

st.write(
    """
    Halaman ini menyajikan analisis komponen utama
    untuk merangkum pola perubahan indikator keuangan
    PT Enseval Putera Megatrading Tbk.

    Analisis menggunakan transformasi pertumbuhan tahunan
    (YoY log) terhadap enam variabel keuangan terpilih.
    """
)

st.caption(
    "Data awal terdiri dari 44 kuartal. Setelah transformasi "
    "YoY log, diperoleh 40 pengamatan."
)

st.divider()


# ==================================================
# 2. KELAYAKAN DATA
# ==================================================

st.subheader("Kelayakan Data")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Kaiser-Meyer-Olkin (KMO)",
        "0,629"
    )

with col2:
    st.metric(
        "Bartlett's Test",
        "p-value < 0,001"
    )

st.info(
    "Nilai KMO sebesar 0,629 menunjukkan kecukupan data "
    "yang tergolong cukup untuk analisis PCA. Bartlett's "
    "Test menghasilkan p-value sebesar 1,07 × 10⁻²⁴, "
    "yang menunjukkan adanya korelasi antarvariabel."
)

st.markdown("**Pemilihan Variabel**")

df_variabel = pd.DataFrame({
    "Keterangan": [
        "Variabel kandidat awal",
        "Variabel dikeluarkan",
        "Variabel yang digunakan"
    ],
    "Jumlah": [
        7,
        1,
        6
    ],
    "Detail": [
        "Seluruh indikator keuangan kandidat",
        "Laba Periode Berjalan (MSA 0,111)",
        "Penjualan, beban, persediaan, piutang, dan aset"
    ]
})

st.dataframe(
    df_variabel,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Laba Periode Berjalan dikeluarkan karena nilai MSA "
    "sebesar 0,111 berada di bawah batas minimum 0,50."
)

st.divider()


# ==================================================
# 3. VARIANS YANG DIJELASKAN
# ==================================================

st.subheader("Varians yang Dijelaskan")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("PC1", "46,03%")

with col2:
    st.metric("PC2", "19,11%")

with col3:
    st.metric("PC3", "15,46%")

st.metric(
    "Varians Kumulatif Tiga Komponen",
    "80,60%"
)

df_varians = pd.DataFrame({
    "Komponen": ["PC1", "PC2", "PC3"],
    "Varians": [46.028, 19.110, 15.464],
    "Kumulatif": [46.028, 65.138, 80.603]
})

fig_varians = go.Figure()

fig_varians.add_trace(
    go.Bar(
        x=df_varians["Komponen"],
        y=df_varians["Varians"],
        text=df_varians["Varians"].apply(
            lambda x: f"{x:.2f}%"
        ),
        textposition="outside",
        name="Varians"
    )
)

fig_varians.update_layout(
    title="Proporsi Varians Setiap Komponen Utama",
    xaxis_title="Komponen Utama",
    yaxis_title="Varians (%)",
    yaxis=dict(range=[0, 55]),
    height=400,
    showlegend=False
)

st.plotly_chart(
    fig_varians,
    use_container_width=True
)

st.info(
    "PC1 menjelaskan 46,03% variasi data, PC2 sebesar "
    "19,11%, dan PC3 sebesar 15,46%. Ketiga komponen "
    "secara kumulatif menjelaskan 80,60% variasi dari "
    "enam variabel keuangan yang dianalisis."
)

st.divider()


# ==================================================
# 4. EIGENVALUE DAN SCREE PLOT
# ==================================================

st.subheader("Hasil Pembentukan Komponen")

st.markdown("**Tabel Eigenvalue**")

df_eigen = pd.DataFrame({
    "Komponen": [
        "PC1", "PC2", "PC3",
        "PC4", "PC5", "PC6"
    ],
    "Eigenvalue": [
        2.762, 1.147, 0.928,
        0.651, 0.497, 0.016
    ],
    "Varians (%)": [
        46.028, 19.110, 15.464,
        10.845, 8.288, 0.264
    ],
    "Kumulatif (%)": [
        46.028, 65.138, 80.603,
        91.448, 99.736, 100.000
    ]
})

st.dataframe(
    df_eigen,
    use_container_width=True,
    hide_index=True
)

st.markdown("**Scree Plot**")

fig_scree = go.Figure()

fig_scree.add_trace(
    go.Bar(
        x=df_eigen["Komponen"],
        y=df_eigen["Eigenvalue"],
        name="Eigenvalue"
    )
)

fig_scree.add_hline(
    y=1,
    line_dash="dash",
    annotation_text="Batas Eigenvalue = 1"
)

fig_scree.update_layout(
    title="Scree Plot Eigenvalue",
    xaxis_title="Komponen Utama",
    yaxis_title="Eigenvalue",
    height=400
)

st.plotly_chart(
    fig_scree,
    use_container_width=True
)

st.info(
    "Kriteria Kaiser menyarankan dua komponen karena "
    "memiliki eigenvalue lebih dari 1. Namun, penelitian "
    "ini menggunakan tiga komponen karena dua komponen "
    "hanya menjelaskan 65,14% variasi, sedangkan tiga "
    "komponen mencapai 80,60% sesuai target minimal 80%."
)

st.divider()


# ==================================================
# 5. LOADING VARIABEL
# ==================================================

st.subheader("Loading Variabel terhadap Komponen Utama")

df_loading = pd.DataFrame({
    "Variabel": [
        "Penjualan Neto",
        "Beban Pokok Penjualan",
        "Beban Penjualan",
        "Persediaan",
        "Piutang Usaha",
        "Total Aset"
    ],
    "PC1": [
        0.946, 0.934, 0.578,
        0.607, 0.378, 0.389
    ],
    "PC2": [
        -0.063, -0.131, 0.179,
        -0.584, 0.799, 0.337
    ],
    "PC3": [
        -0.027, 0.007, -0.524,
        0.110, -0.136, 0.789
    ]
})

st.dataframe(
    df_loading,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Loading menunjukkan kekuatan dan arah hubungan "
    "variabel dengan komponen utama. Nilai absolut loading "
    "minimal 0,50 digunakan sebagai acuan penciri utama."
)

st.divider()


# ==================================================
# 6. INTERPRETASI KOMPONEN UTAMA
# ==================================================

st.subheader("Interpretasi Komponen Utama")

st.markdown(
    """
    **1. PC1 – Dimensi Aktivitas Penjualan dan Operasional**

    PC1 menjelaskan 46,03% variasi data. Komponen ini
    terutama dicirikan oleh Penjualan Neto (0,946),
    Beban Pokok Penjualan (0,934), Persediaan (0,607),
    dan Beban Penjualan (0,578).

    Hasil tersebut menunjukkan bahwa PC1 merangkum
    pola perubahan indikator aktivitas penjualan
    dan operasional perusahaan.

    **2. PC2 – Dimensi Pola Piutang dan Persediaan**

    PC2 menjelaskan 19,11% variasi data. Komponen ini
    dicirikan oleh Piutang Usaha (0,799) dengan arah
    positif dan Persediaan (-0,584) dengan arah negatif.

    Hal ini menggambarkan pola perubahan piutang usaha
    dan persediaan yang berlawanan arah terhadap
    komponen tersebut.

    **3. PC3 – Dimensi Total Aset dan Beban Penjualan**

    PC3 menjelaskan 15,46% variasi data. Komponen ini
    dicirikan oleh Total Aset (0,789) dengan arah positif
    dan Beban Penjualan (-0,524) dengan arah negatif.

    Hal ini menunjukkan bahwa PC3 merangkum pola
    perubahan total aset dan beban penjualan yang
    berlawanan arah terhadap komponen tersebut.
    """
)

st.divider()


# ==================================================
# 7. KESIMPULAN PCA
# ==================================================

st.subheader("Kesimpulan Analisis PCA")

st.markdown(
    """
    Berdasarkan hasil PCA, enam variabel keuangan
    berhasil dirangkum menjadi tiga komponen utama.
    Ketiga komponen tersebut menjelaskan 80,60% variasi
    data, sehingga memenuhi target varians kumulatif
    minimal 80%.

    PC1 menggambarkan aktivitas penjualan dan operasional,
    PC2 menggambarkan pola piutang dan persediaan,
    sedangkan PC3 menggambarkan total aset dan
    beban penjualan.
    """
)

st.warning(
    "PCA digunakan untuk merangkum pola perubahan "
    "indikator keuangan, bukan untuk menyimpulkan "
    "hubungan sebab-akibat atau menentukan variabel "
    "yang secara langsung memengaruhi laba maupun arus kas."
)
