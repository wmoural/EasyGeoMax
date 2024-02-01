import googlemaps
import pandas as pd
import streamlit as st
import xlsxwriter
from io import BytesIO
import io

# Configurando página
st.set_page_config(page_title='Easy Geocoding', layout='wide')

# Título
st.title("**Easy** :green[Geocoding] :world_map:")    

with st.sidebar:
    chave = st.text_input('Insira aqui sua chave API:', type='password')
    
# Funções para colunas
def GeocodeDemanda(df, Chave):

    # Inserindo API KEY
    gmaps = googlemaps.Client(key=Chave)

    # Gerando listas
    lat = []
    long = []
    endereço_formatado = []

    # Geocodificando endereços
    for i in range(len(df)):
        geocode = gmaps.geocode(df[ColunaEndereço].loc[i], region="br", language="PT-BR")
        if len(geocode) == 0:
            lat.append('0')
            long.append('0')
            endereço_formatado.append('0')
        else:
            resultado = geocode[0]
            lat.append(resultado['geometry']['location']['lat'])
            long.append(resultado['geometry']['location']['lng'])
            endereço_formatado.append(resultado['formatted_address'])

    # Criando novas colunas e colando resultados
    df['Lat'] = lat
    df['Long'] = long
    df['Endereço'] = endereço_formatado
    return df



def MostrarCol2():
    with col2:

        if st.session_state.DemandaGerada is not None:
            st.balloons()
            st.dataframe(st.session_state.DemandaGerada, use_container_width=True)

            st.download_button(
                label="**Download em excel**",
                data=buffer,
                file_name="Demanda gerada.xlsx",
                mime="application/vnd.ms-excel"
            )

            st.cache_resource.clear()


def MostrarCol3():
    with col3:
        df = pd.DataFrame(st.session_state.DemandaGerada)
        df['Lat'] = df['Lat'].astype(float)
        df['Long'] = df['Long'].astype(float)
        df = df.rename(columns={'Long': 'lon', 'Lat': 'lat'})
        st.map(df)


# Botão para subir planilha excel
ArquivoCarregado = st.file_uploader('**Faça o upload da planilha aqui** :call_me_hand:', type=['xlsx'])

if ArquivoCarregado is not None:

    # Transformando o arquivo carregado em DataFrame
    df = pd.read_excel(ArquivoCarregado, engine='openpyxl')

    tamanho = len(df)

    # Colunas
    col1, col2, col3 = st.columns([2, 5, 4])

    # Criando botões de input
    with col1:

        with st.form("Inputs"):

            ColunaEndereço = st.selectbox("Selecione a coluna com o endereço", list(df.columns.values))

            # Botão pra rodar o geocode
            rodar = st.form_submit_button("Geocodificar")

            if rodar:

                if 'DemandaGerada' not in st.session_state:
                    st.session_state.DemandaGerada = GeocodeDemanda(df, chave)

                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    st.session_state.DemandaGerada.to_excel(writer, sheet_name='Sheet1')
                    writer.close()
                    
                    
                st.success('Processo concluído!')
                MostrarCol2()
                MostrarCol3()
                st.stop()
                st.cache_resource.clear()
