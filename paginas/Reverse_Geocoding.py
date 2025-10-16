import googlemaps
import pandas as pd
import streamlit as st
import io
import geocoder
from datetime import datetime
import time
from estilos_css import uploader, uploader_depois

# Limpando cache
st.cache_data.clear()

# Configurando página
st.set_page_config(page_title='Easy Reverse Geocoding', layout='wide', page_icon=':material/travel_explore:')

# Funções
@st.cache_data
def carregar_layout(): # Função para ajustar o layout (coisa de frontend, não importa)
    if arquivo is None:
        with st.container(horizontal_alignment='center'):
            
            st.title('Easy :blue[Reverse Geocoding :material/travel_explore:]', width='content')
            st.caption('Aplicação web para realização de geocoding de coordenadas', width=370)
            for i in range(3):st.text('')
            st.subheader(':gray[:material/help: Uso]', width='content')    
            col1,col2,col3 = st.columns([0.2,.6,0.2])
        
            with col2:
                with st.container(horizontal_alignment='left'):
                    st.markdown(':gray[:material/counter_1:] Faça o upload do seu arquivo', width='content')
                    st.markdown(':gray[:material/counter_2:] Forneça uma chave API caso queira geocodificar com Google (opção paga) ou deixe em branco para geocodificar com ArcGIS (opção gratuita)', width='content')
                    st.markdown(':gray[:material/counter_3:] Defina a coluna em que estão as coordenadas e geocodifique', width='content')
                    st.markdown(':gray[:material/counter_4:] Visualize e baixe os resultados', width='content')
            
        # Ajustes de CSS
        st.markdown(uploader(), unsafe_allow_html=True)
     
    else:
        with st.container(horizontal_alignment='center'):
            st.title('Easy :blue[Reverse Geocoding :material/travel_explore:]', width='content')
            st.caption('Aplicação web para realização de geocoding de coordenadas', width=370)
            st.markdown(
                """
                <hr style="margin:5px 0 0px 0;">
                """,
                unsafe_allow_html=True
            )
            
        # Ajustes de CSS
        st.markdown(uploader_depois(arquivo.name), unsafe_allow_html=True)

def Geocodificar(df = pd.DataFrame, Chave = str) -> pd.DataFrame():
    
    # Reduzindo tamando do dataframe
    df_reduzido = df[[ColunaCoordenadas]].drop_duplicates().reset_index(drop=True)
    
    # Gerando listas
    lat, lon, endereco_formatado, provedor = [],[],[],[]
    i = 1
    
    progress_bar = st.progress(0)
    
    # Checagem de chave para definir qual método de geocode
    # Se Chave estiver preenchida, então geocodifica com gmaps
    if Chave != '':
        
        gmaps = googlemaps.Client(key=Chave)
    
        for coordenada in df_reduzido[ColunaCoordenadas]:
            
            # Realizando geocoding através da biblioteca do google
            geocode = gmaps.reverse_geocode(coordenada, location_type='RANGE_INTERPOLATED')
            
            # Checa se o resultado é maior que zero, caso seja, salva os dados, caso não seja, 
            # tenta novamente usando o provedor arcgis com a bibilioteca geocoder
            if len(geocode) == 0:
            
                geocode = geocoder.arcgis(coordenada, method='reverse').json
                
                if geocode is not None:
                
                    endereco_formatado.append(geocode['address'])
                    provedor.append('ArcGIS')
                    
                else:
                    
                    endereco_formatado.append('0')
                    provedor.append('0')                                        
                    
            else:
                
                geocode = geocode[0]['formatted_address']
                endereco_formatado.append(geocode)
                provedor.append('Google')
                    
            progress_bar.progress(i/len(df_reduzido), text=f":material/hourglass_empty: Geocodificando: {i*10}% realizados...")  
            i += 1

    # Se Chave estiver vazia, então geocodifica tudo com ArcGis
    else:
    
        for coordenada in df_reduzido[ColunaCoordenadas]:

            geocode = geocoder.arcgis(coordenada, method='reverse').json
            
            if geocode is not None:
            
                endereco_formatado.append(geocode['address'])
                provedor.append('ArcGIS')
                
            else:
                
                lat.append('0')
                lon.append('0')
                endereco_formatado.append('0')
                provedor.append('0')

            progress_bar.progress(i/len(df_reduzido), text=f":material/hourglass_empty: Geocodificando: {i*10}% realizados...")                    
            i += 1
            
    # Atualizando progress bar
    progress_bar.progress(100, text=":green[:material/done_all: **100% das coordenadas geocodificados**]")
    time.sleep(1)
    
    # Salvando resultados obtidos
    df_reduzido['Endereço Geocodificado'] = endereco_formatado
    df_reduzido['Provedor'] = provedor
    
    df = pd.merge(df, df_reduzido, on=ColunaCoordenadas)
        
    return df

# Variváveis no cache
if 'Resultado' not in st.session_state:
    st.session_state.Resultado = None

# Sidebar
with st.sidebar: 
           
    # Botão para subir planilha excel
    arquivo = st.file_uploader(':blue[:material/upload_file: Faça o upload da planilha excel]', type=['xlsx'])
    st.text('')
    if arquivo is not None:
        chave = st.text_input(':blue[:material/key_vertical: Insira aqui sua chave API:]', type='password')
        for i in range(2):st.text('')
        
# Carregando layout
carregar_layout()

# Botões para a execução dos processos
if arquivo is not None:

    # Transformando o arquivo carregado em DataFrame
    df = pd.read_excel(arquivo, engine='openpyxl')
        
    # Parametrizando o container de inputs
    container_inputs = st.container(border=False, 
                                    horizontal=False,
                                    vertical_alignment='center',
                                    horizontal_alignment='center'
                                    )
    
    # Chamando container de inputs
    with container_inputs:
        
        # Dentro do container de inputs, chamando formulários
        with st.form("Inputs", border=False, width=400):
            
            # Dentro do formulário, definindo parâmetros da caixa de seleção de coluna para geocode
            ColunaCoordenadas = st.selectbox("",
                                          list(df.columns.values),
                                          width='stretch',
                                          index=None,
                                          placeholder='Defina a coluna com as coordenadas')

            # Definindo parâmetros do botão
            rodar = st.form_submit_button("Geocodificar",
                                          width='stretch',
                                          type='primary',
                                          icon=':material/explore_nearby:'
                                          )
            # Uso do botão para geocodificar
            if rodar:
                
                # Chamando barra de progresso
                with st.progress(0, "Geocodificando suass coordenadas...") as progress_bar:
                    st.session_state.Resultado = Geocodificar(df, chave)
                st.balloons()
                time.sleep(2)
                st.rerun()
                    
    # Parametrizando o container de outputs
    container_outputs = st.container(border=False,
                                     horizontal=False,
                                     horizontal_alignment='center',
                                     vertical_alignment='bottom')
    
    # Plotando mapa de resultados
    with container_outputs:
        
        if st.session_state.Resultado is not None:
            coords = st.session_state.Resultado[ColunaCoordenadas].str.split(',', expand=True).astype(float)
            st.map(coords.rename(columns={0:'lat', 1:'lon'}),color='#006480')

        # Inserindo botão de download dos resultados
    if st.session_state.Resultado is not None and arquivo is not None:
           
        buffer = io.BytesIO()
        st.session_state.Resultado.to_excel(buffer, index=False)
        buffer.seek(0)
        
        container_downloads = st.container(border=False,
                                           horizontal=False,
                                           horizontal_alignment='center',
                                           vertical_alignment='center')
        
        with container_downloads:  
            
            st.download_button(
                "Baixe em Excel",
                buffer,
                f"Dados reversamente geocodificados - {datetime.now()}.xlsx",
                "application/vnd.ms-excel",
                key='download-xlsx',
                on_click='rerun',
                type='primary',
                width=500,
                icon=':material/download_for_offline:'
                )
