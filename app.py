import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="MapBiomas Alertas - Legalidade",
    layout="wide"
)

st.title("📊 MapBiomas Alertas - Legalidade")
st.markdown(
    "Visualizador exploratório da situação legal dos alertas, "
    "com foco na variação anual e nos perfis por bioma e estado."
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_excel("data/legality_consolidated_report.xlsx")

    # Padronização simples
    df.columns = df.columns.str.strip()

    return df


df = load_data()

# =========================
# LEGAL STATUS CLASSIFICATION
# =========================
def classify_legal_status(row):
    """
    Classificação interpretativa da situação legal.

    Prioridade:
    1. Autorização / ASV
    2. Auto de infração ou embargo
    3. Fiscalização sem decisão clara
    4. Sem informação
    """

    if row["asvs"] == 1:
        return "Legal/autorizado"

    elif (row["auto"] == 1) or (row["embargoed_areas"] == 1):
        return "Ilegal detectado"

    elif row["fiscalizations"] == 1:
        return "Fiscalizado sem decisão clara"

    else:
        return "Sem informação"


df["legal_status"] = df.apply(classify_legal_status, axis=1)

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filtros")

anos = st.sidebar.multiselect(
    "Ano",
    sorted(df["year"].dropna().unique()),
    default=sorted(df["year"].dropna().unique())
)

biomas = st.sidebar.multiselect(
    "Bioma",
    sorted(df["biome"].dropna().unique()),
    default=sorted(df["biome"].dropna().unique())
)

estados = st.sidebar.multiselect(
    "Estado",
    sorted(df["state"].dropna().unique()),
    default=sorted(df["state"].dropna().unique())
)

status_legais = st.sidebar.multiselect(
    "Situação legal",
    sorted(df["legal_status"].unique()),
    default=sorted(df["legal_status"].unique())
)

df_filt = df[
    (df["year"].isin(anos)) &
    (df["biome"].isin(biomas)) &
    (df["state"].isin(estados)) &
    (df["legal_status"].isin(status_legais))
].copy()

# =========================
# KPIs
# =========================
st.markdown("## Indicadores gerais")

total_alertas = len(df_filt)
area_total = df_filt["area_ha"].sum()

area_sem_info = df_filt.loc[df_filt["legal_status"] == "Sem informação", "area_ha"].sum()
area_ilegal = df_filt.loc[df_filt["legal_status"] == "Ilegal detectado", "area_ha"].sum()
area_legal = df_filt.loc[df_filt["legal_status"] == "Legal/autorizado", "area_ha"].sum()
area_fiscalizada = df_filt.loc[df_filt["legal_status"] == "Fiscalizado sem decisão clara", "area_ha"].sum()

def pct(value, total):
    return (value / total * 100) if total > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Alertas", f"{total_alertas:,}")
col2.metric("Área total (ha)", f"{area_total:,.0f}")
col3.metric("Sem informação", f"{pct(area_sem_info, area_total):.1f}%")
col4.metric("Ilegal detectado", f"{pct(area_ilegal, area_total):.1f}%")
col5.metric("Legal/autorizado", f"{pct(area_legal, area_total):.1f}%")

st.caption(
    "Nota: 'Sem informação' indica ausência de cruzamento com autorização, auto, fiscalização ou embargo "
    "na base consolidada. Não deve ser interpretado automaticamente como ilegalidade."
)

st.markdown("---")

# =========================
# MAIN CHART 1 - ANNUAL VARIATION
# =========================
st.markdown("## Evolução anual da situação legal")

df_year_status = (
    df_filt
    .groupby(["year", "legal_status"], as_index=False)["area_ha"]
    .sum()
)

fig_year = px.bar(
    df_year_status,
    x="year",
    y="area_ha",
    color="legal_status",
    title="Área de alertas por ano e situação legal",
    labels={
        "year": "Ano",
        "area_ha": "Área (ha)",
        "legal_status": "Situação legal"
    }
)

st.plotly_chart(fig_year, use_container_width=True)

# =========================
# MAIN CHART 2 - ANNUAL PERCENTAGE
# =========================
df_year_total = (
    df_year_status
    .groupby("year", as_index=False)["area_ha"]
    .sum()
    .rename(columns={"area_ha": "area_total_year"})
)

df_year_pct = df_year_status.merge(df_year_total, on="year")
df_year_pct["percent"] = df_year_pct["area_ha"] / df_year_pct["area_total_year"] * 100

fig_year_pct = px.bar(
    df_year_pct,
    x="year",
    y="percent",
    color="legal_status",
    title="Composição percentual anual da situação legal",
    labels={
        "year": "Ano",
        "percent": "% da área anual",
        "legal_status": "Situação legal"
    }
)

st.plotly_chart(fig_year_pct, use_container_width=True)

st.markdown("---")

# =========================
# PROFILE BY BIOME / STATE
# =========================
st.markdown("## Perfil espacial da situação legal")

nivel = st.radio(
    "Escolha o nível de agregação:",
    ["state", "biome"],
    horizontal=True
)

label_nivel = {
    "state": "Estado",
    "biome": "Bioma"
}

df_profile = (
    df_filt
    .groupby([nivel, "legal_status"], as_index=False)["area_ha"]
    .sum()
)

fig_profile = px.bar(
    df_profile,
    x=nivel,
    y="area_ha",
    color="legal_status",
    title=f"Área de alertas por {label_nivel[nivel]} e situação legal",
    labels={
        nivel: label_nivel[nivel],
        "area_ha": "Área (ha)",
        "legal_status": "Situação legal"
    }
)

st.plotly_chart(fig_profile, use_container_width=True)

# =========================
# PROFILE PERCENTAGE
# =========================
df_profile_total = (
    df_profile
    .groupby(nivel, as_index=False)["area_ha"]
    .sum()
    .rename(columns={"area_ha": "area_total"})
)

df_profile_pct = df_profile.merge(df_profile_total, on=nivel)
df_profile_pct["percent"] = df_profile_pct["area_ha"] / df_profile_pct["area_total"] * 100

fig_profile_pct = px.bar(
    df_profile_pct,
    x=nivel,
    y="percent",
    color="legal_status",
    title=f"Composição percentual por {label_nivel[nivel]}",
    labels={
        nivel: label_nivel[nivel],
        "percent": "% da área",
        "legal_status": "Situação legal"
    }
)

st.plotly_chart(fig_profile_pct, use_container_width=True)

st.markdown("---")

# =========================
# SUMMARY TABLE
# =========================
st.markdown("## Tabela resumo")

df_summary = (
    df_filt
    .groupby(["year", "biome", "state", "legal_status"], as_index=False)
    .agg(
        alerts=("area_ha", "count"),
        area_ha=("area_ha", "sum")
    )
)

df_summary["area_ha"] = df_summary["area_ha"].round(2)

st.dataframe(df_summary, use_container_width=True)

# =========================
# RAW DATA
# =========================
with st.expander("Ver dados filtrados"):
    st.dataframe(df_filt, use_container_width=True)

# =========================
# DOWNLOAD
# =========================
csv_summary = df_summary.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Baixar tabela resumo em CSV",
    csv_summary,
    "mapbiomas_alertas_legalidade_resumo.csv",
    "text/csv"
)

csv_raw = df_filt.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Baixar dados filtrados em CSV",
    csv_raw,
    "mapbiomas_alertas_legalidade_dados_filtrados.csv",
    "text/csv"
)
