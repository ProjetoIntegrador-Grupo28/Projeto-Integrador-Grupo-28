"""
charts.py – Visualizações 1, 2 e 3 do Dashboard Titanic (Grupo 28)
Responsáveis: Pedro, Karla

Funções:
    plot_sobrevivencia_classe(df)  → Vis. 1: Barras agrupadas por Classe Social
    plot_sobrevivencia_genero(df)  → Vis. 2: Donut por Gênero
    plot_sobrevivencia_faixa(df)   → Vis. 3: Barras por Faixa Etária

Cada função recebe o DataFrame já filtrado pela sidebar e retorna
uma figura Plotly pronta para ser exibida com st.plotly_chart().
"""

import plotly.graph_objects as go
import pandas as pd

# ── Paleta e tipografia coerentes com o tema do projeto ──────────────────────
CORES = {
    "sobreviveu":    "#4A90D9",   # azul oceano
    "nao_sobreviveu": "#C0392B",  # vermelho âncora
    "fundo":         "rgba(0,0,0,0)",
    "texto":         "#2C3E50",
    "grade":         "rgba(44,62,80,0.08)",
}

LAYOUT_BASE = dict(
    paper_bgcolor=CORES["fundo"],
    plot_bgcolor=CORES["fundo"],
    font=dict(family="Georgia, serif", color=CORES["texto"], size=13),
    margin=dict(t=60, b=40, l=40, r=20),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor="rgba(255,255,255,0.6)",
        bordercolor=CORES["grade"],
        borderwidth=1,
    ),
)


# ─────────────────────────────────────────────────────────────────────────────
# VIS. 1 – Barras agrupadas por Classe Social
# ─────────────────────────────────────────────────────────────────────────────
def plot_sobrevivencia_classe(df: pd.DataFrame) -> go.Figure:
    """
    Retorna um gráfico de barras agrupadas mostrando a contagem de
    sobreviventes e não-sobreviventes por classe do passageiro.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame filtrado. Deve conter as colunas:
        - 'classe_pax'  (int ou str: 1, 2, 3)
        - 'sobreviveu'  (int: 0 ou 1)
    """
    if df.empty:
        return _grafico_vazio("Nenhum dado para os filtros selecionados")

    # Agrega contagem por classe e sobrevivência
    agg = (
        df.groupby(["classe_pax", "sobreviveu"])
        .size()
        .reset_index(name="contagem")
    )

    classes_label = {1: "1ª Classe", 2: "2ª Classe", 3: "3ª Classe"}
    agg["classe_label"] = agg["classe_pax"].map(classes_label)

    sobreviventes     = agg[agg["sobreviveu"] == 1]
    nao_sobreviventes = agg[agg["sobreviveu"] == 0]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Sobreviveu",
        x=sobreviventes["classe_label"],
        y=sobreviventes["contagem"],
        marker_color=CORES["sobreviveu"],
        text=sobreviventes["contagem"],
        textposition="outside",
        textfont=dict(size=12),
    ))

    fig.add_trace(go.Bar(
        name="Não sobreviveu",
        x=nao_sobreviventes["classe_label"],
        y=nao_sobreviventes["contagem"],
        marker_color=CORES["nao_sobreviveu"],
        text=nao_sobreviventes["contagem"],
        textposition="outside",
        textfont=dict(size=12),
    ))

    # Taxa de sobrevivência como anotação por classe
    taxas = (
        df.groupby("classe_pax")["sobreviveu"]
        .mean()
        .mul(100)
        .round(1)
    )
    for classe, taxa in taxas.items():
        fig.add_annotation(
            x=classes_label.get(classe, str(classe)),
            y=0,
            yref="paper",
            text=f"<b>{taxa}%</b> taxa",
            showarrow=False,
            yshift=-28,
            font=dict(size=11, color=CORES["texto"]),
        )

    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(
            text="<b>Sobrevivência por Classe Social</b>",
            font=dict(size=16),
            x=0.02,
        ),
        barmode="group",
        bargap=0.25,
        bargroupgap=0.08,
        xaxis=dict(title="Classe", showgrid=False),
        yaxis=dict(
            title="Nº de Passageiros",
            gridcolor=CORES["grade"],
            showgrid=True,
        ),
    )

    return fig


# ─────────────────────────────────────────────────────────────────────────────
# VIS. 2 – Donut por Gênero
# ─────────────────────────────────────────────────────────────────────────────
def plot_sobrevivencia_genero(df: pd.DataFrame) -> go.Figure:
    """
    Retorna um gráfico donut duplo (anel externo = sobreviventes,
    anel interno = total) mostrando a proporção de sobrevivência por gênero.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame filtrado. Deve conter as colunas:
        - 'sexo'        (str: 'masculino' / 'feminino')
        - 'sobreviveu'  (int: 0 ou 1)
    """
    if df.empty:
        return _grafico_vazio("Nenhum dado para os filtros selecionados")

    agg = df.groupby("sexo")["sobreviveu"].agg(["sum", "count"]).reset_index()
    agg.columns = ["sexo", "sobreviventes", "total"]
    agg["nao_sobreviventes"] = agg["total"] - agg["sobreviventes"]
    agg["taxa"] = (agg["sobreviventes"] / agg["total"] * 100).round(1)

    # Labels e cores por gênero
    cores_genero = {
        "feminino":   ["#4A90D9", "#C0D8F0"],
        "masculino":  ["#C0392B", "#F0BEBE"],
    }

    fig = go.Figure()

    for _, row in agg.iterrows():
        genero  = row["sexo"]
        c_vivo, c_morto = cores_genero.get(genero, ["#888", "#ccc"])
        label   = "Feminino" if genero == "feminino" else "Masculino"

        fig.add_trace(go.Pie(
            name=label,
            labels=["Sobreviveu", "Não sobreviveu"],
            values=[row["sobreviventes"], row["nao_sobreviventes"]],
            hole=0.55,
            marker_colors=[c_vivo, c_morto],
            textinfo="label+percent",
            textfont=dict(size=12),
            domain={
                "x": [0, 0.46] if genero == "feminino" else [0.54, 1],
                "y": [0, 1],
            },
            title=dict(
                text=f"<b>{label}</b><br>{row['taxa']}% sobreviveram",
                font=dict(size=13),
            ),
        ))

    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(
            text="<b>Sobrevivência por Gênero</b>",
            font=dict(size=16),
            x=0.02,
        ),
    )

    return fig


# ─────────────────────────────────────────────────────────────────────────────
# VIS. 3 – Barras por Faixa Etária
# ─────────────────────────────────────────────────────────────────────────────
def plot_sobrevivencia_faixa(df: pd.DataFrame) -> go.Figure:
    """
    Retorna um gráfico de barras empilhadas com a taxa de sobrevivência
    (%) por faixa etária, com volume total como anotação secundária.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame filtrado. Deve conter as colunas:
        - 'faixa_etaria' (str: 'Criança', 'Adolescente', 'Adulto', 'Idoso')
        - 'sobreviveu'   (int: 0 ou 1)
    """
    if df.empty:
        return _grafico_vazio("Nenhum dado para os filtros selecionados")

    # Ordem canônica das faixas
    ordem = ["Criança", "Adolescente", "Adulto", "Idoso"]

    agg = df.groupby("faixa_etaria")["sobreviveu"].agg(["sum", "count"]).reset_index()
    agg.columns = ["faixa_etaria", "sobreviventes", "total"]
    agg["nao_sobreviventes"] = agg["total"] - agg["sobreviventes"]
    agg["pct_sobreviveu"]    = (agg["sobreviventes"] / agg["total"] * 100).round(1)
    agg["pct_nao"]           = (100 - agg["pct_sobreviveu"]).round(1)

    # Reordena conforme ordem canônica (filtra só as presentes no df filtrado)
    agg["faixa_etaria"] = pd.Categorical(agg["faixa_etaria"], categories=ordem, ordered=True)
    agg = agg.sort_values("faixa_etaria")

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Sobreviveu",
        x=agg["faixa_etaria"].astype(str),
        y=agg["pct_sobreviveu"],
        marker_color=CORES["sobreviveu"],
        text=agg["pct_sobreviveu"].apply(lambda v: f"{v}%"),
        textposition="inside",
        textfont=dict(size=12, color="white"),
    ))

    fig.add_trace(go.Bar(
        name="Não sobreviveu",
        x=agg["faixa_etaria"].astype(str),
        y=agg["pct_nao"],
        marker_color=CORES["nao_sobreviveu"],
        text=agg["pct_nao"].apply(lambda v: f"{v}%"),
        textposition="inside",
        textfont=dict(size=12, color="white"),
    ))

    # Volume total como anotação acima de cada barra
    for _, row in agg.iterrows():
        fig.add_annotation(
            x=str(row["faixa_etaria"]),
            y=102,
            text=f"n={row['total']}",
            showarrow=False,
            font=dict(size=10, color=CORES["texto"]),
        )

    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(
            text="<b>Sobrevivência por Faixa Etária</b>",
            font=dict(size=16),
            x=0.02,
        ),
        barmode="stack",
        bargap=0.3,
        xaxis=dict(title="Faixa Etária", showgrid=False),
        yaxis=dict(
            title="% de Passageiros",
            range=[0, 115],
            gridcolor=CORES["grade"],
            ticksuffix="%",
        ),
    )

    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Utilitário interno
# ─────────────────────────────────────────────────────────────────────────────
def _grafico_vazio(mensagem: str) -> go.Figure:
    """Retorna uma figura com mensagem amigável quando o df está vazio."""
    fig = go.Figure()
    fig.add_annotation(
        text=mensagem,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=15, color="#888"),
    )
    fig.update_layout(**LAYOUT_BASE)
    return fig
