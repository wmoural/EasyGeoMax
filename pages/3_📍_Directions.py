import googlemaps
import pandas as pd
import streamlit as st
from datetime import datetime

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
                    
                    st.session_state.MatrizResultado = Matriz_uma_por_uma(chave, df)
                    
                st.balloons()
                status.update(label='Cálculo concluído', state='complete')
                
        cl1,cl2,cl3 = st.columns([1,5,1])
        
        with cl2:
            
            if st.session_state.MatrizResultado is not None and arquivo_matriz is not None:
                
                with st.status('Gerando CSV...') as status2:
                    
                    st.download_button(
                        label="Baixe em CSV",
                        data=st.session_state.MatrizResultado.to_csv(),
                        file_name=f"Directions-{datetime.now()}.xlsx",
                        mime="text/csv",
                        key='download-csv',
                        use_container_width=True,
                        icon='✅'
                    ) 
                    
                status2.update(label='**CSV Gerado!**', state='complete', expanded=False)
            
    with col2:
        
        if st.session_state.MatrizResultado is not None and arquivo_matriz is not None:
            
            st.dataframe(st.session_state.MatrizResultado)
