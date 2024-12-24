import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

st.set_page_config(layout="wide")

# If you want to use the no-sections version, this
# defaults to looking in .streamlit/pages.toml, so you can
# just call `get_nav_from_toml()`
nav = get_nav_from_toml("gui/.streamlit/pages_sections.toml")

st.logo("data/TQDN_1/page_1.png")

pg = st.navigation(nav)

add_page_title(pg)

pg.run()