import streamlit as st

# Função para calcular o PU de um título de renda fixa
def calcular_pu(vn, taxa_juros, n):
    pu = vn / ((1 + taxa_juros/100)**n)
    return pu

def show_renda_fixa():
    st.header("Cálculo de Renda Fixa")

    # Create three columns
    col1, col2, col3 = st.columns(3)

    # Inputs for the PU calculation
    vn = col1.number_input("Valor Nominal (VN)", value=1000.00)
    taxa_juros = col2.number_input("Taxa de Juros a.a. (%)", value=10.00)
    n = col3.number_input("Número de Períodos (n)", value=1)

    # Botão para realizar o cálculo
    if st.button("Calcular Preço Unitário (PU)"):
        pu = calcular_pu(vn, taxa_juros, n)
        st.write(f"O Preço Unitário (PU) do título é: R$ {pu:.2f}")