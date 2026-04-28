import streamlit as st
import pandas as pd
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Projeto Integrador - Grupo 28",
    page_icon="🚀",  # O emoji pode ser alterado caso o grupo queira
    layout="wide"
)

# Carregar o CSV tratado
BASE_DIR = Path(__file__).resolve().parent

@st.cache_data
def load_data():
    caminho = BASE_DIR.parent / "Data/processed/titanic_cleaned.csv"
    return pd.read_csv(caminho)

df = load_data()

# Criar a sidebar (estrutura)
st.sidebar.title("Filtros")

# Filtro de Classe
classes_disponiveis = sorted(df['classe_pax'].unique())
filtro_classe = st.sidebar.multiselect(
    "Classe",
    options=classes_disponiveis,
    default=classes_disponiveis
)

# Filtro de Gênero
generos_disponiveis = sorted(df['sexo'].unique())
filtro_genero = st.sidebar.multiselect(
    "Gênero",
    options=generos_disponiveis,
    default=generos_disponiveis
)

# Filtro de Faixa Etária
ordem_faixas = ['Criança', 'Adolescente', 'Adulto', 'Idoso']
faixas_disponiveis = [f for f in ordem_faixas if f in df['faixa_etaria'].unique()]
filtro_faixa = st.sidebar.multiselect(
    "Faixa Etária",
    options=faixas_disponiveis,
    default=faixas_disponiveis
)

# Filtro: Viajava Sozinho
solo_disponiveis = sorted(df['viajava_sozinho'].unique())
filtro_solo = st.sidebar.multiselect(
    "Viajava Sozinho?",
    options=solo_disponiveis,
    default=solo_disponiveis
)

# Aplicar todos os filtros no DataFrame
df_filtrado = df[
    df['classe_pax'].isin(filtro_classe) &
    df['sexo'].isin(filtro_genero) &
    df['faixa_etaria'].isin(filtro_faixa) &
    df['viajava_sozinho'].isin(filtro_solo)
]



# PASSO 6 — Criar área de KPIs
st.markdown("## KPIs Gerais")
col1, col2, col3, col4 = st.columns(4)



# Cálculo dos KPIs
taxa_sobrevivencia = df_filtrado['sobreviveu'].mean() * 100
total_passageiros = len(df_filtrado)
media_idade = df_filtrado['idade'].mean()

df_feminino = df_filtrado[df_filtrado['sexo'] == 'feminino']
taxa_feminina = df_feminino['sobreviveu'].mean() * 100 if len(df_feminino) > 0 else 0

# Exibição dos KPIs
with col1:
    st.metric("Taxa de Sobrevivência", f"{taxa_sobrevivencia:.1f}%")

with col2:
    st.metric("Total de Passageiros", total_passageiros)

with col3:
    st.metric("Média de Idade", f"{media_idade:.1f} anos")

with col4:
    st.metric("Sobrevivência Feminina", f"{taxa_feminina:.1f}%")
