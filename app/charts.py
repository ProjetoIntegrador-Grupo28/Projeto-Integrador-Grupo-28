import pandas as pd
import plotly.express as px

# -------------------------------------------------------------------------
# VISUALIZAÇÃO 4: GRÁFICO DE BARRAS HORIZONTAIS (TÍTULO SOCIAL)
# -------------------------------------------------------------------------
def plot_sobrevivencia_titulo(df: pd.DataFrame):
    
    # TRAVA DE SEGURANÇA: 
    # Verifica se a tabela está vazia, caso o usuário marque filtros que não combinam
    # Se estiver vazia, retorna um gráfico em branco com a mensagem "Sem dados" p o aplicativo n quebrar
    if df.empty:
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_annotation(text="Sem dados", showarrow=False)
        return fig

    df_plot = df.copy()
    # Trocando os números 0 e 1 pelas palavras correspondentes
    df_plot['sobreviveu'] = df_plot['sobreviveu'].map({0: 'Não sobreviveu', 1: 'Sobreviveu'})

    # Agora usamos o df_plot no histograma no lugar do df
    fig = px.histogram(
        df_plot, 
        y="titulo_social", 
        color="sobreviveu", 
        orientation='h', 
        barmode='group'
    )
    
    fig.update_layout(
        title=dict(text="<b>Sobrevivência por Título Social</b>", font=dict(size=16)),
        yaxis_title="Título Social",
        xaxis_title="Quantidade de Passageiros",
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)"   
    )
    
    return fig

# -------------------------------------------------------------------------
# VISUALIZAÇÃO 6: GRÁFICO DE PIZZA / DONUT (VIAJAVA SOZINHO)
# -------------------------------------------------------------------------
def plot_viajava_sozinho(df: pd.DataFrame):
    
    # Mesma trava de segurança
    if df.empty:
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_annotation(text="Sem dados", showarrow=False)
        return fig

    # PREPARANDO OS DADOS:
    # Diferente do histograma, o gráfico de pizza precisa que a gente conte os dados antes.
    # value_counts() conta quantos passageiros estavam sozinhos e quantos acompanhados.
    # reset_index() transforma essa contagem solta em uma tabelinha organizada.
    contagem_solo = df['viajava_sozinho'].value_counts().reset_index()
    
    # Renomeei as colunas 
    contagem_solo.columns = ['viajava_sozinho', 'Quantidade']
    
    fig = px.pie(
        contagem_solo, 
        names='viajava_sozinho', 
        values='Quantidade',     
        hole=0.4                
    )
    
    fig.update_traces(textinfo='percent+label')
    
    fig.update_layout(
        title=dict(text="<b>Proporção: Viajava Sozinho?</b>", font=dict(size=16)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig