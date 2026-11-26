
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import load_data

st.title("Analisis Risiko Arus Kas Operasi")

# ==========================================
# 1. MEMUAT DAN MENYIAPKAN DATA
# ==========================================

df = load_data()

urutan_kuartal = {
    "Q1": 1,
    "Q2": 2,
    "Q3": 3,
    "Q4": 4
}

df_ako = df.copy()

df_ako["PERIODE"] = df_ako["PERIODE"].astype(str).str.upper()
df_ako["URUTAN_KUARTAL"] = df_ako["PERIODE"].map(urutan_kuartal)

df_ako["TAHUN"] = pd.to_numeric(
    df_ako["TAHUN"], errors="coerce"
)

df_ako["ARUS KAS OPERASI"] = pd.to_numeric(
    df_ako["ARUS KAS OPERASI"], errors="coerce"
)

df_ako = df_ako.dropna(
    subset=["TAHUN", "URUTAN_KUARTAL", "ARUS KAS OPERASI"]
).copy()

df_ako["TAHUN"] = df_ako["TAHUN"].astype(int)

df_ako = df_ako.sort_values(
    ["TAHUN", "URUTAN_KUARTAL"]
).reset_index(drop=True)

df_ako["PERIODE_LABEL"] = (
    df_ako["TAHUN"].astype(str)
    + " "
    + df_ako["PERIODE"]
)

# ==========================================
# 2. NILAI RISIKO DARI HASIL NOTEBOOK
# ==========================================

var_95 = 682604940823.40
cvar_95 = 777000000000.00

var_99 = 834329303821.98
cvar_99 = 888190000000.00

# ==========================================
# 3. MENGHITUNG PERUBAHAN DAN KERUGIAN AKO
# ==========================================

df_ako["PERUBAHAN_AKO"] = (
    df_ako["ARUS KAS OPERASI"].diff()
)

df_risk = df_ako.dropna(
    subset=["PERUBAHAN_AKO"]
).copy()

# Kerugian merupakan negatif dari perubahan AKO
df_risk["KERUGIAN_AKO"] = (
    -df_risk["PERUBAHAN_AKO"]
)

loss = df_risk["KERUGIAN_AKO"]

# Periode dengan penurunan AKO terbesar
idx_penurunan_terbesar = loss.idxmax()

periode_penurunan_terbesar = df_risk.loc[
    idx_penurunan_terbesar, "PERIODE_LABEL"
]

nilai_penurunan_terbesar = loss.loc[
    idx_penurunan_terbesar
]

# ==========================================
# 4. PENJELASAN HALAMAN
# ==========================================

st.write(
    """
    Halaman ini menyajikan analisis risiko perubahan
    arus kas operasi PT Enseval Putera Megatrading Tbk
    menggunakan metode Value at Risk (VaR) dan
    Conditional Value at Risk (CVaR) dengan pendekatan
    Simulasi Historis.
    """
)

st.divider()

# ==========================================
# 5. RINGKASAN RISIKO
# ==========================================

st.subheader("Ringkasan Risiko")

col1, col2 = st.columns(2)

with col1:
    st.metric("VaR 95%", "Rp682,60 M")

with col2:
    st.metric("CVaR 95%", "Rp777,00 M")

col3, col4 = st.columns(2)

with col3:
    st.metric("VaR 99%", "Rp834,33 M")

with col4:
    st.metric("CVaR 99%", "Rp888,19 M")

st.caption(
    "Seluruh nilai risiko dinyatakan dalam miliar rupiah."
)

# ==========================================
# 6. PERGERAKAN ARUS KAS OPERASI
# ==========================================

st.divider()

st.subheader("Pergerakan Arus Kas Operasi")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df_ako["PERIODE_LABEL"],
        y=df_ako["ARUS KAS OPERASI"] / 1e9,
        mode="lines+markers",
        name="Arus Kas Operasi"
    )
)

fig.update_layout(
    title="Perkembangan Arus Kas Operasi per Kuartal",
    xaxis_title="Periode",
    yaxis_title="Arus Kas Operasi (Miliar Rp)",
    hovermode="x unified",
    height=450,
    xaxis=dict(
        type="category",
        tickangle=-45,
        automargin=True
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# 7. DISTRIBUSI KERUGIAN DAN NILAI VAR
# ==========================================

st.divider()

st.subheader("Distribusi Kerugian Arus Kas Operasi")

fig_var = go.Figure()

fig_var.add_trace(
    go.Histogram(
        x=loss / 1e9,
        nbinsx=12,
        name="Distribusi Kerugian",
        opacity=0.75
    )
)

fig_var.add_vline(
    x=var_95 / 1e9,
    line_dash="dash",
    line_color="orange",
    annotation_text="VaR 95%",
    annotation_position="top"
)

fig_var.add_vline(
    x=var_99 / 1e9,
    line_dash="dash",
    line_color="red",
    annotation_text="VaR 99%",
    annotation_position="top left"
)

fig_var.update_layout(
    title="Distribusi Kerugian AKO dan Ambang VaR",
    xaxis_title="Kerugian AKO (Miliar Rp)",
    yaxis_title="Frekuensi",
    height=450,
    bargap=0.08
)

st.plotly_chart(
    fig_var,
    use_container_width=True
)

st.caption(
    "Kerugian dihitung sebagai negatif dari perubahan AKO. "
    "Nilai positif menunjukkan penurunan AKO, sedangkan "
    "nilai negatif menunjukkan kenaikan AKO."
)

# ==========================================
# 8. TABEL HASIL VAR DAN CVAR
# ==========================================

st.divider()

st.subheader("Hasil Perhitungan VaR dan CVaR")

df_hasil_var = pd.DataFrame({
    "Tingkat Kepercayaan": ["95%", "99%"],
    "VaR (Miliar Rp)": [
        var_95 / 1e9,
        var_99 / 1e9
    ],
    "CVaR (Miliar Rp)": [
        cvar_95 / 1e9,
        cvar_99 / 1e9
    ]
})

st.dataframe(
    df_hasil_var.style.format({
        "VaR (Miliar Rp)": "{:.2f}",
        "CVaR (Miliar Rp)": "{:.2f}"
    }),
    use_container_width=True,
    hide_index=True
)

st.caption(
    f"Perhitungan menggunakan Simulasi Historis "
    f"dengan {len(df_risk)} observasi perubahan AKO."
)

if len(df_risk) != 43:
    st.warning(
        "Jumlah observasi perubahan AKO berbeda dari "
        "43 observasi pada hasil analisis notebook. "
        "Periksa kembali rentang data yang digunakan."
    )

# ==========================================
# 9. INTERPRETASI RISIKO
# ==========================================

st.divider()

st.subheader("Interpretasi Risiko")

st.markdown(
    f"""
    **1. Risiko pada tingkat kepercayaan 95%**

    VaR 95% sebesar Rp682,60 miliar menunjukkan ambang
    kerugian berdasarkan distribusi historis. Dalam
    interpretasi probabilistiknya, terdapat sekitar 5%
    kemungkinan kerugian melampaui nilai tersebut,
    berdasarkan asumsi dan data historis yang digunakan.

    **2. Potensi kerugian pada kondisi ekstrem**

    CVaR 95% sebesar Rp777,00 miliar menggambarkan
    rata-rata kerugian pada kelompok kondisi yang
    melampaui ambang VaR 95%. Nilai ini memberikan
    gambaran tingkat kerugian pada bagian ekor distribusi.

    **3. Risiko pada tingkat kepercayaan 99%**

    VaR 99% sebesar Rp834,33 miliar menunjukkan ambang
    kerugian yang lebih tinggi dibandingkan VaR 95%.
    Hal ini menunjukkan bahwa pengukuran pada tingkat
    kepercayaan 99% berfokus pada kondisi kerugian yang
    lebih ekstrem.

    CVaR 99% sebesar Rp888,19 miliar menunjukkan
    rata-rata kerugian pada kelompok kondisi yang
    melampaui ambang VaR 99%.

    **4. Periode penurunan AKO terbesar**

    Penurunan AKO terbesar dalam data terjadi pada
    periode **{periode_penurunan_terbesar}**, dengan
    besaran penurunan sekitar **Rp{nilai_penurunan_terbesar / 1e9:,.2f} miliar**.
    Periode tersebut merupakan observasi dengan kerugian
    historis terbesar dalam perhitungan perubahan AKO.
    """
)

st.info(
    "VaR dan CVaR merupakan estimasi risiko berdasarkan "
    "distribusi kerugian historis, bukan batas maksimum "
    "kerugian yang pasti terjadi pada masa mendatang. "
    "Estimasi pada tingkat kepercayaan 99% perlu "
    "diinterpretasikan secara hati-hati karena jumlah "
    "observasi pada bagian ekor distribusi relatif sedikit."
)
