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
st.set_page_config(page_title='Easy Geocoding', layout='wide', page_icon='🗺️')

# Título
st.title("**Easy** :green[Geocoding] :world_map:")   

# Declarando session state
if 'DemandaGerada' not in st.session_state:
    st.session_state.DemandaGerada = None

with st.sidebar:
    
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
def GeocodeDemanda(df, Chave):

    # Inserindo API KEY
    gmaps = googlemaps.Client(key=Chave)

    # Gerando listas
    lat = []
    lon = []
    endereço_formatado = []
    provedor = []
    
    # Geocodificando endereços
    for i in range(len(df)):
        
        geocode = gmaps.geocode(df[ColunaEndereço].loc[i], region="br", language="PT-BR")
        
        if len(geocode) == 0:
        
            geocode = geocoder.arcgis(df[ColunaEndereço].loc[i]).json
            
            if geocode is not None:
            
                endereço_formatado.append(geocode['address'])
                lat.append(geocode['lat'])
                lon.append(geocode['lng'])
                provedor.append('ArcGIS')
                
            else:
                
                lat.append('0')
                lon.append('0')
                endereço_formatado.append('0')
                provedor.append('0')
                
        else:
            
            resultado = geocode[0]
            lat.append(resultado['geometry']['location']['lat'])
            lon.append(resultado['geometry']['location']['lng'])
            endereço_formatado.append(resultado['formatted_address'])
            provedor.append('Google')
        
        status.update(label=f'{i+1} de {tamanho}')
        
    # Criando novas colunas e colando resultados
    df['Lat'] = lat
    df['Long'] = lon
    df['Endereço'] = endereço_formatado
    df['Provedor'] = provedor
    
    return df

def GeocodeDemandaFree(df):

    # Gerando listas
    lat = []
    lon = []
    endereço_formatado = []
    provedor = []
    
    # Geocodificando endereços
    for i in range(len(df)):

        geocode = geocoder.osm(df[ColunaEndereço].loc[i]).json
        
        if geocode is not None:
            
            endereço_formatado.append(geocode['address'])
            lat.append(geocode['lat'])
            lon.append(geocode['lng'])
            provedor.append('OSM')

        else:
            
            geocode = geocoder.arcgis(df[ColunaEndereço].loc[i]).json
            
            if geocode is not None:
            
                endereço_formatado.append(geocode['address'])
                lat.append(geocode['lat'])
                lon.append(geocode['lng'])
                provedor.append('ArcGIS')
                
            else:
                
                lat.append('0')
                lon.append('0')
                endereço_formatado.append('0')
                provedor.append('0')
            
        status.update(label=f'{i+1} de {tamanho}')
            
    # Criando novas colunas e colando resultados
    df['Lat'] = lat
    df['Long'] = lon
    df['Endereço'] = endereço_formatado
    df['Provedor'] = provedor

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

            ColunaEndereço = st.selectbox("Selecione a coluna com o endereço", list(df.columns.values))

            # Botão pra rodar o geocode
            rodar = st.form_submit_button("Geocodificar", use_container_width=True, icon='✌')
                       
            if rodar:
                
                with st.status('Geocodificando...', expanded=True) as status:
                    
                    if chave != '':
                        
                        st.session_state.DemandaGerada = GeocodeDemanda(df, chave)
                        
                        if st.session_state.DemandaGerada is not None:
                            
                            buffer = io.BytesIO()
                            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                                st.session_state.DemandaGerada.to_excel(writer, sheet_name='Sheet1')
                                writer.close()
                    
                    else:
                        
                        st.session_state.DemandaGerada = GeocodeDemandaFree(df)
                
                st.balloons()
                status.update(label='Geocode concluído', state='complete')
                st.toast('Se o easygeomax foi útil, valorize-me: pague-me um café!', icon='🥳')
        
        cl1,cl2,cl3 = st.columns([1,3,1])
        
        with cl2:
            
            if st.session_state.DemandaGerada is not None and ArquivoCarregado is not None:
            
                with st.status('Gerando CSV...') as status2:
                    
                    st.download_button(
                        "Baixe em CSV",
                        st.session_state.DemandaGerada.to_csv(),
                        f"Geocoding-{datetime.now()}.csv",
                        "text/csv",
                        key='download-csv',
                        use_container_width=True,
                        icon='✅')
                    
                    status2.update(label='**CSV Gerado!**', state='complete', expanded=True)
    
    with col2:
        
        if st.session_state.DemandaGerada is not None:

            st.map(st.session_state.DemandaGerada.rename(columns={'Lat':'lat', 'Long':'lon'}),color='#006480')
            
    
with st.expander('Resultado: '):
    
    if st.session_state.DemandaGerada is not None:
        
        st.dataframe(st.session_state.DemandaGerada, use_container_width=True)
