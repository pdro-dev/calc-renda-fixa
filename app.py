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

# Export results button
export_expander = st.expander('Exportar Resultados')
if export_expander.button('Exportar Resultados para CSV'):
    df_resultados.to_csv('rendimentos.csv', index=False)
    export_expander.success('Arquivo exportado com sucesso!')

# Calculation history
history_expander = st.expander('Histórico de Cálculos')
if 'historico_calculos' not in st.session_state:
    st.session_state['historico_calculos'] = []

# Add new calculations to history
st.session_state['historico_calculos'].append(resultados)

# Display the calculation history in a DataFrame
df_historico = pd.DataFrame(st.session_state['historico_calculos'])
# Add a column with the title of highest yield
df_historico['Título de Maior Rendimento'] = df_historico.idxmax(axis=1)
history_expander.write(df_historico)

# Clear calculation history
if history_expander.button('Limpar Histórico'):
    st.session_state['historico_calculos'] = []
    history_expander.success('Histórico de cálculos limpo com sucesso!')

# Export calculation history
if history_expander.button('Exportar Histórico'):
    df_historico.to_csv('historico.csv', index=False)
    history_expander.success('Histórico exportado com sucesso!')

# Feedback form
feedback_expander = st.expander('Feedback')
with feedback_expander.form("form_feedback"):
    feedback = st.text_area("Deixe seu feedback aqui:")
    submitted = st.form_submit_button("Enviar Feedback")
    if submitted:
        # Here you can process the feedback, such as saving it to a file or database
        feedback_expander.success("Obrigado pelo seu feedback!")