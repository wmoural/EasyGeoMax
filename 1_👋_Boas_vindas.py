import streamlit as st

# Configurando página
st.set_page_config(page_title='Easy GeoMax!')
    
with st.sidebar:
    with st.expander('**Dados do autor:** ', expanded=True):
    
        with st.container():
            sidebarcol1, sidebarcol2 = st.columns([2, 1])
            with sidebarcol1:
                imagem = 'https://i.imgur.com/Xe9O2MX.png'
                st.image(imagem, use_column_width=True, caption='Wellington Moura')
    
            with sidebarcol2:
                st.header('')
                st.subheader('[Linkedin](https://www.linkedin.com/in/wellington-moura-27497a1b3/)')
                st.subheader('[Github](https://github.com/wmoural)')
    
    with st.expander('**Pague-me um café:**☕', expanded=False):
        pix = 'https://i.imgur.com/8Dgf5dm.jpg'
        st.image('pix, use_column_width=True', caption='PIX')
     

st.title(':blue[Boas vindas ] 👋')

with st.expander('**Sobre**', expanded=True):
    st.markdown("""
                Este é o EasyGeoMax! Uma aplicação desenvolvida para otimizar o processo de geocoding ([Geocoding API](https://developers.google.com/maps/documentation/geocoding/overview?hl=pt-br))
                , cálculo de matrizes de distância ([Directions API](https://developers.google.com/maps/documentation/directions/overview?hl=pt-br)) e aquisição de dados vetoriais ([Overture Maps](https://docs.overturemaps.org/getting-data/overturemaps-py/)).
                Para das ferramentas de geocoding e cálculo de matriz é necessário ter uma [API KEY](https://developers.google.com/maps/documentation/javascript/get-api-key?hl=pt) ativa.
                """)
with st.expander('**Uso**', expanded=True):

    st.markdown("""
                 - **:green[Easy Geocoding]**: insira sua API KEY -> faça o upload de uma planilha Excel (.xlsx) contendo a lista de endereços que deseja geocodificar -> 
                indique a coluna alvo -> clique em "Geocodificar".
                
                 - **:green[Easy Directions]**: insira sua API KEY -> faça o upload de uma planilha Excel (.xlsx) contendo a lista de endereços ou (LATLONGs) de origem e 
                 destino e o modo de transporte correspondente -> indique as colunas alvos -> clique em "Calcular".

                 - **:green[Easy OvertureData]**: faça o upload de um polígono não vazio em formato geopackage -> defina o tipo de dado desejado -> clique em "Filtrar!".
                 """)

    st.info('Para Easy Directions, a formatação de LATLONGs deve seguir o exemplo: "-3.71917,-38.51226"')  
  
with st.expander('**Notas**', expanded=True):

    st.markdown("""
                Caso seja identificado algum problema durante o uso da aplicação ou caso deseje contribuir para o 
                aprimoramento do código com ideias, por favor entre em contato!
                 
                 """)
  
st.markdown("""
            <style>
                .st-emotion-cache-10trblm {
                
                    margin-left: calc(17rem)
                    
                }
            </style>
            
            """, unsafe_allow_html=True)
