import streamlit as st
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="PET Invest", layout="wide")

# Lista de resultados
if "ranking" not in st.session_state:
    st.session_state.ranking = []

# Estilo
st.markdown("""
    <style>
        body { background-color: #0e1117; color: #ffffff; }
        .stApp { background-color: #0e1117; }
        table { background-color: #1c1f26; border-radius: 10px; padding: 10px; }
        td { padding: 5px 10px; }
        .titulo { font-size: 32px; color: #00ccff; font-weight: bold; }
        .bloco { background-color: #1c1f26; padding: 20px; border-radius: 15px; }
        .stButton>button { background-color: #00ccff; color: black; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='titulo'>📈 PET Invest – Terminal Simulador de Bolsa</div>", unsafe_allow_html=True)

# Definições das ações e preços
acoes = {
    "TechBrasil (R$100)": ("TechBrasil", 100),
    "AgroVale (R$80)": ("AgroVale", 80),
    "PetroMax (R$120)": ("PetroMax", 120),
    "EcoEnergia (R$60)": ("EcoEnergia", 60),
    "BancoReal (R$90)": ("BancoReal", 90)
}

# Notícias e variações de preço
noticias = {
    "TechBrasil": [
        ("Parceria com governo para IA nas escolas", 0.27),
        ("Vazamento de dados de usuários", -0.22)
    ],
    "AgroVale": [
        ("Exportações de soja batem recorde", 0.32),
        ("Crise hídrica afeta colheita", -0.28)
    ],
    "PetroMax": [
        ("Alta no petróleo impulsiona lucros", 0.21),
        ("Explosão interrompe produção offshore", -0.35)
    ],
    "EcoEnergia": [
        ("Contrato bilionário com Europa", 0.38),
        ("Corte de incentivos afeta setor", -0.19)
    ],
    "BancoReal": [
        ("Nova fintech com taxa zero", 0.24),
        ("Escândalo de corrupção no conselho", -0.26)
    ]
}

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<div class='bloco'>", unsafe_allow_html=True)
    nome = st.text_input("👤 Nome do participante:")
    acao = st.selectbox("🧾 Escolha uma ação:", list(acoes.keys()))
    valor = st.number_input("💰 Quanto deseja investir? (R$)", min_value=1.0)
    simular = st.button("🚀 Simular Investimento")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if simular and nome:
        nome_acao, preco_inicial = acoes[acao]
        noticia, variacao = random.choice(noticias[nome_acao])
        preco_final = preco_inicial * (1 + variacao)
        resultado = (valor / preco_inicial) * preco_final
        ganho = resultado - valor
        percentual = variacao * 100

        st.session_state.ranking.append((nome, ganho))

        st.markdown("<div class='bloco'>", unsafe_allow_html=True)
        st.subheader("📊 Resultado da Simulação")

        st.markdown(
            f"""
            <table>
            <tr><td><b>🟦 Ação:</b></td><td>{nome_acao}</td></tr>
            <tr><td><b>📰 Notícia:</b></td><td>{noticia}</td></tr>
            <tr><td><b>📌 Preço Inicial:</b></td><td>R$ {preco_inicial:.2f}</td></tr>
            <tr><td><b>🎯 Preço Final:</b></td><td style='color:{'lime' if variacao > 0 else 'red'};'>R$ {preco_final:.2f} ({'▲' if variacao > 0 else '▼'} {abs(percentual):.1f}%)</td></tr>
            <tr><td><b>💸 Valor Investido:</b></td><td>R$ {valor:.2f}</td></tr>
            <tr><td><b>📈 Valor Final:</b></td><td>R$ {resultado:.2f}</td></tr>
            </table>
            """,
            unsafe_allow_html=True
        )

        if resultado > valor:
            st.success("📗 Lucro! Sua estratégia deu certo!")
        else:
            st.error("📕 Prejuízo! O mercado não perdoou...")

        st.markdown("</div>", unsafe_allow_html=True)

        st.subheader("📉 Gráfico de Variação da Ação")
        fig, ax = plt.subplots()
        ax.plot([0, 1], [preco_inicial, preco_final], marker='o', linewidth=2,
                color='lime' if variacao > 0 else 'red')
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Antes da notícia", "Depois da notícia"])
        ax.set_ylabel("Preço (R$)")
        ax.set_title(f"📊 {nome_acao}")
        ax.grid(True)
        st.pyplot(fig)

# Separação do ranking
st.markdown("---")
st.subheader("🏆 Ranking dos Participantes")

ranking_ordenado = sorted(st.session_state.ranking, key=lambda x: x[1], reverse=True)
for i, (nome, lucro) in enumerate(ranking_ordenado[:5], 1):
    cor = "lime" if lucro >= 0 else "red"
    st.markdown(f"**{i}. {nome}** – <span style='color:{cor};'>R$ {lucro:.2f}</span>", unsafe_allow_html=True)

# Botão para jogar novamente
if st.button("🔄 Jogar Novamente"):
    st.session_state.clear()  # Limpar o estado da sessão para reiniciar o jogo
    st.experimental_rerun()
