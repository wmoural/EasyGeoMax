import geopandas as gpd
import streamlit as st
from overturemaps import core
import leafmap.foliumap as leafmap
import io
from datetime import datetime
import time
from estilos_css import uploader, uploader_depois

# Limpando cache
st.cache_data.clear()
   
# Configurando página
st.set_page_config(page_title="Easy Overture", page_icon=':south_america:',layout='wide')

# Funções
    # Funções para carregamento do layout
@st.cache_data
def carregar_layout(): # Função para ajustar o layout (coisa de frontend, não importa)
    if arquivo is None:
        with st.container(horizontal_alignment='center'):
            
            st.title('Easy :red[Overture :material/south_america:]', width='content')
            st.caption('Aplicação web para acesso à base de dados OvertureMaps Foundation', width=410)
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
            st.title('Easy :red[Overture :material/south_america:]', width='content')
            st.caption('Aplicação web para acesso à base de dados OvertureMaps Foundation', width=410 )
            st.markdown(
                """
                <hr style="margin:5px 0 0px 0;">
                """,
                unsafe_allow_html=True
            )
            
            # Ajustes de CSS
        st.markdown(uploader_depois(arquivo.name), unsafe_allow_html=True)

# Funções para estilização do mapa
@st.cache_data
def estilobbox(feature):
    return {
    "color": "red",
    "fillOpacity": 0,
    "weight": 3,
    }
@st.cache_data
def estiloarea(feature):
    return {
    
        "stroke": True,
        "color": "red",
        "weight": 3,
        "opacity": 1,
        "fill": True,
        "fillColor": "red",
        "fillOpacity": 0.1,
        "dashArray": "5, 10",
    }

    # Carregando mapa
def mapa(area):
    # Criando instância de mapa
    m = leafmap.Map()
    
    # Carregando basemap de satélites
    m.add_basemap("SATELLITE")

    # Alimentando com a área de interesse + bbox
    m.add_gdf(area, layer_name='Area de interesse', style_callback=estiloarea)
    m.add_gdf(gpd.GeoDataFrame(geometry=area.geometry.envelope,crs=area.crs), layer_name='BoundingBox', style_callback=estilobbox) 
    m.to_streamlit(responsive=True, scrolling=True, height=450)
    
    return m

    # Definindo as categorias
if 'categorias' not in st.session_state:
    st.session_state.categorias = {'Edificações':'building',
                                   'PGVs':'place',
                                   'Vias':'segment',
                                   'Nós viários':'connector',
                                   'Infraestrutura':'infrastructure',
                                   'Solo':'land',
                                   'Uso do solo':'land_use',
                                   'Massas de água':'water'
                                   }
        
    # Filtragem
def BaixarOverture(area, categoria):   

   # Pegando os bbox
   limites = area.total_bounds
   limites = (limites[0],limites[1],limites[2],limites[3])

   # Fazendo progress bar
   progress_bar = st.progress(0)

   # Carregando os dados
   progress_bar.progress(50, text=f":material/hourglass_empty: Acessando dados...") 
   dados = gpd.GeoDataFrame(core.geodataframe(categoria, bbox=limites))
   dados = dados.astype(str)
   
   # Ajuste de colunas
   progress_bar.progress(90, text=f":material/hourglass_empty: Ajustando colunas...") 
   
   if str(categoria) == 'place':
      nome = dados['names'].str.split(': ', expand=True).replace([", 'common'", "'"],['',''], regex=True)
      dados['names'] = nome[1]

      categoria = dados['categories'].str.split(': ', expand=True).replace([", 'alternate'", "'"], ['', ''], regex=True)
      dados['categories'] = categoria[1]

   if str(categoria) == 'segment':
      nome = dados['names'].str.split(': ', expand=True).replace([", 'common'", "'"],['',''], regex=True)
      dados['names'] = nome[1]
      
   if str(categoria) == 'infrastructure':
      nome = df_temp['names'].str.split(': ', expand=True).replace([", 'common'", "'"],['',''], regex=True)
      dados['names'] = nome[1]
   
   progress_bar.progress(100, text=":green[:material/done_all: **Dados disponibilizados!**]")
   
   return dados

# Definindo variáveis importantes
if 'Resultado' not in st.session_state:
    st.session_state.Resultado = None

# Configurando sidebar
with st.sidebar:
    
    with st.expander('**Informações importantes**', icon=':material/info:', expanded=False):
        st.info("""
                - A área de interesse deve ser um POLÍGONO;
                - A área de interesse deve estar no SRC WGS84 (EPSG:4326);
                - Cada tipo de dado leva um tempo específico para ser carregado;
                - Mantenha a tela do computador ligada nesta aba após iniciar o processo;
                - A ferramenta é indicada para projetos de pequeno e médio porte.
                """)
        

    # Definindo uploader de arquivo    
    arquivo = st.file_uploader('**Faça o upload da área de interesse aqui** :call_me_hand:', type=['.gpkg','.geojson'])
    
# Carregando layout
carregar_layout()

# Iniciado aplicação caso haja caixa delimitadora
if arquivo is not None:
       
    # Criando buffer
    buffer = io.BytesIO(arquivo.getvalue())
    
    # Lendo área de interesse
    area_entrada = gpd.read_file(buffer)
    area_entrada = area_entrada[['geometry']]
    
    # Definindo container de inputs
    container_inputs = st.container(border=False,
                                    horizontal=False,
                                    horizontal_alignment='center',
                                    vertical_alignment='center'
                                    )
    
    # Trabalhando com o container
    with container_inputs:
        
            # Definindo filtros para executar
            with st.form('Definições de filtragem', border=False, width=400):        
                        
            
                # Organizando botões e rodando filtragem       
                busca = st.selectbox('',
                                     list(st.session_state.categorias.keys()),
                                     placeholder='Selecione o tipo de dado a ser consultado',
                                     width=400,
                                     index=None)
      
                rodar = st.form_submit_button("Acessar dados",
                                              width='stretch',
                                              type='primary',
                                              icon=':material/south_america:'
                                              )

                # Execução do botão rodar
                if rodar:
                           
                    with st.progress(0, "Iniciando...") as progress_bar:
                        st.session_state.Resultado = BaixarOverture(area_entrada, st.session_state.categorias[busca])
                    st.balloons()
                    time.sleep(2)
                    st.rerun()

    # Renderizando o mapa no streamlit
    m = mapa(area_entrada)

# Inserindo botões de download dos resultados
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
            f"Dados geocodificados - {datetime.now()}.xlsx",
            "application/vnd.ms-excel",
            key='download-xlsx',
            on_click='rerun',
            type='primary',
            width=500,
            icon=':material/download_for_offline:'
        )













