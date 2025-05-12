import streamlit as st
import json
import random
import time
import plotly.graph_objects as go
import pandas as pd

# CONFIGURAÇÕES GERAIS
st.set_page_config(layout="wide", page_title="Painel PET-ACE")
st.markdown(
    """
    <style>
        body {
            background-color: black;
        }
        .main {
            background-color: black;
        }
        h1, h2, h3, h4, h5, h6, p, div, span {
            color: white !important;
        }
        .news-box {
            background-color: orange;
            color: black;
            padding: 15px;
            border-radius: 10px;
            animation: blink 1s infinite;
        }
        @keyframes blink {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# TÍTULO
st.markdown("<h1 style='text-align: center;'>Painel PET-ACE</h1>", unsafe_allow_html=True)
st.markdown("---")

# CARREGAR DADOS
with open("dados_acoes.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

acoes = list(dados.keys())
valores = [dados[acao]["preco"] for acao in acoes]

# CRIAR COLUNAS
col1, col2 = st.columns([2, 1])

# GRÁFICO
with col1:
    df = pd.DataFrame({"Ação": acoes, "Preço": valores})
    fig = go.Figure(
        data=[
            go.Bar(
                x=df["Ação"],
                y=df["Preço"],
                marker=dict(color="orange")
            )
        ]
    )
    fig.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white'),
        title='Desempenho das Ações'
    )
    st.plotly_chart(fig, use_container_width=True)

# FEED DE NOTÍCIAS
noticias = [
    "Mercado reage positivamente à nova política fiscal.",
    "Investidores internacionais voltam ao Brasil.",
    "Selic deve cair nas próximas reuniões do COPOM.",
    "Setor de tecnologia lidera ganhos na bolsa.",
    "PET-ACE lança novo projeto de educação financeira.",
    "Alta do dólar pressiona inflação de alimentos.",
    "Ibovespa opera em alta impulsionado por bancos.",
]

with col2:
    noticia_aleatoria = random.choice(noticias)
    st.markdown(
        f"""
        <div class="news-box">
            <h3>Última Notícia</h3>
            <p>{noticia_aleatoria}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ATUALIZAÇÃO AUTOMÁTICA (opcional)
time.sleep(5)
st.rerun()

