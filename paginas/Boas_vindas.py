import streamlit as st

# Configurando página
st.set_page_config(page_title='Easy GeoMax!', layout='wide', page_icon=':material/home:')


st.caption('Site em manutenção...')


@st.cache_data
def carregar_layout(): # Função para ajustar o layout (coisa de frontend, não importa)
    if arquivo is None:
        with st.container(horizontal_alignment='center'):
            
            st.title('Easy :green[GeoMax!]', width='content')
            st.caption('Aplicação web multifuncionalidade', width=370) 
            
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
