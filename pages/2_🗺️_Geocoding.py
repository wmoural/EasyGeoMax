import googlemaps
import pandas as pd
import streamlit as st
import io
import geocoder
from datetime import datetime
import time

# Limpando cache
st.cache_data.clear()

# Configurando página
st.set_page_config(page_title='Easy Geocoding', layout='wide', page_icon=':material/globe_location_pin:')

# Funções
@st.cache_data
def carregar_layout(): # Função para ajustar o layout (coisa de frontend, não importa)
    if arquivo is None:
        with st.container(horizontal_alignment='center'):
            
            st.title('Easy :green[Geocoding :material/globe_location_pin:]', width='content')
            st.caption('Aplicação web para realização de geocoding de endereços', width=370)
            for i in range(3):st.text('')
            st.subheader(':gray[:material/help: Uso]', width='content')    
            col1,col2,col3 = st.columns([0.2,.6,0.2])
        
            with col2:
                with st.container(horizontal_alignment='left'):
                    st.markdown(':gray[:material/counter_1:] Faça o upload do seu arquivo', width='content')
                    st.markdown(':gray[:material/counter_2:] Forneça uma chave API caso queira geocodificar com Google (opção paga) ou deixe em branco para geocodificar com ArcGIS (opção gratuita)', width='content')
                    st.markdown(':gray[:material/counter_3:] Defina a coluna em que estão os endereços e geocodifique', width='content')
                    st.markdown(':gray[:material/counter_4:] Visualize e baixe os resultados', width='content')
            
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
     
    else:
        with st.container(horizontal_alignment='center'):
            st.title('Easy :green[Geocoding :material/globe_location_pin:]', width='content')
            st.caption('Aplicação web para realização de geocoding de endereços', width=370)
            st.divider()
            
            # Ajustes de CSS
            st.markdown("""
                        <style>
                        .st-emotion-cache-zy6yx3 {
                            padding: 2rem;                        
                            }
    
                        .st-emotion-cache-1fc0ges p {
                            margin-top: -2px;
                            }
                        
                        .st-emotion-cache-rv01uy { 
                            margin-top: -1rem;
                            margin-bottom: -1rem;
                            }
                        
                        .st-em {
                            background-color: #62D292;
                            }
                        
                        .st-emotion-cache-14xp4b3 {
                            margin-top: -2rem;
                            }
                        
                        .st-emotion-cache-1s2v671 {
                            min-height: 0rem;
                        }
                        
                        </style>
                    """,
                    unsafe_allow_html=True)

def Geocodificar(df = pd.DataFrame, Chave = str) -> pd.DataFrame():
    
    # Reduzindo tamando do dataframe
    df_reduzido = df[[ColunaEndereco]].drop_duplicates().reset_index(drop=True)
    
    # Gerando listas
    lat, lon, endereço_formatado, provedor = [],[],[],[]
    i = 1
    
    progress_bar = st.progress(0)
    
    # Checagem de chave para definir qual método de geocode
    # Se Chave estiver preenchida, então geocodifica com gmaps
    if Chave != '':
        
        gmaps = googlemaps.Client(key=Chave)
    
        for endereco in df_reduzido[ColunaEndereco]:
            
            # Realizando geocoding através da biblioteca do google
            geocode = gmaps.geocode(endereco, region="br", language="PT-BR")
            
            # Checa se o resultado é maior que zero, caso seja, salva os dados, caso não seja, 
            # tenta novamente usando o provedor arcgis com a bibilioteca geocoder
            if len(geocode) == 0:
            
                geocode = geocoder.arcgis(endereco).json
                
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
                    
            progress_bar.progress(i/len(df_reduzido), text=f":material/hourglass_empty: Geocodificando: {i*10}% realizados...")  
            i += 1

    # Se Chave estiver vazia, então geocodifica tudo com ArcGis
    else:
    
        for endereco in df_reduzido[ColunaEndereco]:

            geocode = geocoder.arcgis(endereco).json
            
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

            progress_bar.progress(i/len(df_reduzido), text=f":material/hourglass_empty: Geocodificando: {i*10}% realizados...")                    
            i += 1
            
    # Atualizando progress bar
    progress_bar.progress(100, text=":green[:material/done_all: **100% dos endereços geocodificados**]")
    time.sleep(1)
    
    # Salvando resultados obtidos
    df_reduzido['Latitude'] = lat
    df_reduzido['Longitude'] = lon
    df_reduzido['Endereço Geocodificado'] = endereço_formatado
    df_reduzido['Provedor'] = provedor
    
    df = pd.merge(df, df_reduzido, on=ColunaEndereco)
        
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
            ColunaEndereco = st.selectbox("",
                                          list(df.columns.values),
                                          width='stretch',
                                          index=None,
                                          placeholder='Defina a coluna com os endereços')

            # Definindo parâmetros do botão
            rodar = st.form_submit_button("Geocodificar",
                                          width='stretch',
                                          type='primary',
                                          icon=':material/explore_nearby:'
                                          )
            # Uso do botão para geocodificar
            if rodar:
                
                # Chamando barra de progresso
                with st.progress(0, "Geocodificando seus endereços...") as progress_bar:
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
        
            st.map(st.session_state.Resultado.rename(columns={'Latitude':'lat', 'Longitude':'lon'}),color='#006480')

        # Inserindo botão de download dos resultados
    if st.session_state.Resultado is not None and arquivo is not None:
           
        buffer = io.BytesIO()
        st.session_state.Resultado.to_excel(buffer, index=False)
        buffer.seek(0)
        
        coluna1,coluna2,coluna3 = st.columns([.2,.6,.2])
        
        with coluna2:
            with st.container(horizontal_alignment='center'):
                                        
                st.download_button(
                    "Baixe em Excel",
                    buffer,
                    f"Dados geocodificados - {datetime.now()}.xlsx",
                    "application/vnd.ms-excel",
                    key='download-xlsx',
                    on_click='rerun',
                    type='primary',
                    width='stretch',
                    icon=':material/download_for_offline:'
                    )
