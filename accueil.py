import streamlit as st

st.set_page_config(
   page_title="CR OBSTACLES",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)


st.header(":steam_locomotive: Outils de contrôle des fiches obstacles format BINOD.. ")
st.write("Outil permettant de contrôler si un fichier texte respecte le format attendu dans l'interface CRETE -> BINOD")

st.subheader(":scroll: Historique des versions")
st.text("19/01/2024 - v1.01 : Gestion erreur sur les points successifs identiques.")
st.text("02/01/2024 - v1.01 : Ajout contrôle Des Obstacles.")
st.text("10/12/2023 - v1.00 : Version initiale.")

