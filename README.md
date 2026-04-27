# 📊 MapBiomas Alertas – Visualizador de Legalidade

Aplicação interativa desenvolvida em **Streamlit** para explorar dados do **MapBiomas Alertas**, com foco na análise da **situação legal de alertas de desmatamento**.

O objetivo é permitir uma leitura rápida e estruturada de:

- evidências de **autorização**
- registros de **infrações**
- ações de **fiscalização**
- presença de **embargos**
- e a **situação final consolidada** dos alertas

---

## 🎯 Objetivo

Este projeto busca responder perguntas-chave para conservação e governança:

- Qual a proporção de alertas com **algum tipo de ação ou autorização**?
- Quanto da área está **sem qualquer evidência de legalidade**?
- Como isso varia ao longo do tempo, entre biomas e estados?
- Onde estão os principais **gaps de fiscalização e resposta institucional**?

---

## 📁 Estrutura dos dados

O dataset utilizado é um consolidado dos alertas com os seguintes campos:

| Campo | Descrição |
|------|----------|
| `year` | Ano do alerta |
| `biome` | Bioma (Amazônia, Cerrado, Mata Atlântica) |
| `state` | Estado |
| `area_ha` | Área do alerta (hectares) |
| `auto` | Situação de auto de infração |
| `asvs` | Situação de autorização (ASV) |
| `fiscalizations` | Existência de fiscalização |
| `embargoed_areas` | Situação de embargo |
| `actions_final_situation` | Indica se houve alguma ação |
| `final_situation` | Síntese final (com ou sem ação/autorização) |

---

## ⚖️ Interpretação da legalidade

A variável **`final_situation`** resume o cruzamento entre os dados:

- `1` → Alerta com **algum tipo de ação ou autorização**
- `0` → Alerta **sem evidência de ação ou autorização**

⚠️ Importante:  
"Sem ação" **não significa automaticamente ilegal**, mas indica ausência de registro de resposta institucional.

---

## 🚀 Funcionalidades

O app permite:

### 🔎 Filtros interativos
- Ano
- Bioma
- Estado

### 📊 Indicadores principais (KPIs)
- Número de alertas
- Área total
- Área sem ação/autorização
- % da área sem ação

### 📈 Visualizações
- Série temporal da área de alertas
- Distribuição por bioma
- Situação final (com vs sem ação)

### 📄 Exploração de dados
- Tabela interativa
- Download dos dados filtrados

---

## 🧪 Como rodar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/barroso2501/Streamlit_MapBiomas_Alertas.git
cd Streamlit_MapBiomas_Alertas
