
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ==================================================
# 1. JUDUL DAN PENJELASAN
# ==================================================

st.title("Principal Component Analysis (PCA)")

st.write(
    """
    Analisis PCA digunakan untuk merangkum pola perubahan
    indikator keuangan PT Enseval Putera Megatrading Tbk
    ke dalam sejumlah komponen utama yang lebih ringkas.

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

st.subheader("Kelayakan Data untuk PCA")

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
    """
    Nilai KMO sebesar 0,629 menunjukkan kecukupan data
    yang tergolong cukup untuk analisis PCA.

    Bartlett's Test menghasilkan p-value sebesar
    1,07 × 10⁻²⁴, lebih kecil dari 0,05. Hasil ini
    menunjukkan bahwa matriks korelasi berbeda secara
    signifikan dari matriks identitas, sehingga terdapat
    korelasi antarvariabel yang mendukung penerapan PCA.
    """
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
    """
    Laba Periode Berjalan dikeluarkan karena nilai MSA
    sebesar 0,111 berada di bawah batas 0,50.
    Enam variabel lainnya digunakan dalam pembentukan
    komponen utama.
    """
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
    """
    PC1 menjelaskan 46,03% variasi data, PC2 sebesar
    19,11%, dan PC3 sebesar 15,46%.

    Secara kumulatif, ketiga komponen menjelaskan
    80,60% variasi dari enam variabel keuangan yang
    dianalisis.
    """
)

st.divider()


# ==================================================
# 4. EIGENVALUE DAN SCREE PLOT
# ==================================================

st.subheader("Pembentukan Komponen Utama")

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
    go.Scatter(
        x=df_eigen["Komponen"],
        y=df_eigen["Eigenvalue"],
        mode="lines+markers",
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

st.markdown("**Dasar Pemilihan Jumlah Komponen**")

st.write(
    """
    Jumlah komponen ditentukan dengan mempertimbangkan
    dua kriteria berikut:
    """
)

st.markdown(
    """
    - **Kriteria Kaiser:** mempertahankan komponen dengan
      eigenvalue lebih dari 1. Berdasarkan kriteria ini,
      terdapat dua komponen, yaitu PC1 dan PC2.
    - **Varians kumulatif:** mempertimbangkan kemampuan
      komponen dalam menjelaskan variasi data. Dua komponen
      menjelaskan 65,14%, sedangkan tiga komponen menjelaskan
      80,60%.
    """
)

st.info(
    """
    Penelitian ini mempertahankan tiga komponen utama
    karena varians kumulatifnya mencapai 80,60%,
    sesuai target minimal 80% yang digunakan dalam analisis.

    Dengan demikian, pemilihan tiga komponen merupakan
    keputusan berdasarkan pertimbangan varians kumulatif,
    meskipun kriteria Kaiser menyarankan dua komponen.
    """
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
    """
    Loading menunjukkan kontribusi hubungan masing-masing
    variabel terhadap komponen utama. Nilai absolut loading
    sebesar 0,50 atau lebih digunakan sebagai acuan untuk
    mengidentifikasi variabel yang paling mencirikan komponen.
    """
)

st.markdown("**Visualisasi Loading PCA**")

fig_loading = go.Figure(
    data=go.Heatmap(
        z=df_loading[["PC1", "PC2", "PC3"]].values,
        x=["PC1", "PC2", "PC3"],
        y=df_loading["Variabel"],
        text=df_loading[["PC1", "PC2", "PC3"]].values,
        texttemplate="%{text:.3f}",
        zmin=-1,
        zmax=1,
        colorscale="RdBu",
        colorbar=dict(title="Loading")
    )
)

fig_loading.update_layout(
    title="Heatmap Loading Variabel pada Komponen Utama",
    xaxis_title="Komponen Utama",
    yaxis_title="Variabel Keuangan",
    height=430
)

st.plotly_chart(
    fig_loading,
    use_container_width=True
)

st.caption(
    """
    Warna menunjukkan arah dan besar loading. Nilai positif
    dan negatif menggambarkan arah hubungan relatif variabel
    terhadap komponen yang bersangkutan.
    """
)

st.divider()


# ==================================================
# 6. INTERPRETASI KOMPONEN UTAMA
# ==================================================

st.subheader("Interpretasi Komponen Utama")

with st.expander(
    "1. PC1 – Aktivitas Penjualan dan Operasional",
    expanded=True
):
    st.metric("Varians yang Dijelaskan", "46,03%")

    st.write(
        """
        PC1 terutama dicirikan oleh:

        - Penjualan Neto: 0,946
        - Beban Pokok Penjualan: 0,934
        - Persediaan: 0,607
        - Beban Penjualan: 0,578

        Keempat variabel memiliki loading positif.
        Hal ini menunjukkan bahwa PC1 merangkum pola
        perubahan bersama indikator penjualan dan
        aktivitas operasional perusahaan.
        """
    )

with st.expander(
    "2. PC2 – Pola Piutang dan Persediaan"
):
    st.metric("Varians yang Dijelaskan", "19,11%")

    st.write(
        """
        PC2 terutama dicirikan oleh:

        - Piutang Usaha: 0,799
        - Persediaan: -0,584

        Piutang Usaha memiliki loading positif,
        sedangkan Persediaan memiliki loading negatif.
        Hal ini menunjukkan arah loading yang berlawanan
        pada komponen kedua.
        """
    )

with st.expander(
    "3. PC3 – Pola Total Aset dan Beban Penjualan"
):
    st.metric("Varians yang Dijelaskan", "15,46%")

    st.write(
        """
        PC3 terutama dicirikan oleh:

        - Total Aset: 0,789
        - Beban Penjualan: -0,524

        Total Aset memiliki loading positif,
        sedangkan Beban Penjualan memiliki loading negatif.
        Komponen ketiga merangkum pola perubahan relatif
        kedua indikator tersebut.
        """
    )

st.caption(
    """
    Penamaan komponen merupakan interpretasi berdasarkan
    variabel dengan loading yang relatif besar. Tanda positif
    atau negatif pada komponen bersifat relatif dan tidak
    menunjukkan hubungan sebab-akibat.
    """
)

st.divider()


# ==================================================
# 7. KESIMPULAN PCA
# ==================================================

st.subheader("Kesimpulan Analisis PCA")

st.markdown(
    """
    Berdasarkan hasil Principal Component Analysis,
    enam variabel keuangan yang telah melalui proses
    seleksi berhasil dirangkum menjadi tiga komponen utama.

    Ketiga komponen tersebut menjelaskan 80,60% variasi
    data. PC1 menggambarkan pola aktivitas penjualan dan
    operasional, PC2 menggambarkan pola piutang dan
    persediaan, sedangkan PC3 menggambarkan pola total
    aset dan beban penjualan.

    Hasil ini menunjukkan bahwa PCA dapat menyederhanakan
    enam indikator keuangan menjadi tiga dimensi utama
    tanpa kehilangan sebagian besar informasi variasi data.
    """
)

st.warning(
    """
    PCA digunakan untuk merangkum pola variasi antarindikator
    keuangan. Hasilnya tidak dapat langsung digunakan untuk
    menyimpulkan hubungan sebab-akibat atau menentukan
    variabel yang memengaruhi laba maupun arus kas.
    """
)
