import googlemaps
import pandas as pd
import streamlit as st
import xlsxwriter
from io import BytesIO
import io

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

@st.cache_data
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
    
    return df

arquivo_matriz = st.file_uploader('**Faça o upload da planilha aqui!:call_me_hand:**', type=['xlsx'])

if 'MatrizResultado' not in st.session_state:
    
    st.session_state.MatrizResultado = None

if arquivo_matriz is not None:
            
    buffer = io.BytesIO()
    
    df = pd.read_excel(arquivo_matriz)
    
    with st.form('Form rodar matriz'):
        Origem = st.selectbox('**Indique a coluna com a origem:**', df.columns)
        Destino = st.selectbox('**Indique a coluna com o destino:**', df.columns)
        Modo = st.selectbox('**Indique a coluna com o modo de deslocamento:**', df.columns)
        
        rodar = st.form_submit_button('**Calcular**')
        
        if rodar:

            st.session_state.MatrizResultado = Matriz_uma_por_uma(chave, df)                
        
            
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                st.session_state.MatrizResultado.to_excel(writer, sheet_name='Sheet1')
                writer.close()    
            
            st.success('Processo concluído!')
            st.dataframe(st.session_state.MatrizResultado)
        

    st.download_button(
        label="**Download em excel**",
        data=buffer,
        file_name="Matriz gerada.xlsx",
        mime="application/vnd.ms-excel"
    )

else:

    st.session_state.MatrizResultado = None
