import geopandas as gpd
import streamlit as st
from overturemaps import core
import leafmap.foliumap as leafmap
import pandas as pd
from shapely import wkt
import io
from io import BytesIO

# Funções para estilização do mapa
def estilobbox(feature):
    return {
    "color": "green",
    "fillOpacity": 0
    }

def estiloarea(feature):
    return {
    
        "stroke": True,
        "color": "green",
        "weight": 2,
        "opacity": 1,
        "fill": True,
        "fillColor": "green",
        "fillOpacity": 0.4,
    }

# Definindo variáveis importantes
if 'resultado' not in st.session_state:
    st.session_state.resultado = None

# Configurando página
st.set_page_config(page_title="Easy OvertureData", page_icon=':motorway:',layout='wide')

# Título
st.title("**Easy** :violet[OvertureData] :motorway:")    

# Configurando sidebar
with st.sidebar:
    
    with st.expander('**Informações importantes**', icon='ℹ️', expanded=False):
        st.info("""
                - A área de interesse deve ser um POLÍGONO;
                - A área de interesse deve estar no SRC WGS84 (EPSG:4326);
                - Cada tipo de dado leva um tempo específico para ser carregado;
                - Mantenha a tela do computador ligada nesta aba após iniciar o processo;
                - A ferramenta é indicada para projetos de pequeno e médio porte.
                """)

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
    
    with st.expander('**Mais sobre Streamlit:** ', expanded=False):
        st.info('[Veja aqui](https://streamlit.io/)')    
    
# Definindo uploader de arquivo    
arquivo = st.file_uploader('**Faça o upload da área de interesse aqui** :call_me_hand:', type=['.gpkg'])

col1,col2 = st.columns([3,2])

with col2:
    
    # Iniciado aplicação caso haja caixa delimitadora
    if arquivo is not None:

        # Criando buffer
        gpkg_buffer = io.BytesIO(arquivo.getvalue())
        
        # Lendo área de interesse
        arquivo_gpd = gpd.read_file(gpkg_buffer)
        
        # Corrigindo erro comum de coluna com datetime errado/ausente
        if 'arquivo_gpd' in locals():
            datetime_cols = arquivo_gpd.select_dtypes(include=['datetime64', 'timedelta64']).columns
            if len(datetime_cols) > 0:
                arquivo_gpd[datetime_cols] = arquivo_gpd[datetime_cols].astype(str)
        
        # Pegando os bbox
        limites = arquivo_gpd.total_bounds
        limites = (limites[0],limites[1],limites[2],limites[3])

        # Definindo filtros para executar
        with st.form('Definições de filtragem'):        
            
            categorias = {'Edificações':'building', 
             'Pontos de interesse (PGVs)':'place', 
             'Segmentos viários (links)':'segment',
             'Nós viários':'connector', 
             'Infraestrutura':'infrastructure', 
             'Solo':'land', 
             'Uso do solo':'land_use', 
             'Massas de água':'water'}
             
            # Organizando botões e rodando filtragem
            c1,c2,c3 = st.columns([2,2,1.5])          
            
            busca = st.selectbox('**🛠️ Escolha o tema:**', list(categorias.keys()))

            nomapa = st.toggle('Carregar resultado para mapa?')
            
            st.warning("""          
                       Caso a área de interessa seja grande, o funcionamento da
                       aplicação pode ser severamente afetado e seu progresso poderá
                       ser perdido caso deseje carregar os resultados no mapa. Pondere.
                       """, icon='⚠️')
            
            rodar = st.form_submit_button('**Filtrar! 🔎**', use_container_width=True)
            
            if rodar:
                                   
                with st.status('Buscando...') as status:

                    st.session_state.resultado = core.geodataframe(categorias[busca], bbox=limites)
                    
                    status.update(label='**:green[Filtragem completa: {len(st.session_state.resultado)} resultados encontrados!]** :partying_face:', state='complete', expanded=False)
                            
        if st.session_state.resultado is not None:
            
            # Gerando gdf de resultado no cache
            buffer = io.BytesIO()
            
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                st.session_state.resultado.to_excel(writer, sheet_name='Sheet1')
                writer.close()    

            # Criando botão de download
            cl1,cl2,cl3 = st.columns([2,2,2])
            
            with cl2:

                st.download_button(
                    label="**:green[Download em excel (WKT)] ✅**",
                    data=buffer,
                    file_name=f"base-{busca}.xlsx",
                    mime="application/vnd.ms-excel",
                    use_container_width=True)

with col1:
    
    if arquivo is not None:  
        
        # Criando instância de mapa
        m = leafmap.Map()
        m.add_basemap("SATELLITE")
        
        # Alimentando com a área de interesse + bbox
        m.add_gdf(arquivo_gpd, layer_name='Area de interesse', style_callback=estiloarea)
        m.add_gdf(gpd.GeoDataFrame(geometry=arquivo_gpd.geometry.envelope,crs=arquivo_gpd.crs), layer_name='BoundingBox', style_callback=estilobbox)
        
        # Caso existam resultados da busca, inserí-los no mapa
        if st.session_state.resultado is not None and nomapa is True:
            
            df = st.session_state.resultado
            
            # Por algum motivo, carregar todo o gdf ou df dá errado
            df = st.session_state.resultado[['geometry']].astype(str) 

            df['geometry'] = df['geometry'].apply(wkt.loads)
            
            gdf = gpd.GeoDataFrame(df, geometry='geometry')
            
            gdf.set_crs(epsg=4326, inplace=True)
            
            m.add_gdf(gdf, layer_name=busca,fill_colors=["red"])     
        
        # Renderizando o mapa no streamlit
        m.to_streamlit(responsive=True, scrolling=True)

# Mostrando tabela com resultados finais
if st.session_state.resultado is not None:
    
    with st.expander('Resultados:'):
        
        st.session_state.resultado
