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
# graficos 5-7
def plot_sobrevivencia_familia(df: pd.DataFrame):
    if df.empty:
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_annotation(text="Sem dados", showarrow=False)
        return fig

    # Como a equipe já criou a coluna "tamanho_familia" no ETL, 
    # não precisamos somar "irmaos_conjuges" e "pais_filhos" aqui.
    # Vamos usar a coluna que já existe direto!
    
    # Agrupa e calcula a média de sobrevivência
    sobrevivencia_familia = df.groupby("tamanho_familia")["sobreviveu"].mean().reset_index()
    # Multiplica por 100 para ficar em porcentagem
    sobrevivencia_familia["sobreviveu"] = sobrevivencia_familia["sobreviveu"] * 100

    # Cria o gráfico de barras com Plotly
    fig = px.bar(
        sobrevivencia_familia, 
        x="tamanho_familia", 
        y="sobreviveu",
        text_auto='.1f' # Mostra o número em cima da barra
    )
    
    fig.update_layout(
        title=dict(text="<b>Taxa de Sobrevivência por Tamanho da Família</b>", font=dict(size=16)),
        xaxis_title="Tamanho da Família",
        yaxis_title="Taxa de Sobrevivência (%)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def plot_sobrevivencia_porto(df: pd.DataFrame):
    if df.empty:
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_annotation(text="Sem dados", showarrow=False)
        return fig

    df_plot = df.copy()
    
    # Usando o nome correto da coluna que você encontrou: "porto_embarque"
    df_plot["nome_porto"] = df_plot["porto_embarque"].replace({
        "C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"
    })
    
    # Agrupa e calcula a média
    sobrevivencia_porto = df_plot.groupby("nome_porto")["sobreviveu"].mean().reset_index()
    sobrevivencia_porto["sobreviveu"] = sobrevivencia_porto["sobreviveu"] * 100

    fig = px.bar(
        sobrevivencia_porto, 
        x="nome_porto", 
        y="sobreviveu",
        color="nome_porto", # Dá uma cor diferente para cada porto
        text_auto='.1f'
    )
    
    fig.update_layout(
        title=dict(text="<b>Taxa de Sobrevivência por Porto de Embarque</b>", font=dict(size=16)),
        xaxis_title="Porto de Embarque",
        yaxis_title="Taxa de Sobrevivência (%)",
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig