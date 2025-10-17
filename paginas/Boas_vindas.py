import streamlit as st

# Configurando página
st.set_page_config(page_title='Easy Geo!', layout='wide', page_icon=':material/home:')

# Carregando layout
with st.container(horizontal_alignment='center'):
    st.title('Easy :green[GeoMax!]', width='content')
    st.caption('Aplicação web multifuncionalidade', width='content')

CSS = """
<style>
:root{
  --accent: #0b63d6;
  --muted: #6b7280;
  --shadow: 0 6px 18px rgba(13, 27, 62, 0.08);
}

body {font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;}

.card{
  border-radius:12px;
  padding:24px;
  box-shadow: var(--shadow);
  border: 1px solid rgba(11,99,214,0.06);
  height: 240px;
  display:flex;flex-direction:column;justify-content:flex-start;
  transition: transform .16s ease, box-shadow .16s ease;
  overflow: hidden;
}
.card:hover{transform: translateY(-6px); box-shadow: 0 18px 40px rgba(11,99,214,0.08);} 
.card h3{margin:0 0 10px 0; font-size:20px; color:#062a48;}
.card .subtitle{font-size:14px; color:var(--muted); margin-bottom:14px}
.card p{margin:0; font-size:15px; color:#13324a; line-height:1.5; flex-shrink:0; overflow-wrap: break-word;}
.card .badge{display:inline-block;padding:6px 10px;border-radius:999px;font-weight:600;font-size:13px;background:rgba(11,99,214,0.09);color:var(--accent);margin-bottom:12px}

.card-1{background: linear-gradient(135deg, #d0f0c0 0%, #a8e6a3 100%);}
.card-2{background: linear-gradient(135deg, #c0e8b0 0%, #88d78c 100%);}
.card-3{background: linear-gradient(135deg, #b0e0a0 0%, #70c870 100%);}
.card-4{background: linear-gradient(135deg, #a0d890 0%, #58b858 100%);}

@media (max-width: 900px){
  .stColumns > div {width: 100% !important; margin-bottom:16px}
  .card {height: auto; min-height:200px}
}
</style>
"""

descriptions = [
    {
        "title": "Easy Geocoding",
        "badge": "Geocodificação",
        "class": "card-1",
        "text": "Realize geocodificação de endereços de forma rápida e precisa. O Easy Geocoding converte listas de endereços em coordenadas geográficas utilizando provedores confiáveis como Google e ArcGIS, permitindo integração direta com análises espaciais e mapas temáticos."
    },
    {
        "title": "Easy ReverseGeocoding",
        "badge": "Geocodificação Reversa",
        "class": "card-2",
        "text": "Obtenha endereços detalhados a partir de coordenadas geográficas. O Easy ReverseGeocoding utiliza as APIs do Google e ArcGIS para identificar locais com precisão, facilitando a validação de dados espaciais e o enriquecimento de bases geográficas."
    },
    {
        "title": "Easy Routes",
        "badge": "Rotas Otimizadas",
        "class": "card-3",
        "text": "Gere rotas otimizadas de maneira simples e eficiente. O Easy Routes calcula trajetos entre múltiplos pontos usando a API Directions do Google, permitindo análises de mobilidade, planejamento logístico e comparação de alternativas de deslocamento."
    },
    {
        "title": "Easy Overture",
        "badge": "Dados Overtures",
        "class": "card-4",
        "text": "Acesse e baixe dados abertos da Overture Maps Foundation diretamente a partir de uma área definida por você. O Easy Overture facilita a obtenção de camadas geoespaciais atualizadas, ideais para uso em estudos urbanos, ambientais e de infraestrutura."
    }
]

st.markdown(CSS, unsafe_allow_html=True)

cols = st.columns(4, gap="medium")
for col, desc in zip(cols, descriptions):
    html = f"""
    <div class='card {desc['class']}'>
      <div class="badge">{desc['badge']}</div>
      <h3>{desc['title']}</h3>
      <div class="subtitle">Solução integrada para análise espacial</div>
      <p>{desc['text']}</p>
    </div>
    """
    col.markdown(html, unsafe_allow_html=True)

