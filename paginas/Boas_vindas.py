import streamlit as st

# Configurando página
st.set_page_config(page_title='Easy GeoMax!', layout='wide', page_icon=':material/home:')

# Carregando layout
with st.container(horizontal_alignment='center'):
    st.title('Easy :green[GeoMax!]', width='content')
    st.caption('Aplicação web multifuncionalidade', width='content') 

col1,col2,col3,col4 = st.columns(4, border=True, vertical_alignment = 'center', width=450)

with col1:
    st.header('Easy :green[Geocoding :material/globe_location_pin:]')

with col2:
    st.header('Easy :blue[Reverse Geocoding :material/travel_explore:]')

with col3:
    st.header('Easy :violet[Routes :material/route:]')

with col4:
    st.header('Easy :red[Overture :material/south_america:]')

