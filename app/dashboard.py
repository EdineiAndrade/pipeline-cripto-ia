import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time
import os
from dotenv import load_dotenv
from psycopg2 import connect

# Configurações visuais do Streamlit
st.set_page_config(page_title="Painel Cripto", layout="wide", page_icon="💰")
st.markdown(
    """
    <style>
        body {
            background-color: #0e1117;
            color: #fafafa;
        }
        .stDataFrame thead tr th {
            background-color: #1c1e26;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Carregar variáveis de ambiente
load_dotenv()
DATABASE_URL = os.getenv('DB_URL')

def ler_dados():
    try:
        conn = connect(DATABASE_URL)
        query = "SELECT * FROM crypto_prices ORDER BY timestamp DESC LIMIT 50"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro ao ler os dados do banco de dados: {e}")
        return pd.DataFrame()
def mostrar_estatisticas(df):
    preco_atual = df.sort_values('timestamp', ascending=False).iloc[0]['valor']
    preco_maximo = df['valor'].max()
    preco_minimo = df['valor'].min()

    st.markdown("### 📊 Estatísticas Gerais")
    col1, col2, col3 = st.columns(3)

    col1.metric("Preço Atual", f"${preco_atual:,.2f}")
    col2.metric("Preço Máximo", f"${preco_maximo:,.2f}")
    col3.metric("Preço Mínimo", f"${preco_minimo:,.2f}")

def plotar_grafico(df):
    df = df.sort_values('timestamp')  # ordenar por tempo
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['valor'],
        mode='lines+markers',
        line=dict(color='cyan', width=2),
        marker=dict(size=6, color='lightblue'),
        name='BTC'
    ))
    fig.update_layout(
        template='plotly_dark',
        title='📈 Variação do Bitcoin (BTC/USD)',
        xaxis_title='Data e Hora',
        yaxis_title='Valor em USD',
        font=dict(color='white'),
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.title("💹 Painel de Monitoramento - Criptomoedas")
    df = ler_dados()

    if df.empty:
        st.warning("Nenhum dado disponível para plotar.")
        return

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Estatísticas gerais
    mostrar_estatisticas(df)

    # Gráfico principal
    plotar_grafico(df)

    # Últimos dados em tabela interativa
    st.subheader("📄 Últimos registros")
    st.dataframe(
        df[['timestamp', 'valor', 'cripto', 'moeda']].sort_values('timestamp', ascending=False),
        use_container_width=True,
        height=400
    )
    with st.empty():
        for i in range(60, 0, -1):
            st.caption(f"🔄 Atualizando em {i} segundos...")
            time.sleep(1)
        st.rerun()

if __name__ == "__main__":
    main()
