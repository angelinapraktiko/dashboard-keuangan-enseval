import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import load_data

st.title("Analisis Risiko Arus Kas Operasi")
df = load_data()


# Mengurutkan data berdasarkan tahun dan kuartal
urutan_kuartal = {
    "Q1": 1,
    "Q2": 2,
    "Q3": 3,
    "Q4": 4
}

df_ako = df.copy()

df_ako["PERIODE"] = df_ako["PERIODE"].astype(str)
df_ako["URUTAN_KUARTAL"] = df_ako["PERIODE"].map(
    urutan_kuartal
)

df_ako = df_ako.sort_values(
    ["TAHUN", "URUTAN_KUARTAL"]
)

df_ako["PERIODE_LABEL"] = (
    df_ako["TAHUN"].astype(str)
    + " "
    + df_ako["PERIODE"]
)

st.write(
    """
    Halaman ini menyajikan analisis risiko arus kas operasi
    PT Enseval Putera Megatrading Tbk menggunakan metode
    Value at Risk (VaR).
    """
)


st.divider()

st.subheader("Ringkasan Risiko")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "VaR 95%",
        "682,60 M"
    )

with col2:
    st.metric(
        "CVaR 95%",
        "777,00 M"
    )

col3, col4 = st.columns(2)

with col3:
    st.metric(
        "VaR 99%",
        "834,33 M"
    )

with col4:
    st.metric(
        "CVaR 99%",
        "888,19 M"
    )

# Grafik pergerakan Arus Kas Operasi
st.divider()

st.subheader("Pergerakan Arus Kas Operasi")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_ako["PERIODE_LABEL"],
    y=df_ako["ARUS KAS OPERASI"],
    mode="lines+markers",
    name="Arus Kas Operasi"
))

fig.update_layout(
    title="Perkembangan Arus Kas Operasi per Kuartal",
    xaxis_title="Periode",
    yaxis_title="Arus Kas Operasi (Rp)",
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


# Menghitung perubahan dan kerugian AKO
df_ako["PERUBAHAN_AKO"] = (
    df_ako["ARUS KAS OPERASI"].diff()
)

df_risk = df_ako.dropna(
    subset=["PERUBAHAN_AKO"]
).copy()

df_risk["KERUGIAN_AKO"] = (
    -df_risk["PERUBAHAN_AKO"]
)

loss = df_risk["KERUGIAN_AKO"]

# Nilai VaR dari hasil notebook
var_95 = 682604940823.40
var_99 = 834329303821.98

# Grafik distribusi kerugian
st.divider()

st.subheader("Distribusi Kerugian Arus Kas Operasi")

fig_var = go.Figure()

fig_var.add_trace(go.Histogram(
    x=loss / 1e9,
    nbinsx=12,
    name="Distribusi Kerugian",
    opacity=0.75
))


fig_var.add_vline(
    x=var_95 / 1e9,
    line_dash="dash",
    line_color="orange"
)

fig_var.add_vline(
    x=var_99 / 1e9,
    line_dash="dash",
    line_color="red"
)

# Label VaR dibuat terpisah
fig_var.add_annotation(
    x=var_95 / 1e9,
    y=1.12,
    yref="paper",
    text="VaR 95%: 682,60 M",
    showarrow=False,
    font=dict(color="orange", size=11),
    xanchor="left"
)

fig_var.add_annotation(
    x=var_99 / 1e9,
    y=1.04,
    yref="paper",
    text="VaR 99%: 834,33 M",
    showarrow=False,
    font=dict(color="red", size=11),
    xanchor="left"
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



st.divider()

st.subheader("Hasil Perhitungan VaR dan CVaR")

df_hasil_var = pd.DataFrame({
    "Tingkat Kepercayaan": ["95%", "99%"],
    "VaR (M)": [682.60, 834.33],
    "CVaR (M)": [777.00, 888.19]
})

st.dataframe(
    df_hasil_var.style.format({
        "VaR (M)": "{:.2f}",
        "CVaR (M)": "{:.2f}"
    }),
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Seluruh nilai dinyatakan dalam miliar rupiah (M). "
    "Perhitungan menggunakan metode Simulasi Historis."
)



st.divider()

st.subheader("Interpretasi Risiko")

st.markdown(
    """
    **1. Risiko pada tingkat kepercayaan 95%**

    Hasil perhitungan menunjukkan VaR 95% sebesar
    Rp682,60 miliar. Berdasarkan distribusi kerugian
    historis, nilai tersebut menjadi ambang kerugian
    AKO pada tingkat kepercayaan 95%.

    **2. Potensi kerugian ketika melewati ambang VaR**

    CVaR 95% sebesar Rp777,00 miliar menunjukkan
    rata-rata kerugian pada kelompok observasi yang
    melampaui ambang VaR 95%. Dengan demikian, CVaR
    memberikan gambaran besarnya kerugian pada kondisi
    yang lebih ekstrem.

    **3. Risiko pada tingkat kepercayaan 99%**

    VaR 99% sebesar Rp834,33 miliar menunjukkan
    ambang kerugian yang lebih tinggi dibandingkan
    VaR 95%. Hal ini menggambarkan bahwa penggunaan
    tingkat kepercayaan yang lebih tinggi membuat
    pengukuran berfokus pada kondisi kerugian yang
    lebih ekstrem.

    **4. Periode penurunan AKO terbesar**

    Berdasarkan hasil analisis historis, penurunan
    AKO terbesar terjadi pada periode 2023 Q1.
    Periode tersebut menjadi salah satu observasi
    penting dalam menggambarkan risiko perubahan
    arus kas operasi perusahaan.
    """
)

st.info(
    "Nilai VaR dan CVaR merupakan estimasi berdasarkan "
    "distribusi kerugian historis, bukan batas maksimum "
    "kerugian yang pasti terjadi pada masa mendatang."
)

