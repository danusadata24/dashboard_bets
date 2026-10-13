import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração da página (Layout wide para melhor aproveitamento visual)
st.set_page_config(page_title="Dashboard Gerencial - Bets UFPI", layout="wide")

# --- 1. GERAÇÃO DE DADOS FICTÍCIOS ---
@st.cache_data
def carregar_dados():
    np.random.seed(42)
    n_linhas = 1000
    
    datas = pd.date_range(start="2026-09-01", periods=30, freq="D")
    data_apostas = np.random.choice(datas, n_linhas)

    esportes = ['Futebol', 'Basquete', 'eSports', 'Tênis', 'Futebol Americano']
    esporte = np.random.choice(esportes, n_linhas, p=[0.5, 0.2, 0.15, 0.1, 0.05])
    
    regioes = ['Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste', 'Norte']
    regiao = np.random.choice(regioes, n_linhas, p=[0.4, 0.3, 0.15, 0.1, 0.05])
    
    valor_apostado = np.random.exponential(scale=50, size=n_linhas).round(2) + 10
    
    # Resultado da aposta (Casa ganha mais vezes estatisticamente)
    status = np.random.choice(['Perdida', 'Ganha'], n_linhas, p=[0.65, 0.35])
    df = pd.DataFrame({
        'Data': data_apostas,
        'Esporte': esporte,
        'Regiao': regiao,
        'Valor_Apostado': valor_apostado,
        'Status': status
    })
    
    df['Lucro_Casa'] = np.where(df['Status'] == 'Perdida', df['Valor_Apostado'], -df['Valor_Apostado'] * 0.8)
    return df

df = carregar_dados()

# --- 2. CABEÇALHO E CONCEITO DE SHNEIDERMAN (Overview) ---
st.title("🎯 Painel Analítico de Risco: Plataforma BetAnalytics")
st.markdown("Monitoramento gerencial de fluxo de apostas, distribuição por modalidade e controle de caixa.")

# Sidebar para Filtros (Zoom and Filter)
st.sidebar.header("Filtros Globais (Zoom & Filter)")
regiao_sel = st.sidebar.selectbox("Filtrar por Região", ['Todas'] + list(df['Regiao'].unique()))
esporte_sel = st.sidebar.selectbox("Filtrar por Esporte", ['Todas'] + list(df['Esporte'].unique()))

# Aplicando filtros (Brushing & Linking lógico)
df_filtrado = df.copy()
if regiao_sel != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Regiao'] == regiao_sel]
if esporte_sel != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Esporte'] == esporte_sel]

# --- 3. MÉTRICAS PRINCIPAIS (KPIs) ---
col1, col2, col3 = st.columns(3)
col1.metric("Volume Total Apostado", f"R$ {df_filtrado['Valor_Apostado'].sum():,.2f}")
col2.metric("Resultado Operacional (Casa)", f"R$ {df_filtrado['Lucro_Casa'].sum():,.2f}")
col3.metric("Total de Bilhetes", len(df_filtrado))

st.markdown("---")

# --- 4. CONSTRUÇÃO DOS 3 GRÁFICOS COORDENADOS ---
col_A, col_B = st.columns(2)

with col_A:
    st.subheader("1. Visão Geral Temporal (Série Histórica)")
    # Gráfico 1: Evolução temporal do valor apostado por dia
    df_tempo = df_filtrado.groupby('Data')['Valor_Apostado'].sum().reset_index()
    fig_tempo = px.line(
        df_tempo, x='Data', y='Valor_Apostado', 
        markers=True, title="Evolução Diária de Apostas",
        labels={'Valor_Apostado': 'Total Apostado (R$)', 'Data': 'Data'}
    )
    fig_tempo.update_layout(template="plotly_white", margin=dict(t=30, b=10, l=10, r=10))
    st.plotly_chart(fig_tempo, use_container_width=True)

with col_B:
    st.subheader("2. Distribuição Categórica")
    # Gráfico 2: Barras ordenadas por Esporte e Status
    df_cat = df_filtrado.groupby(['Esporte', 'Status'])['Valor_Apostado'].sum().reset_index()
    fig_cat = px.bar(
        df_cat, x='Esporte', y='Valor_Apostado', color='Status',
        title="Volume por Esporte e Status da Aposta",
        barmode='group',
        color_discrete_map={'Perdida': '#2b5c8f', 'Ganha': '#d95f02'} # Cores amigáveis e limpas
    )
    fig_cat.update_layout(template="plotly_white", margin=dict(t=30, b=10, l=10, r=10))
    st.plotly_chart(fig_cat, use_container_width=True)

# --- 5. PAINEL DE DETALHES SOB DEMANDA (Details-on-Demand) ---
st.subheader("3. Detalhes sob Demanda (Amostra de Transações)")
st.markdown("Abaixo encontram-se os registros detalhados correspondentes ao filtro aplicado:")
st.dataframe(df_filtrado[['Data', 'Regiao', 'Esporte', 'Valor_Apostado', 'Status', 'Lucro_Casa']].head(10), use_container_width=True)
import streamlit as st

st.title("Teste UFPI")
st.write("Se estás a ver isto, o Streamlit está a funcionar perfeitamente!")
