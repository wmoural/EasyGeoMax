import streamlit as st

# Configurando página
st.set_page_config(page_title='Easy GeoMax!', layout='wide', page_icon=':material/home:')

# Carregando layout
with st.container(horizontal_alignment='center'):
    st.title('Easy :green[GeoMax!]', width='content')
    st.caption('Aplicação web multifuncionalidade', width='content') 

col1,col2,col3,col4 = st.columns(4, border=True, vertical_alignment ='top')

with col1:
    col1.container(height=500, border=False)
    st.title('Easy :green[Geocoding :material/globe_location_pin:]', width='content')
    
with col2:
    col2.container(height=500, border=False)
    st.title('Easy :blue[Reverse Geocoding :material/travel_explore:]', width='content')

with col3:
    col3.container(height=500, border=False)
    st.title('Easy :violet[Routes :material/route:]', width='content')

with col4:
    col4.container(height=500, border=False)
    st.title('Easy :red[Overture :material/south_america:]', width='content')









