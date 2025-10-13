import googlemaps
import pandas as pd
import streamlit as st
from datetime import datetime
from shapely.geometry import LineString
import polyline
import geopandas as gpd
import leafmap.foliumap as leafmap
import time
import io
from estilos_css import uploader, uploader_depois

# Limpando cache
st.cache_data.clear()

# Configurando página
st.set_page_config(page_title='Easy Directions', layout='wide', page_icon=':material/route:')

# Funções
@st.cache_data
def carregar_layout(): # Função para ajustar o layout (coisa de frontend, não importa)
    if arquivo is None:
        with st.container(horizontal_alignment='center'):
            
            st.title('Easy :violet[Routes :material/route:]', width='content')
            st.caption('Aplicação web para geração de rotas otimizadas', width=310)
            for i in range(3):st.text('')
            st.subheader(':gray[:material/help: Uso]', width='content')    
            col1,col2,col3 = st.columns([0.2,.6,0.2])
        
            with col2:
                with st.container(horizontal_alignment='left'):
                    st.markdown(':gray[:material/counter_1:] Faça o upload do seu arquivo', width='content')
                    st.markdown(':gray[:material/counter_2:] Forneça uma chave API', width='content')
                    st.markdown(':gray[:material/counter_3:] Defina a coluna em que estão os endereços/coordenadas de origem, destino e o modo de transporte', width='content')
                    st.markdown(':gray[:material/counter_4:] Visualize e baixe os resultados', width='content')
            
            # Ajustes de CSS
            st.markdown(uploader(), unsafe_allow_html=True)
     
    else:
        with st.container(horizontal_alignment='center'):
            st.title('Easy :violet[Routes :material/route:]', width='content')
            st.caption('Aplicação web para geração de rotas otimizadas', width=310)
            st.divider()
            
            # Ajustes de CSS
            #css = uploader_depois(arquivo.name)
            #if css:
            #    st.markdown(css, unsafe_allow_html=True)

# Função para calculo de matriz
def Rotear(df = pd.DataFrame, Chave = str) -> pd.DataFrame():
    
    # Inputs
    df_rota = df
    
    # Conectando ao client googlemaps
    gmaps = googlemaps.Client(key=chave)
    
    # Criando novas colunas a serem preenchidas
    lista_origem, lista_latlong_origem, lista_destino, lista_latlong_destino, lista_tempo, lista_dist, lista_rotas = [],[],[],[],[],[],[]
    i = 1
    progress_bar = st.progress(0)
    
    # Loops
    for origem,destino,modo in zip(df_rota[ColunaOrigem], df_rota[ColunaDestino], df_rota[ColunaModo]):
        

        if modo == 'bus':
            geocode = gmaps.directions(origem, destino, mode='transit', transit_mode='bus')
            
        else:
            geocode = gmaps.directions(origem, destino, mode=modo)
            
        if len(geocode)>0:
            
            geocode = geocode[0]['legs'][0]

            lista_origem.append(geocode['start_address'])
            lista_latlong_origem.append(geocode['start_location'])
            lista_destino.append(geocode['end_address'])
            lista_latlong_destino.append(geocode['end_location'])
            lista_tempo.append(geocode['duration']['value'])
            lista_dist.append(geocode['distance']['value'])
            
            for rota in geocode['steps']:
                
                rota.update({'Origem':origem, 'Destino':destino})

            lista_rotas.append(geocode['steps'])
        
        else:
            
            lista_origem.append('Não encontrado')
            lista_latlong_origem.append('Não encontrado')
            lista_destino.append('Não encontrado')
            lista_latlong_destino.append('Não encontrado')
            lista_tempo.append('Não encontrado')
            lista_dist.append('Não encontrado')
        
        # Atualizando progress bar
        progress_bar.progress(i/len(df_rota), text=f":material/hourglass_empty: Gerando rotas...: {i*10}% realizados...")  
        i += 1
    
    # Atualizando progress bar
    progress_bar.progress(100, text=":green[:material/done_all: **100% das rotas geradas**]")
    time.sleep(1)
    
    # Criando novas colunas a serem preenchidas
    df_rota['Origem_Formatada'] = lista_origem
    df_rota['LatLong_Origem'] = lista_latlong_origem
    df_rota['Destino_Formatado'] = lista_destino
    df_rota['LatLong_Destino'] = lista_latlong_destino
    df_rota['Tempo [s]'] = lista_tempo
    df_rota['Distância [m]'] = lista_dist
    
    return (df_rota, lista_rotas)

# Função para criar as rotas (GPT)
def DesenharRotas(rotas):

    rotas_totais = []

    # Loop through the list of routes
    for route in rotas:
        # For each route, loop through its legs
        for caminho in route:
            # Decode the polyline for each leg
            coordinates = polyline.decode(caminho['polyline']['points'])
            
            # Create LineString geometry from the decoded coordinates
            line_geometry = LineString([(lng, lat) for lat, lng in coordinates])
            
            # Append the route data with geometry into the list
            rotas_totais.append({
                'distancia': caminho['distance']['value'],
                'duracao': caminho['duration']['value'],
                'modo': caminho['travel_mode'],
                'origem': caminho['Origem'],
                'destino': caminho['Destino'],
                'geometry': line_geometry
            })
    
    # Convert the list of geometries into a GeoDataFrame
    gdf = gpd.GeoDataFrame(rotas_totais, crs="EPSG:4326") 
    
    return gdf

# Variáveis no cache
if 'Resultado' not in st.session_state:
    st.session_state.Resultado = None
    
if 'Rotas' not in st.session_state:
    st.session_state.Rotas = None

# Sidebar
with st.sidebar:
    
    with st.expander('**Informações importantes**', expanded=False, icon=':material/info:'):
        st.info("""
                Use os seguintes valores para indicar o modo de transporte:
                - driving (para carros e motos)
                - bicycling (para bicicleta)
                - walking (para a pé)
                - bus (para ônibus)
                """)
               
    # Botão para subir planilha excel
    arquivo = st.file_uploader(':blue[:material/upload_file: Faça o upload da planilha excel]', type=['xlsx'])
    st.text('')
    if arquivo is not None:
        chave = st.text_input(':blue[:material/key_vertical: Insira aqui sua chave API:]', type='password')

# Carregando layout
carregar_layout()
   
# Botões para a execução dos processos
if arquivo is not None:

    # Transformando o arquivo carregado em DataFrame
    df = pd.read_excel(arquivo, engine='openpyxl')
    
     # Parametrizando o container de inputs
    container_inputs = st.container(border=False, 
                                    horizontal=True,
                                    vertical_alignment='center',
                                    horizontal_alignment='center'
                                    )
    
    # Formulário de processamento
    with st.form('Form rodar matriz', width='stretch', border=False):
        
        # Chamando container de inputs
        with container_inputs:
            
            ColunaOrigem = st.selectbox('', 
                                        df.columns,
                                        index=None,
                                        placeholder='Defina a coluna com as origens')
            
            ColunaDestino = st.selectbox('', 
                                        df.columns,
                                        index=None,
                                        placeholder='Defina a coluna com os destinos')
            
            ColunaModo = st.selectbox('',
                                      df.columns,
                                      index=None,
                                      placeholder='Defina a coluna com os modos')
            
        # Centralizando botão de executar roteamento
        c1,c2,c3 = st.columns([.3,.4,.3])
        
        with c2:
            
            # Botão de submit
            rodar = st.form_submit_button('Rotear', width='stretch', icon=':material/route:', type='primary')
            
            # Uso do botão
            if rodar:
                
                with st.progress(0, "Gerando rotas...") as progress_bar:
                    st.session_state.Resultado, rotas = Rotear(df, chave)
                    st.session_state.Rotas = DesenharRotas(rotas)
                st.balloons()
                time.sleep(2)
                st.rerun()

    # Parametrizando o container de outputs
    container_outputs = st.container(border=False,
                                     horizontal=False,
                                     horizontal_alignment='center',
                                     vertical_alignment='bottom')
    
    # Plotando mapa de resultados
    if st.session_state.Resultado is not None and arquivo is not None:
        
        with container_outputs:
            
            # Criando instância de mapa
            m = leafmap.Map()
            m.add_gdf(st.session_state.Rotas, layer_name='Roteamento')
            
            # Plotando mapa de resultados
            m.to_streamlit(responsive=True, scrolling=True, height=450)

    
# Inserindo botões de download dos resultados
    if st.session_state.Resultado is not None and arquivo is not None:
               
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            st.session_state.Resultado.to_excel(writer, sheet_name='Resultado', index=False)
            st.session_state.Rotas.to_excel(writer, sheet_name='Rotas', index=False)
        buffer.seek(0)
                
        container_downloads = st.container(border=False,
                                           horizontal=False,
                                           horizontal_alignment='center',
                                           vertical_alignment='center')
        
        with container_downloads:
    
            st.download_button(
                "Baixe em Excel",
                buffer,
                f"Dados de roterização - {datetime.now()}.xlsx",
                "application/vnd.ms-excel",
                key='download-xlsx',
                on_click='rerun',
                type='primary',
                width=500,
                icon=':material/download_for_offline:'
                )










