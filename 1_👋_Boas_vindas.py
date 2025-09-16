import streamlit as st

# Configurando página
st.set_page_config(page_title='Easy GeoMax!', layout='wide', page_icon=':material/manufacturing:')

# Funções
@st.cache_data
def carregar_layout(): # Função para ajustar o layout (coisa de frontend, não importa)
    if arquivo is None:
        with st.container(horizontal_alignment='center'):
            
            st.title('Easy :green[GeoMax! :material/distance:]', width='content')
            for i in range(3):st.text('')
            st.subheader(':gray[:material/help: Uso]', width='content')    
            col1,col2,col3 = st.columns([0.2,.6,0.2])
        
            with col2:
                with st.container(horizontal_alignment='left'):
                    st.markdown(':gray[:material/info:] Site em manutenção, porém uso ainda liberado.', width='content')

            
            # Ajustes de CSS
            st.markdown("""
                        <style>
    
                        .st-emotion-cache-1fc0ges p {
                            margin-top: -19px;
                            }
                        
                        .st-emotion-cache-10p9htt {
                            height: 1rem;
                            margin-bottom: 10px;                            
                            }
                        
                        .st-emotion-cache-1s2v671 {
                            min-height: 0rem;
                        }
                        
                        </style>
                    """,
                    unsafe_allow_html=True)
