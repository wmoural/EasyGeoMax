import streamlit as st

pag_inicial = st.Page(
    page='paginas/Boas_vindas.py',
    title='Boas Vindas!',
    icon=':material/home:',
    default=True
    )

pag_geocoding = st.Page(
    page='paginas/Geocoding.py',
    title='Geocoding',
    icon=':material/globe_location_pin:',
    )

pag_reverse_geocoding = st.Page(
    page='paginas/Reverse_Geocoding.py',
    title='Reverse Geocoding',
    icon=':material/travel_explore:',
    )

pag_directions = st.Page(
    page='paginas/Directions.py',
    title='Directions',
    icon=':material/route:',
    )

pag_overturemaps = st.Page(
    page='paginas/OvertureMaps.py',
    title='Overture Maps',
    icon=':material/south_america:',
    )


pg = st.navigation(paginas=[pag_inicial, pag_geocoding, pag_reverse_geocoding, pag_directions, pag_overturemaps])

pg.run()



