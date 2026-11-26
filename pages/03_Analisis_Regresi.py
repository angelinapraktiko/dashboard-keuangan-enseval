
import streamlit as st
import pandas as pd

st.title("Analisis Regresi Linear Berganda")

st.write(
    """
    Analisis regresi linear berganda digunakan untuk mengidentifikasi
    hubungan antara Beban Pokok Penjualan dan Beban Penjualan
    dengan Laba Periode Berjalan PT Enseval Putera Megatrading Tbk.
    """
)

# ==================================================
# 1. RINGKASAN MODEL
# ==================================================

st.subheader("Ringkasan Hasil Regresi")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Jumlah Observasi", "44 Kuartal")

with col2:
    st.metric("R-squared", "29,56%")

with col3:
    st.metric("Adjusted R-squared", "26,12%")

st.markdown("**Persamaan Regresi**")

st.latex(
    r"\hat{Y} = 147559522386.82"
    r" + 0.0621X_1 - 0.8158X_2"
)

st.caption(
    """
    Y = Laba Periode Berjalan;
    X₁ = Beban Pokok Penjualan;
    X₂ = Beban Penjualan.
    """
)

st.divider()



# ==================================================
# 3. INTERPRETASI KOEFISIEN
# ==================================================

st.subheader("Interpretasi Koefisien")

with st.expander("1. Konstanta", expanded=True):
    st.write(
        """
        Konstanta sebesar Rp147,56 miliar menunjukkan nilai
        prediksi Laba Periode Berjalan ketika Beban Pokok
        Penjualan dan Beban Penjualan bernilai nol.

        Interpretasi tersebut merupakan bagian matematis
        dari model dan belum tentu menggambarkan kondisi
        operasional perusahaan yang realistis.
        """
    )

with st.expander("2. Beban Pokok Penjualan"):
    st.write(
        """
        Koefisien sebesar 0,0621 dengan p-value HAC 0,0038.

        Artinya, dengan Beban Penjualan dianggap tetap,
        kenaikan Beban Pokok Penjualan sebesar Rp1 berkaitan
        dengan kenaikan nilai prediksi Laba Periode Berjalan
        sebesar Rp0,0621.

        Karena p-value 0,0038 lebih kecil dari 0,05,
        hubungan tersebut signifikan secara statistik
        pada tingkat signifikansi 5%.
        """
    )

with st.expander("3. Beban Penjualan"):
    st.write(
        """
        Koefisien sebesar -0,8158 dengan p-value HAC 0,0522.

        Artinya, dengan Beban Pokok Penjualan dianggap tetap,
        kenaikan Beban Penjualan sebesar Rp1 berkaitan
        dengan penurunan nilai prediksi Laba Periode Berjalan
        sebesar Rp0,8158.

        Namun, p-value 0,0522 lebih besar dari 0,05.
        Dengan demikian, hubungan tersebut belum signifikan
        secara statistik pada tingkat signifikansi 5%.
        """
    )

st.divider()

# ==================================================
# 4. PENGUJIAN SIGNIFIKANSI MODEL
# ==================================================

st.subheader("Pengujian Signifikansi Model")

col1, col2 = st.columns(2)

with col1:
    st.metric("F-statistic OLS", "8,602")

with col2:
    st.metric("Prob (F-statistic)", "0,000759")

st.info(
    """
    Berdasarkan uji F OLS konvensional, nilai Prob (F-statistic)
    sebesar 0,000759 lebih kecil dari 0,05.

    Hasil tersebut menunjukkan bahwa kedua variabel independen
    secara bersama-sama signifikan dalam model OLS konvensional.

    Catatan: pengujian ini menggunakan kovarians OLS konvensional,
    bukan uji simultan yang telah dikoreksi menggunakan HAC
    Newey-West.
    """
)

st.divider()

# ==================================================
# 5. PENGUJIAN DIAGNOSTIK
# ==================================================

st.subheader("Ringkasan Pengujian Diagnostik")

df_diagnostik = pd.DataFrame({
    "Pengujian": [
        "Variance Inflation Factor (VIF)",
        "Breusch-Pagan",
        "Breusch-Godfrey (Lag 4)",
        "Durbin-Watson",
        "Jarque-Bera"
    ],
    "Hasil": [
        "8,8211",
        "0,5592",
        "0,0089",
        "2,6556",
        "0,9965"
    ],
    "Keterangan": [
        "Indikasi multikolinearitas cukup tinggi",
        "Tidak ditemukan bukti cukup adanya heteroskedastisitas",
        "Terdapat indikasi autokorelasi residual",
        "Statistik pendukung pemeriksaan autokorelasi",
        "Tidak ditemukan bukti cukup adanya penyimpangan normalitas"
    ]
})

st.dataframe(
    df_diagnostik,
    use_container_width=True,
    hide_index=True
)

st.markdown("**Interpretasi Pengujian Diagnostik**")

st.warning(
    """
    Uji Breusch-Godfrey menghasilkan p-value 0,0089,
    lebih kecil dari 0,05. Hasil ini menunjukkan adanya
    indikasi autokorelasi pada residual hingga lag yang diuji.
    """
)

st.write(
    """
    Sementara itu, uji Breusch-Pagan menghasilkan p-value
    0,5592, sehingga tidak ditemukan bukti yang cukup
    mengenai heteroskedastisitas pada tingkat signifikansi 5%.

    Nilai VIF sebesar 8,8211 menunjukkan adanya indikasi
    multikolinearitas yang perlu diperhatikan dalam
    interpretasi koefisien.
    """
)

st.info(
    """
    Untuk mengakomodasi kemungkinan heteroskedastisitas
    dan autokorelasi, pengujian signifikansi koefisien
    menggunakan standard error HAC Newey-West dengan
    4 lag. Koreksi HAC tidak menghilangkan autokorelasi
    dari residual, tetapi membuat inferensi koefisien
    lebih robust terhadap kedua kondisi tersebut.
    """
)

st.divider()


# ==================================================
# 2. HASIL KOEFISIEN REGRESI
# ==================================================

st.subheader("Hasil Koefisien Regresi")

df_koefisien = pd.DataFrame({
    "Variabel": [
        "Konstanta",
        "Beban Pokok Penjualan",
        "Beban Penjualan"
    ],
    "Koefisien": [
        147559522386.8206,
        0.0621,
        -0.8158
    ],
    "Standard Error HAC": [
        51255175252.2465,
        0.0203,
        0.4080
    ],
    "P-value HAC": [
        0.0063,
        0.0038,
        0.0522
    ],
    "Kesimpulan": [
        "Signifikan",
        "Positif dan signifikan",
        "Negatif, belum signifikan"
    ]
})

st.dataframe(
    df_koefisien,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Koefisien": st.column_config.NumberColumn(
            "Koefisien",
            format="localized"
        ),
        "Standard Error HAC": st.column_config.NumberColumn(
            "Standard Error HAC",
            format="%.4f"
        ),
        "P-value HAC": st.column_config.NumberColumn(
            "P-value HAC",
            format="%.4f"
        )
    }
)

st.caption(
    """
    Standard error dan p-value menggunakan koreksi HAC
    Newey-West dengan 4 lag. Pengujian menggunakan
    tingkat signifikansi 5% (α = 0,05).
    """
)

st.divider()


# ==================================================
# 6. KESIMPULAN
# ==================================================

st.subheader("Kesimpulan Analisis")

st.markdown(
    """
    Berdasarkan hasil regresi linear berganda, Beban Pokok
    Penjualan memiliki hubungan positif dan signifikan
    dengan Laba Periode Berjalan. Sebaliknya, Beban Penjualan
    memiliki hubungan negatif, tetapi belum signifikan secara
    statistik pada tingkat signifikansi 5%, berdasarkan
    pengujian HAC Newey-West.

    Model menghasilkan nilai R-squared sebesar 29,56%.
    Artinya, kedua variabel independen dalam model mampu
    menjelaskan 29,56% variasi Laba Periode Berjalan pada
    data pengamatan. Sementara itu, 70,44% variasi lainnya
    belum dapat dijelaskan oleh model.
    """
)

st.caption(
    """
    Hasil regresi menggambarkan hubungan statistik antarvariabel,
    bukan bukti hubungan sebab-akibat. Interpretasi koefisien
    juga perlu mempertimbangkan bahwa kedua variabel beban
    merupakan komponen dalam perhitungan laba.
    """
)
