import streamlit as st

# Configurando página
st.set_page_config(page_title='Easy GeoMax!', layout='wide', page_icon=':material/home:')

# Carregando layout
with st.container(horizontal_alignment='center'):
    st.title('Easy :green[GeoMax!]', width='content')
    st.caption('Aplicação web multifuncionalidade', width='content') 

with st.container(horizontal_aligment='center'):
    col1,col2,col3,col4 = st.columns([0.25, 0.25, 0.25, 0.25])
    with col1:
        'TESTE'



