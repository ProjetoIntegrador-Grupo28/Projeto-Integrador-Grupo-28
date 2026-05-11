import streamlit as st
import pandas as pd
from pathlib import Path
from charts import plot_sobrevivencia_titulo, plot_viajava_sozinho, plot_sobrevivencia_familia, plot_sobrevivencia_porto

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
    # .parent sobe para a raiz, permitindo entrar em /data
    caminho = BASE_DIR.parent / "data" / "processed" / "titanic_cleaned.csv"
    
    # Verifica se o arquivo existe antes de tentar ler
    if not caminho.exists():
        st.error(f"Arquivo não encontrado: {caminho}")
        return pd.DataFrame()
        
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

# graficos 4-6
st.divider() 
st.subheader("Análise Social e Familiar")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    fig_titulo = plot_sobrevivencia_titulo(df_filtrado)
    st.plotly_chart(fig_titulo, use_container_width=True)

with col_graf2:
    fig_sozinho = plot_viajava_sozinho(df_filtrado)
    st.plotly_chart(fig_sozinho, use_container_width=True)

st.divider()
st.subheader("Análise de Família e Embarque")

# Cria uma nova linha com duas colunas
col_graf3, col_graf4 = st.columns(2)

#graficos 5-7
with col_graf3:
    fig_familia = plot_sobrevivencia_familia(df_filtrado)
    st.plotly_chart(fig_familia, use_container_width=True)

with col_graf4:
    fig_porto = plot_sobrevivencia_porto(df_filtrado)
    st.plotly_chart(fig_porto, use_container_width=True)   