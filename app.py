import streamlit as st
from mod_comparador import show_comparador
from mod_renda_fixa import show_renda_fixa

# Sidebar para alternar entre modos
modo = st.sidebar.radio("Selecione o Modo", ('Comparador de Rendimento', 'Cálculo de Renda Fixa'))

if modo == 'Comparador de Rendimento':
    show_comparador()
elif modo == 'Cálculo de Renda Fixa':
    show_renda_fixa()
