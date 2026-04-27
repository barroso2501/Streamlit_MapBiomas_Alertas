import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(layout="wide")

st.title("📊 MapBiomas Alertas - Legalidade")
st.markdown("Visualização exploratória dos alertas e sua situação legal")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_excel("data/legality_consolidated_report.xlsx")
    return df

df = load_data()

# =========================
# SIDEBAR (FILTROS)
# =========================
st.sidebar.header("Filtros")

anos = st.sidebar.multiselect(
    "Ano",
    sorted(df["year"].unique()),
    default=sorted(df["year"].unique())
)

biomas = st.sidebar.multiselect(
    "Bioma",
    sorted(df["biome"].unique()),
    default=sorted(df["biome"].unique())
)

estados = st.sidebar.multiselect(
    "Estado",
    sorted(df["state"].unique()),
    default=sorted(df["state"].unique())
)

df_filt = df[
    (df["year"].isin(anos)) &
    (df["biome"].isin(biomas)) &
    (df["state"].isin(estados))
]

# =========================
# KPIs
# =========================
total_alertas = len(df_filt)
area_total = df_filt["area_ha"].sum()

area_sem_acao = df_filt[df_filt["final_situation"] == 0]["area_ha"].sum()
perc_sem_acao = (area_sem_acao / area_total * 100) if area_total > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Alertas", f"{total_alertas:,}")
col2.metric("Área total (ha)", f"{area_total:,.0f}")
col3.metric("Área sem ação (ha)", f"{area_sem_acao:,.0f}")
col4.metric("% sem ação", f"{perc_sem_acao:.1f}%")

st.markdown("---")

# =========================
# GRÁFICO 1 - Série temporal
# =========================
df_year = df_filt.groupby("year")["area_ha"].sum().reset_index()

fig1 = px.bar(
    df_year,
    x="year",
    y="area_ha",
    title="Área de alertas por ano"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# GRÁFICO 2 - Bioma
# =========================
df_biome = df_filt.groupby("biome")["area_ha"].sum().reset_index()

fig2 = px.pie(
    df_biome,
    names="biome",
    values="area_ha",
    title="Distribuição por bioma"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# GRÁFICO 3 - Situação final
# =========================
df_final = df_filt.groupby("final_situation")["area_ha"].sum().reset_index()

df_final["label"] = df_final["final_situation"].map({
    0: "Sem ação/autorização",
    1: "Com ação ou autorização"
})

fig3 = px.bar(
    df_final,
    x="label",
    y="area_ha",
    title="Situação final dos alertas"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# TABELA
# =========================
st.markdown("### 📄 Dados filtrados")

st.dataframe(df_filt, use_container_width=True)

# =========================
# DOWNLOAD
# =========================
csv = df_filt.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Baixar CSV",
    csv,
    "alertas_filtrados.csv",
    "text/csv"
)
