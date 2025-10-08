import streamlit as st

pag_inicial = st.Page(
    page='pages/Boas_vindas.py',
    title='Boas Vindas!',
    icon=':material/home:',
    default=True
    )

pag_geocoding = st.Page(
    page='pages/Geocoding.py',
    title='Geocoding',
    icon=':material/globe_location_pin:',
    )

pag_reverse_geocoding = st.Page(
    page='pages/Reverse_Geocoding.py',
    title='Reverse Geocoding',
    icon=':material/travel_explore:',
    )

pag_directions = st.Page(
    page='pages/Directions.py',
    title='Directions',
    icon=':material/route:',
    )

pag_overturemaps = st.Page(
    page='pages/OvertureMaps.py',
    title='Overture Maps',
    icon=':material/south_america:',
    )

pag_clustering = st.Page(
    page='pages/Clustering_and_Routing.py',
    title='Clustering and Routing',
    icon=':material/globe_location_pin:',
    )

pg = st.navigation(pages=[pag_inicial, pag_geocoding, pag_reverse_geocoding, pag_directions, pag_overturemaps, pag_clustering])

pg.run()

