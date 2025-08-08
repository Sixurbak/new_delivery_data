

import streamlit as st
from PIL import Image

st.set_page_config(page_title="Home", page_icon=":house:", layout="wide")

st.sidebar.image("logo2.gif", width=200)




st.sidebar.markdown('# Cury Company' )
st.sidebar.markdown('## Fastest Delivery in Town' )
st.sidebar.markdown("""___""")

st.write("# Curry Company Growth Dashboard")

st.markdown(
    """
    <h2 style="text-align: center;">Como utilizar este Growth Dashboard?</h2>
    <ul>
        <li><b>Visão Empresa:</b>
            <ul>
                <li><b>Visão Gerencial:</b> Métricas gerais de comportamento.</li>
                <li><b>Visão Tática:</b> Indicadores semanais de crescimento.</li>
                <li><b>Visão Geográfica:</b> Insights de geolocalização.</li>
            </ul>
        </li>
        <li><b>Visão Entregador:</b>
            <ul>
                <li>Acompanhamento dos indicadores semanais de crescimento.</li>
            </ul>
        </li>
        <li><b>Visão Restaurante:</b>
            <ul>
                <li>Indicadores semanais de crescimento dos restaurantes.</li>
            </ul>
        </li>
    </ul>
    <hr>
    <h3 style="text-align: center;">Precisa de ajuda?</h3>
    <p style="text-align: center;">Entre em contato com o time de Data Science:<br>
    <code>Decio Carrilho</code></p>
    """,
    unsafe_allow_html=True
)