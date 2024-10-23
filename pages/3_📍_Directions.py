import googlemaps
import pandas as pd
import streamlit as st
from datetime import datetime
from shapely.geometry import LineString
import polyline
import geopandas as gpd
import leafmap.foliumap as leafmap

st.set_page_config(page_title='Easy Directions', layout='wide')

# Título
st.title("**Easy** :red[Directions] 📍")    

with st.sidebar:
    
    st.info("""
            Use os seguintes valores para indicar o modo de transporte:
            - driving (para carros e motos)
            - bicycling (para bicicleta)
            - walking (para a pé)
            - bus (para ônibus)
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
    
    with st.expander('**Mais sobre Streamlit:** ', expanded=False):
        st.info('[Veja aqui](https://streamlit.io/)')    

# Função para calculo de matriz
def Matriz_uma_por_uma(chave, dataframe):
    
    # Inputs
    df = dataframe
    
    # Conectando ao client googlemaps
    gmaps = googlemaps.Client(key=chave)
    
    # Criando novas colunas a serem preenchidas
    df['Origem_Formatada'] = ''
    df['LatLong_Origem'] = ''
    df['Destino_Formatado'] = ''
    df['LatLong_Destino'] = ''
    df['Tempo [s]'] = ''
    df['Distância [m]'] = ''
    rotas = []
    
    # Loops
    for i in range(len(df)):
        
        try:
            
            if df[Modo].loc[i] == 'bus':
                geocode = gmaps.directions(df[Origem].loc[i], df[Destino].loc[i], mode='transit', transit_mode='bus')
                
            if df[Modo].loc[i] != 'bus':
                geocode = gmaps.directions(df[Origem].loc[i], df[Destino].loc[i], mode=df[Modo].loc[i])
                
            if len(geocode)>0:
                
                geocode = geocode[0]['legs'][0]
                
                df['Origem_Formatada'].loc[i] = geocode['start_address']
                df['LatLong_Origem'].loc[i] = geocode['start_location']
                df['Destino_Formatado'].loc[i] = geocode['end_address']
                df['LatLong_Destino'].loc[i] = geocode['end_location']
                df['Tempo [s]'].loc[i] = geocode['duration']['value']
                df['Distância [m]'].loc[i] = geocode['distance']['value']
                
                for rota in geocode['steps']:
                    
                    rota.update({'Origem':df['ori'].loc[i], 'Destino':df['dest'].loc[i], 'Indice':i})

                rotas.append(geocode['steps'])
                
            else:
                
                df['Origem_Formatada'].loc[i] = 'Não encontrado'
                df['LatLong_Origem'].loc[i] = 'Não encontrado'
                df['Destino_Formatado'].loc[i] = 'Não encontrado'
                df['LatLong_Destino'].loc[i] = 'Não encontrado'
                df['Tempo [s]'].loc[i] = 'Não encontrado'
                df['Distância [m]'].loc[i] = 'Não encontrado'
                            
        except:
            
                df['Origem_Formatada'].loc[i] = 'Não encontrado'
                df['LatLong_Origem'].loc[i] = 'Não encontrado'
                df['Destino_Formatado'].loc[i] = 'Não encontrado'
                df['LatLong_Destino'].loc[i] = 'Não encontrado'
                df['Tempo [s]'].loc[i] = 'Não encontrado'
                df['Distância [m]'].loc[i] = 'Não encontrado'
    
    return (df, rotas)

# Função para criar as rotas
def roteamento(rotas):

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
                'índice': caminho['Indice'],
                'geometry': line_geometry
            })
    
    # Convert the list of geometries into a GeoDataFrame
    gdf = gpd.GeoDataFrame(rotas_totais, crs="EPSG:4326") 
    
    return gdf

arquivo_matriz = st.file_uploader('**Faça o upload da planilha aqui!:call_me_hand:**', type=['xlsx'])

if 'MatrizResultado' not in st.session_state:
    
    st.session_state.MatrizResultado = None
    
if 'Rotas' not in st.session_state:
    
    st.session_state.Rotas = None

# Iniciando aplicação
if arquivo_matriz is not None:
    
    df = pd.read_excel(arquivo_matriz)
    
    col1,col2 = st.columns([5,5])
    
    with col1:
    
        with st.form('Form rodar matriz'):
            
            Origem = st.selectbox('**Indique a coluna com a origem:**', df.columns)
            Destino = st.selectbox('**Indique a coluna com o destino:**', df.columns)
            Modo = st.selectbox('**Indique a coluna com o modo de deslocamento:**', df.columns)
            
            rodar = st.form_submit_button('**Calcular**')
            
            if rodar:
                
                with st.status('Calculando matriz...', expanded=True) as status:
                    
                    st.session_state.MatrizResultado, rotas = Matriz_uma_por_uma(chave, df)
                    st.session_state.Rotas = roteamento(rotas)
        
                st.balloons()
                status.update(label='Cálculo concluído', state='complete')
                
        cl1,cl2,cl3 = st.columns([1,5,1])
        
        with cl2:
            
            if st.session_state.MatrizResultado is not None and arquivo_matriz is not None:
                
                with st.status('Gerando CSV...') as status2:
                    
                    st.download_button(
                        label="Baixe em CSV - Matriz geral",
                        data=st.session_state.MatrizResultado.to_csv(),
                        file_name=f"Directions-{datetime.now()}.xlsx",
                        mime="text/csv",
                        key='download-csv',
                        use_container_width=True,
                        icon='✅'
                    )
                    
                    st.download_button(
                        label="Baixe em CSV - Matriz de percursos",
                        data=st.session_state.Rotas.to_csv(),
                        file_name=f"Directions-{datetime.now()}.xlsx",
                        mime="text/csv",
                        key='download-csv2',
                        use_container_width=True,
                        icon='✅'
                    ) 
                    
                status2.update(label='**CSVs Gerados!**', state='complete', expanded=False)
                
# Mostrando mapa na coluna 2    
    with col2:
        
        if st.session_state.MatrizResultado is not None and arquivo_matriz is not None:

            # Criando instância de mapa
            m = leafmap.Map()
            m.add_gdf(st.session_state.Rotas, layer_name='Roteamento')
            m.to_streamlit(responsive=True, scrolling=True)

# Carregando resultados finais
if st.session_state.MatrizResultado is not None and arquivo_matriz is not None:
     
    with st.expander('**Matriz geral:**'):
        
        st.dataframe(st.session_state.MatrizResultado)
        
    with st.expander('**Percursos:**'):
        
        st.dataframe(st.session_state.Rotas)
