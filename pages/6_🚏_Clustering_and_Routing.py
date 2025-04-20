import googlemaps
import pandas as pd
import geopandas as gpd
import leafmap.foliumap as leafmap
from sklearn_extra.cluster import KMedoids
import streamlit as st
import io
from itertools import chain
import polyline
from shapely.geometry import LineString
import random
import folium

# Clusterizando a partir de uma matriz de distâncias
@st.cache_data
def clusterizar(dataframe, clusters):
    
    modelo = KMedoids(n_clusters=clusters, metric='precomputed', method='pam', random_state=0)
    resultado = modelo.fit_predict(dataframe)
    labels = modelo.labels_
    res = pd.DataFrame({
        'ID': dataframe.index.tolist(),
        'Cluster': labels
    })
    
    return res

# Gerando roteirização partindo de um ponto distante em direção ao local fixo
@st.cache_data
def rotear_vindo(otimizar):
    
    # Inserindo API KEY
    gmaps = googlemaps.Client(key=chave)
    
    # Gerando lista para guardar resultados finais
    rotas_totais = [] 
    
    for cluster in arquivo_roteirizacao[coluna_cluster].drop_duplicates():
        
        # classificando valores
        df_filtrado = arquivo_roteirizacao[arquivo_roteirizacao[coluna_cluster] == cluster].reset_index().drop(columns=['index'])
        df_filtrado = df_filtrado.sort_values(by=coluna_distancia, ascending=False).reset_index().drop(columns=['index'])
        

        # pegando distancias
        geocode = gmaps.directions(df_filtrado.loc[0, coluna_coordenadas],
                                   local_fixo,
                                   waypoints=df_filtrado[coluna_coordenadas].tolist()[1:],
                                   optimize_waypoints=otimizar,
                                   mode='driving',
                                   alternatives=False)
          
        # ordenar waypoints
        ordem_waypoints = geocode[0]['waypoint_order']

        # pegando rotas
        geocode = geocode[0]['legs']
        
        coords = []
        
        for i in range(len(geocode)):
            
            for ii in range(len(geocode[i]['steps'])):
                           
                coords.append(polyline.decode(geocode[i]['steps'][ii]['polyline']['points']))
                
                # checando se a rota é muito pequena e gerando uma "pseudo-linha"
                if len(coords[0]) == 1:
                   
                    coords[0].append((coords[0][0][0],coords[0][0][1]))
    
            coords = tuple(chain.from_iterable(coords))
                
            
            if i != len(geocode)-1:
                
                rotas_totais.append({
                    'Distancia': geocode[i]['distance']['text'],
                    'Duracao': geocode[i]['duration']['text'],
                    'Coordenada_Origem': f"{geocode[i]['start_location']['lat']},{geocode[i]['start_location']['lng']}",
                    'Coordenada_Destino': f"{geocode[i]['end_location']['lat']},{geocode[i]['end_location']['lng']}",             
                    'ID Destino': df_filtrado.loc[ordem_waypoints[i], 'ID'],
                    'Cluster': cluster,
                    'geometry': LineString([(lng, lat) for lat, lng in coords])
                })

            else:
                
                rotas_totais.append({
                    'Distancia': geocode[i]['distance']['text'],
                    'Duracao': geocode[i]['duration']['text'],
                    'Coordenada_Origem': f"{geocode[i]['start_location']['lat']},{geocode[i]['start_location']['lng']}",
                    'Coordenada_Destino': f"{geocode[i]['end_location']['lat']},{geocode[i]['end_location']['lng']}",
                    'ID Destino': 'Ponto fixo',
                    'Cluster': cluster,
                    'geometry': LineString([(lng, lat) for lat, lng in coords])
                })
            
            coords = []
            
    gdf = gpd.GeoDataFrame(rotas_totais, crs="EPSG:4326")
    
    return gdf

# Gerando roteirização partindo de um local fixo em direção ao ponto mais distante
@st.cache_data
def rotear_indo(otimizar):
    
    # Inserindo API KEY
    gmaps = googlemaps.Client(key=chave)
    
    # Gerando lista para guardar resultados finais
    rotas_totais = [] 

    for cluster in arquivo_roteirizacao[coluna_cluster].drop_duplicates():
        
        # classificando valores
        df_filtrado = arquivo_roteirizacao[arquivo_roteirizacao[coluna_cluster] == cluster].reset_index().drop(columns=['index'])
        df_filtrado = df_filtrado.sort_values(by=coluna_distancia, ascending=False).reset_index().drop(columns=['index'])
    
        # pegando distancias
        geocode = gmaps.directions(local_fixo,
                                   df_filtrado.loc[0, coluna_coordenadas],
                                   waypoints=df_filtrado[coluna_coordenadas].tolist()[1:], 
                                   optimize_waypoints=otimizar, 
                                   mode='driving',
                                   alternatives=False)
          
        # ordenar waypoints
        ordem_waypoints = geocode[0]['waypoint_order']

        # pegando rotas
        geocode = geocode[0]['legs']
        
        coords = []
        
        for i in range(len(geocode)):
            
            for ii in range(len(geocode[i]['steps'])):
                           
                coords.append(polyline.decode(geocode[i]['steps'][ii]['polyline']['points']))
                
                # checando se a rota é muito pequena e gerando uma "pseudo-linha"
                if len(coords[0]) == 1:
                   
                    coords[0].append((coords[0][0][0],coords[0][0][1]))
    
            coords = tuple(chain.from_iterable(coords))
                
            
            if i != len(geocode)-1:
                
                rotas_totais.append({
                    'Distancia': geocode[i]['distance']['text'],
                    'Duracao': geocode[i]['duration']['text'],
                    'Coordenada_Origem': f"{geocode[i]['start_location']['lat']},{geocode[i]['start_location']['lng']}",
                    'Coordenada_Destino': f"{geocode[i]['end_location']['lat']},{geocode[i]['end_location']['lng']}",             
                    'ID Destino': df_filtrado.loc[ordem_waypoints[i], 'ID'],
                    'Cluster': cluster,
                    'geometry': LineString([(lng, lat) for lat, lng in coords])
                })

            else:
                
                rotas_totais.append({
                    'Distancia': geocode[i]['distance']['text'],
                    'Duracao': geocode[i]['duration']['text'],
                    'Coordenada_Origem': f"{geocode[i]['start_location']['lat']},{geocode[i]['start_location']['lng']}",
                    'Coordenada_Destino': f"{geocode[i]['end_location']['lat']},{geocode[i]['end_location']['lng']}",
                    'ID Destino': 'Ponto fixo',
                    'Cluster': cluster,
                    'geometry': LineString([(lng, lat) for lat, lng in coords])
                })
            
            coords = []
            
    gdf = gpd.GeoDataFrame(rotas_totais, crs="EPSG:4326")
    
    return gdf

# Gerando roteirização partindo de um local fixo em direção ao mesmo local fixo, circularmente
@st.cache_data
def rotear_circular(otimizar):
    
    # Inserindo API KEY
    gmaps = googlemaps.Client(key=chave)
    
    # Gerando lista para guardar resultados finais
    rotas_totais = [] 
    
    for cluster in arquivo_roteirizacao[coluna_cluster].drop_duplicates():
        
        # classificando valores
        df_filtrado = arquivo_roteirizacao[arquivo_roteirizacao[coluna_cluster] == cluster].reset_index().drop(columns=['index'])
        
        # pegando distancias
        geocode = gmaps.directions(local_fixo,
                                   local_fixo,
                                   waypoints=df_filtrado[coluna_coordenadas].tolist(), 
                                   optimize_waypoints=otimizar, 
                                   mode='driving',
                                   alternatives=False)
          
        # ordenar waypoints
        ordem_waypoints = geocode[0]['waypoint_order']

        # pegando rotas
        geocode = geocode[0]['legs']
        
        coords = []
        
        for i in range(len(geocode)):
            
            for ii in range(len(geocode[i]['steps'])):
                           
                coords.append(polyline.decode(geocode[i]['steps'][ii]['polyline']['points']))
                
                # checando se a rota é muito pequena e gerando uma "pseudo-linha"
                if len(coords[0]) == 1:
                   
                    coords[0].append((coords[0][0][0],coords[0][0][1]))
    
            coords = tuple(chain.from_iterable(coords))
            
            if i != len(geocode)-1:
                
                rotas_totais.append({
                    'Distancia': geocode[i]['distance']['text'],
                    'Duracao': geocode[i]['duration']['text'],
                    'Coordenada_Origem': f"{geocode[i]['start_location']['lat']},{geocode[i]['start_location']['lng']}",
                    'Coordenada_Destino': f"{geocode[i]['end_location']['lat']},{geocode[i]['end_location']['lng']}",             
                    'ID Destino': df_filtrado.loc[ordem_waypoints[i], 'ID'],
                    'Cluster': cluster,
                    'geometry': LineString([(lng, lat) for lat, lng in coords])
                })

            else:
                
                rotas_totais.append({
                    'Distancia': geocode[i]['distance']['text'],
                    'Duracao': geocode[i]['duration']['text'],
                    'Coordenada_Origem': f"{geocode[i]['start_location']['lat']},{geocode[i]['start_location']['lng']}",
                    'Coordenada_Destino': f"{geocode[i]['end_location']['lat']},{geocode[i]['end_location']['lng']}",
                    'ID Destino': 'Ponto fixo',
                    'Cluster': cluster,
                    'geometry': LineString([(lng, lat) for lat, lng in coords])
                })
            
            coords = []
            
    gdf = gpd.GeoDataFrame(rotas_totais, crs="EPSG:4326")
    
    return gdf

# Colocando variáveis importantes no session state
if 'coloracao' not in st.session_state:
    st.session_state.coloracao = [
    "lime", "teal", "lavender", "chartreuse", "lightpink", "indigo", "peru", "peachpuff", "steelblue", "seagreen",
    "mediumvioletred", "springgreen", "darkmagenta", "beige", "lavender", "chocolate", "mediumspringgreen",
    "saddlebrown", "lemonchiffon", "floralwhite", "darkslategray", "blanchedalmond", "crimson", "firebrick",
    "ghostwhite", "lavenderblush", "thistle", "darkkhaki", "navajowhite", "mediumseagreen", "skyblue",
    "palevioletred", "royalblue", "deeppink", "sienna", "plum", "seagreen", "mediumorchid", "mediumseagreen",
    "oldlace", "burlywood", "orangered", "lightgreen", "lawngreen", "mediumblue", "tan", "gainsboro", "gold",
    "lightblue", "bisque", "navy", "darkviolet", "linen", "indigo", "forestgreen", "goldenrod", "chartreuse",
    "mediumturquoise", "mistyrose", "indianred", "salmon", "dimgrey", "azure", "lightsalmon", "turquoise",
    "orangered", "moccasin", "lightcoral", "papayawhip", "brown", "steelblue", "slategray", "dodgerblue",
    "deepskyblue", "firebrick", "lightcyan", "midnightblue", "wheat", "powderblue", "peachpuff", "tomato",
    "rosybrown", "peru", "slateblue", "darkseagreen", "khaki", "darkgoldenrod", "limegreen", "antiquewhite",
    "darkgreen", "mediumaquamarine", "darkorange", "aliceblue", "palegoldenrod", "fuchsia", "lightseagreen",
    "hotpink", "magenta", "cornflowerblue", "lightgray"
]

if 'rotas_geradas' not in st.session_state:
    st.session_state.rotas_geradas = None
    
if 'cluster' not in st.session_state:
    st.session_state.cluster = None

if 'arquivo_gpkg' not in st.session_state:
    st.session_state.arquivo_gpkg = None

if 'buffer_cluster' not in st.session_state:
    st.session_state.buffer_cluster = None

if 'buffer_rotas' not in st.session_state:
    st.session_state.buffer_rotas = None

if 'reload_tab1' not in st.session_state:
    st.session_state.reload_tab1 = None
    
if 'reload_tab2' not in st.session_state:
    st.session_state.reload_tab2 = None

# Configurando página
st.set_page_config(page_title="Easy Clustering and Routing", page_icon=':material/tactic:', layout='wide')

# Ajustando CSSs
st.markdown("""
            <style>
            .st-emotion-cache-y2gf1w {
                position: relative;
                top: 300px;
            }
            
            .st-emotion-cache-lsgwmo p {
                position: relative;
                top: 300px;
                left: 15px;
            }
            </style>      
            """, unsafe_allow_html=True)

# Título
st.title("**Easy** :gray[Clustering and Routing] :busstop:")   

# Sidebar com as infos e os resultados
with st.sidebar:
    
    chave = st.text_input('Insira aqui sua chave API:', type='password')
    st.subheader('Acesse os resultados:', divider='gray')        
    
    # Download clusters
    if st.session_state.cluster is not None:
        
        with st.expander('Apenas clusterização', icon=':material/hive:'):
            
            # Download clusters csv
            st.download_button(
                'Baixe em *.csv*',
                st.session_state.cluster.to_csv(),
                'Clusterização.csv',
                "text/csv",
                key='download-csv',
                use_container_width=True,
                icon=':material/download:',
                type='primary'
            )
 
    # Download pontos clusters gpgk
    if st.session_state.buffer_cluster is not None:
        
        with st.expander('Pontos clusterizados', icon=':material/grain:'):
            
            st.download_button(
                "Baixe em *.gpkg*",
                st.session_state.buffer_cluster,
                'Pontos_Clusterizados.gpkg',
                key='download-gpkg',
                use_container_width=True,
                icon=':material/download:',
                type='primary'
            )
            
    # Download rotas csv
    if st.session_state.rotas_geradas is not None:    
        
        with st.expander('Apenas roteamento', icon=':material/call_split:'):
            
            st.download_button(
                "Baixe em *.csv*",
                st.session_state.rotas_geradas.to_csv(),
                'Roteamento_gerado.csv',
                "text/csv",
                key='download-roteamento-csv',
                use_container_width=True,
                icon=':material/download:',
                type='primary'
            )
            
    # Download rotas gpgk
    if st.session_state.buffer_rotas is not None:     
        
        with st.expander('Linhas de roteamento', icon=':material/tactic:'):
            
            st.download_button(
                "Baixe em *.gpkg*",
                st.session_state.buffer_rotas,
                'Roteamento_gerado.gpkg',
                key='download-roteamento-gpkg',
                use_container_width=True,
                icon=':material/download:',
                type='primary'
            )   
       
    
    # Botão de tira-dúvidas
    if st.button('**Informações importantes**', icon=':material/help:', use_container_width=True, type='tertiary'):
        
        @st.dialog("Informações")
        def duvidas():
            
            # Texto explicativo sobre clusterização
            with st.expander('Clusterização', icon=':material/grain:'):
                
                st.info("""
                        Nessa aba será possível gerar clusters de pontos por meio da metodologia K-Medoids, se utilizando do método PAM, a partir de
                        uma matriz de distância entre os pontos, que deverá ser previamente calculada.\n
                        Para gerar a clusterização, você deverá fazer o upload de um arquivo excel [neste formato](https://github.com/wmoural/EasyGeoMax/raw/refs/heads/main/src/easy_routing/padrao_clusterizacao.xlsx), na área de upload destinada (localizada à esquerda).
                        Você pode gerar até 100 clusters.\n
                        Após gerar os clusters, você pode baixá-los no formato *.csv* ou, caso deseje visualizar a espacialização da clusterização e já atribuir os clusters aos pontos, carregue um arquivo no formato *.gpkg* na área de upload destinada (localizada à direita).
                        Dessa forma, você poderá visualizar e baixar os pontos já com os clusters atribuídos no formato *.gpkg*.
                        API KEY não requerida nessa aba.
                        """)
                
                # Colunas criadas só para posicionar a imagem no centro
                dia_col1, dia_col2, dia_col3 = st.columns([.5,2,.5])
                
                with dia_col2:
                    st.image('https://i.imgur.com/1qN6a7h.gif', caption='[Fonte](https://pt.wikipedia.org/wiki/K-medoides)')
           
            # Texto explicativo sobre clusterização
            with st.expander('Roteirização', icon=':material/tactic:'):           
                
                st.info("""
                        Nessa aba será possível estimar a roteirização de pontos por meio da API Google Directions, utilizando waypoints (pontos de parada) entre a origem e o destino.
                        Para gerar a roteirização, você deverá fazer o upload de um arquivo excel [neste formato](https://github.com/wmoural/EasyGeoMax/raw/refs/heads/main/src/easy_routing/padrao_roteirizacao.xlsx). Caso você deseje fazer roterizações que não são circulares, você deverá 
                        encontrar a distância de cada ponto de parada até o ponto fixo.\n
                        A roteirização considerará no máximo **25 paradas** por cluster.\n
                        A API KEY é requerida nessa aba. A roteirização pode ser feita em três métodos:
                            """)
                
                # Roteirização circular
                with st.container(border=False):
                    div_col1, div_col2 = st.columns([3,1])
                    with div_col1:
                        st.info("""
                                **Roteirização circular**: é realizada quando se deseja estimar uma rota circular em que o ponto de origem e de destino são iguais, 
                                realizando as devidas paradas entre os dois pontos.
                                    """)
                    with div_col2:
                        st.image('https://i.imgur.com/Ap8E0tM.png', use_container_width=True)

                # Roteirização com destino fixo                
                with st.container(border=False):
                    div_col1, div_col2 = st.columns([3,1])
                    with div_col1:
                        st.info("""
                                **Roteirização com destino fixo**: é realizada quando se deseja estimar uma rota linear com origem no ponto fixo, 
                                com destino ao ponto mais distante dentro do cluster designado, realizando as devidas paradas entre os dois pontos.
                                """)
                    with div_col2:
                        st.image('https://i.imgur.com/5nhsPha.png', use_container_width=True)
                    
                with st.container(border=False):
                    div_col1, div_col2 = st.columns([3,1])
                    with div_col1:
                        st.info("""
                                **Roteirização com origem fixa**: é realizada quando se deseja estimar uma rota linear partindo do ponto mais distante dentro de um cluster em relação ao ponto fixo, 
                                realizando as devidas paradas entre os dois pontos.
                                """)
                    with div_col2:
                        st.image('https://i.imgur.com/LxcGHIk.png', use_container_width=True)
                        
        duvidas()
        
    st.caption('Projeto desenvolvido por [Wellington Moura](www.linkedin.com/in/wmoural/)')

# Criando tabs
tab1, tab2 = st.tabs(['Clusterização', 'Roteirização'])

# Tab para clusterização
with tab1:

    # Definindo reload
    st.session_state.reload_tab1 = False
    
    tab1_col1, tab1_col2 = st.columns([2,2])
    
    with tab1_col1:
        
        # Carregando a matriz de distâcia
        matriz = st.file_uploader('**Carregue a matriz de distâncias**', type=['xlsx'])

        if matriz is not None:
            
            # Transformando o arquivo em dataframe
            matriz = pd.read_excel(matriz, engine='openpyxl')
            
            # Botão de inputs
            with st.form('Campos de input', border=False):
                
                tab1_col1_col1, tab1_col1_col2 = st.columns([2,2])
                
                with tab1_col1_col1:
        
                    linha_pivot = st.selectbox('Indique a coluna com a origem', matriz.columns, index=None, placeholder='Selecione uma coluna')
                    valores_pivot = st.selectbox('Indique a coluna com a impedância', matriz.columns, placeholder='Tempo, distância, custo...', index=None)
                    
                with tab1_col1_col2:                  

                    coluna_pivot = st.selectbox('Indique a coluna com o destino', matriz.columns, index=None, placeholder='Selecione uma coluna')
                    qtde_clusters = st.number_input('Quantidade de clusters?', min_value=1, max_value=len(st.session_state.coloracao), value=None, placeholder='Valor máximo de 100')
                
                # Criando colunas para posicionar o botão no centro
                tab1_col1_col3, tab1_col1_col4, tab1_col1_col5 = st.columns([1,2,1])
                
                with tab1_col1_col4:
                    
                    # Criando submit button do formulário
                    gerar_clusters = st.form_submit_button('Gerar clusters', use_container_width=True, icon=':material/hive:')
                
                if gerar_clusters:
                    
                    # Gerando dataframe com clusterização
                    st.session_state.cluster = clusterizar(matriz.pivot(index=linha_pivot, 
                                                                        columns=coluna_pivot, 
                                                                        values=valores_pivot),
                                                           qtde_clusters)
                    
                    st.toast('Clusterização concluída', icon=':material/done_all:')
                    st.rerun()
            
    with tab1_col2:
        
        # Carregando pontos
        
        if st.session_state.cluster is None:
            
            pontos = st.file_uploader('**Carregue os pontos para clusterização**', type=['.gpkg'], disabled=True)
        
        else:
            
            pontos = st.file_uploader('**Carregue os pontos para clusterização**', type=['.gpkg'], disabled=False)
            
        if pontos is not None and st.session_state.cluster is not None:
        
                # Criando buffer
                gpkg_buffer = io.BytesIO(pontos.getvalue())
                
                # Lendo área de interesse
                arquivo_gpd = gpd.read_file(gpkg_buffer)
                
                # Extraindo X e Y
                arquivo_gpd['x'] = arquivo_gpd.geometry.x
                arquivo_gpd['y'] = arquivo_gpd.geometry.y
                
                # Inserindo o cluster
                arquivo_gpd = pd.merge(arquivo_gpd, st.session_state.cluster)
                st.session_state.reload_tab1 = False

                # Mostrando clusters gerados
                m = leafmap.Map(center=[arquivo_gpd.geometry.y.mean(), arquivo_gpd.geometry.x.mean()], zoom=11)
                
                # Iterando para carregar cluster por cluster com cores especificas
                for i in range(qtde_clusters):
                    
                    gpd_filtrado = arquivo_gpd[arquivo_gpd['Cluster'] == i]
                    
                    m.add_circle_markers_from_xy(gpd_filtrado, x='x', y='y', color='white', fill_color=st.session_state.coloracao[i])
                
                # Renderizando o mapa
                m.to_streamlit(responsive=True, scrolling=True, height=500)
                
                # Salvando resultado num buffer
                if arquivo_gpd is not None:
                    
                        tab1_col2_col1, tab1_col2_col2, tab1_col2_col3 = st.columns([1,2,1])
                        
                        with tab1_col2_col2:
                        
                            if st.button('Processar pontos', icon=':material/grain:', use_container_width=True):
                            
                                # Guardando espaço na memória
                                st.session_state.buffer_cluster = io.BytesIO()
                                
                                # Colocando geopackage no buffer
                                arquivo_gpd.to_file(st.session_state.buffer_cluster, driver="GPKG")
        
                                # Rerun só pra aparecer pontos nos resultados
                                st.rerun()
               
# Expander roterização
with tab2:

    # Definindo colunas pros inputs
    tab2_col1, tab2_col2 = st.columns([2,2])
    
    with tab2_col1:
        
        # Carregando o excel com os pontos e os clusters
        arquivo_roteirizacao = st.file_uploader('Carregue excel com os clusters e os pontos para roteirização', )
        
        if arquivo_roteirizacao is not None:
            
            # Lendo excel como dataframe
            arquivo_roteirizacao = pd.read_excel(arquivo_roteirizacao, engine='openpyxl')
            
            with st.form('Formulario roteirizacao', border=False):
                
                local_fixo = st.text_input('Insira a coordenada do ponto fixo (de partida ou destino)', placeholder='Ex.: -3.807155,-38.561099')
                
                # Gerando colunas para organizar inputs
                formcol1,formcol2 = st.columns([1,1]) 
                                
                with formcol1:
                    
                    # Inputs 
                    tipo_roteirizacao = st.selectbox('Tipo de roteirização',['Circular','Destino fixo','Origem fixa'], index=None, placeholder='Selecione o método')
                    coluna_distancia = st.selectbox('Indique a coluna de distância até o ponto fixo', arquivo_roteirizacao.columns, index=None, placeholder='Deixe vazio se o roteamento for Circular')

                with formcol2:
                    
                    # Inputs 
                    coluna_cluster = st.selectbox('Indique a coluna de clusters', arquivo_roteirizacao.columns, index=None, placeholder='Selecione uma coluna')
                    coluna_coordenadas = st.selectbox('Indique a coluna de coordenadas', arquivo_roteirizacao.columns, index=None, placeholder='Selecione uma coluna')
                
                # Gerando colunas para organizar inputs
                formcol3,formcol4,formcol5,formcol6 = st.columns([.5,1,1,.5]) 
                 
                # Botão de otimização de rotas                  
                with formcol4:
                    
                    otimizar = st.toggle('Ativar otimização')
                
                # Botão para rotear
                with formcol5:

                    botaorotear = st.form_submit_button('Gerar roteamento', use_container_width=True, icon=':material/call_split:')
                    
                    if botaorotear:
                    
                        if tipo_roteirizacao == 'Circular':
                            
                            st.session_state.rotas_geradas = rotear_circular(otimizar)
                            
                        elif tipo_roteirizacao == 'Destino fixo':
                            
                            st.session_state.rotas_geradas = rotear_indo(otimizar)
                            
                        else:
                            
                            st.session_state.rotas_geradas = rotear_vindo(otimizar)

                        if st.session_state.rotas_geradas is not None:
                            
                            # Corrigindo um zig com formatação 64int
                            st.session_state.rotas_geradas = st.session_state.rotas_geradas.applymap(lambda x: x.item() if hasattr(x, 'item') else x)
                            
                            # Guardando espaço na memória
                            st.session_state.buffer_rotas = io.BytesIO()
                            
                            # Colocando geopackage no buffer
                            st.session_state.rotas_geradas.to_file(st.session_state.buffer_rotas, driver="GPKG")

                            st.rerun()
            
    with tab2_col2:
          
        if st.session_state.rotas_geradas is not None:
            
            # Pegando limites do geodataframe
            limites_geodataframe = st.session_state.rotas_geradas.total_bounds 
            x_limites = (limites_geodataframe[0]+limites_geodataframe[2])/2
            y_limites = (limites_geodataframe[1]+limites_geodataframe[3])/2           
            
            # Gerando mapinha
            m_tab2 = leafmap.Map(center=[y_limites, x_limites], zoom=11)
            m_tab2.add_basemap("SATELLITE")

            # Adicionando rotas no mapa
            for i in st.session_state.rotas_geradas['Cluster'].drop_duplicates():
                
                gpd_filtrado = st.session_state.rotas_geradas[st.session_state.rotas_geradas['Cluster'] == i]
                
                cor = st.session_state.coloracao[random.randint(0,99)]
            
                for _, row in gpd_filtrado.iterrows():
                    linha = row.geometry
            
                    if isinstance(linha, LineString):
                        coords = [[pt[1], pt[0]] for pt in linha.coords]
            
                        # Definindo informações para exibir
                        info = f"""
                        <b>Cluster:</b> {row['Cluster']}<br>
                        <b>ID Destino:</b> {row['ID Destino']}<br>
                        <b>Distância:</b> {row['Distancia']}<br>
                        <b>Duração:</b> {row['Duracao']}
                        """
            
                        folium.PolyLine(
                            locations=coords,
                            color=cor,
                            weight=3,
                            opacity=0.8,
                            tooltip=folium.Tooltip(info, sticky=True),
                            popup=folium.Popup(info, max_width=300)
                        ).add_to(m_tab2)
            
            
            # Adicionando pontos no mapa
            origens = st.session_state.rotas_geradas[['Coordenada_Origem', 'ID Destino']].drop_duplicates().copy()
            origens[['lat', 'lon']] = origens['Coordenada_Origem'].str.split(',', expand=True).astype(float)
            origens.rename(columns={'ID Destino': 'ID'}, inplace=True)
            m_tab2.add_circle_markers_from_xy(
                origens,
                x="lon",
                y="lat",
                popup="ID",  # Or use tooltip="ID"
                layer_name="Pontos de Origem e Destino",
                color="white",
                fill_color="red",
                radius=7
            )
            
            # Renderizando mapas
            m_tab2.to_streamlit(responsive=True, scrolling=True, height=500)
