import googlemaps
import pandas as pd
import streamlit as st
import xlsxwriter
from io import BytesIO
import io
import geocoder
from datetime import datetime

# Limpando cache
st.cache_data.clear()

# Configurando página
st.set_page_config(page_title='Easy Reverse-Geocoding', layout='wide', page_icon='🧭')

# Título
st.title("**Easy** :orange[Reverse-Geocoding] :compass:")   

# Declarando session state
if 'DemandaReversaGerada' not in st.session_state:
    st.session_state.DemandaReversaGerada = None

with st.sidebar:
    
    with st.expander('**Informações importantes**', icon='ℹ️', expanded=False):
        st.info("""
                As coordenadas deverão:
                - estar em uma única coluna
                - serem separadas por ","
                - possuírem "." como separador decimal \n
                ex.: [-3.72026, -38.51144]
                """)
        
    chave = st.text_input('Insira aqui sua chave API:', type='password')
 
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
    
    with st.expander('**Pague-me um café:**', icon='☕', expanded=False):
        pix = 'https://i.imgur.com/LLr5WY8.jpg'
        st.image(pix, use_column_width='True', caption='PIX')
    
# Funções para colunas
def ReverseGeocodeDemanda(df, Chave):

    # Inserindo API KEY
    gmaps = googlemaps.Client(key=chave)

    # Gerando listas
    endereco_formatado = []
    provedor = []
    
    # Geocodificando endereços
    for i in range(len(df)):
        
        geocode_reverso = gmaps.reverse_geocode(df[LatLong].loc[i], location_type='RANGE_INTERPOLATED')
        
        if len(geocode_reverso) == 0:
        
            geocode_reverso = geocoder.arcgis(df[LatLong].loc[i], method='reverse').json
            
            if geocode_reverso is not None:
                
                endereco_formatado.append(geocode_reverso['address'])
                provedor.append('ArcGIS')
            
        else:
            
            geocode_reverso = geocode_reverso[0]['formatted_address']
            endereco_formatado.append(geocode_reverso)
            provedor.append('Google')
            
        status.update(label=f'{i+1} de {tamanho}')

    # Criando novas colunas e colando resultados
    df['resultado_Endereço'] = endereco_formatado
    df['resultado_Provedor'] = provedor
    
    return df

# Botão para subir planilha excel
ArquivoCarregado = st.file_uploader('**Faça o upload da planilha aqui** :call_me_hand:', type=['xlsx'])

if ArquivoCarregado is not None:

    # Transformando o arquivo carregado em DataFrame
    df = pd.read_excel(ArquivoCarregado, engine='openpyxl')

    tamanho = len(df)
   
    # Colunas
    col1, col2 = st.columns([4, 5])

    # Criando botões de input
    with col1:

        with st.form("Inputs"):

            LatLong = st.selectbox("Selecione a coluna com o endereço", list(df.columns.values))

            # Botão pra rodar o geocode
            rodar = st.form_submit_button("Geocodificar", use_container_width=True, icon='✌')
                       
            if rodar:
                
                with st.status('Geocodificando...', expanded=True) as status:
                    
                    if chave == None:
                        
                        st.warning('Insira sua API KEY')
                                            
                    else:
                        
                        st.session_state.DemandaReversaGerada = ReverseGeocodeDemanda(df, chave)
                        
                        if st.session_state.DemandaGerada is not None:
                            
                            buffer = io.BytesIO()
                            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                                st.session_state.DemandaReversaGerada.to_excel(writer, sheet_name='Sheet1')
                                writer.close()
                                        
                        st.balloons()
                        status.update(label='Reverse geocode concluído', state='complete')
                        st.toast('Se o easygeomax foi útil, valorize-me: pague-me um café!', icon='🥳')
        
        cl1,cl2,cl3 = st.columns([1,3,1])
        
        with cl2:
            
            if st.session_state.DemandaReversaGerada is not None and ArquivoCarregado is not None:
            
                with st.status('Gerando CSV...') as status2:
                    
                    st.download_button(
                        "Baixe em CSV",
                        st.session_state.DemandaReversaGerada.to_csv(),
                        f"Geocoding-Reverso-{datetime.now()}.csv",
                        "text/csv",
                        key='download-csv',
                        use_container_width=True,
                        icon='✅')
                    
                    status2.update(label='**CSV Gerado!**', state='complete', expanded=True)
    
    with col2:
        
        with st.expander('Resultado: '):
            
            if st.session_state.DemandaReversaGerada is not None:
                
                st.dataframe(st.session_state.DemandaReversaGerada, use_container_width=True)
