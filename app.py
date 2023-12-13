import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Função para comparar o rendimento dos títulos
def compare_yield(DI, IPCA, titulo_pre, titulo_cdi_percent, titulo_ipca_percent, titulo_di_plus):
    resultados = {
        'Pré': titulo_pre,
        'IPCA +': IPCA + titulo_ipca_percent,
        f'{titulo_cdi_percent}% do DI': (titulo_cdi_percent / 100) * DI,
        'DI +': DI + titulo_di_plus,
    }
    titulo_max_yield = max(resultados, key=resultados.get)
    max_yield = resultados[titulo_max_yield]
    return resultados, titulo_max_yield, max_yield

# Criação da interface de usuário no Streamlit
st.title("Comparador de Rendimento de Títulos de Renda Fixa")

with st.sidebar:
    st.header("Configurações de Cálculo")
    # Campos para entrada de dados na barra lateral
    DI = st.number_input("Taxa DI acumulada em 1 ano (%)", value=8.0, format="%.2f", step=0.01)
    IPCA = st.number_input("Taxa IPCA acumulada em 1 ano (%)", value=4.0, format="%.2f", step=0.01)
    titulo_pre = st.number_input("Taxa fixa do título 'Pré' (%)", value=11.5, format="%.2f", step=0.01)
    titulo_cdi_percent = st.number_input("Porcentagem do CDI do título (%)", value=120.0, format="%.2f", step=0.01)
    titulo_ipca_percent = st.number_input("Taxa fixa acima do IPCA do título (%)", value=7.0, format="%.2f", step=0.01)
    titulo_di_plus = st.number_input("Taxa fixa acima do DI do título (%)", value=1.0, format="%.2f", step=0.01)


# Cálculo automático quando qualquer input é alterado
resultados, titulo_max_yield, max_yield = compare_yield(DI, IPCA, titulo_pre, titulo_cdi_percent, titulo_ipca_percent, titulo_di_plus)

# Conversão dos resultados para um DataFrame para visualização
df_resultados = pd.DataFrame(list(resultados.items()), columns=['Título', 'Rendimento'])
df_resultados = df_resultados.sort_values('Rendimento', ascending=True)

# Criação de um gráfico de barras para visualizar os resultados
bar_chart = alt.Chart(df_resultados).mark_bar().encode(
    x='Rendimento',
    y=alt.Y('Título', sort='-x'),
    color=alt.condition(
        alt.datum.Título == titulo_max_yield,  # Se o título for o de máximo rendimento
        alt.value('orange'),     # destaque com a cor laranja
        alt.value('steelblue')   # senão, use a cor azul-aco
    )
).properties(
    title='Comparação de Rendimento dos Títulos'
)

st.altair_chart(bar_chart, use_container_width=True)
st.write(f"**O título com o maior rendimento é o '{titulo_max_yield}' com um rendimento de {max_yield}%.**")
