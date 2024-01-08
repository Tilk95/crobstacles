import streamlit as st
import crobstacles
import os
from io import StringIO


st.set_page_config(layout="wide")

st.header("CONTROLE DES FICHIERS OBSTACLES")

def isFileLF(p_lines):
    _return = True
    for _line in p_lines:
        if _line[-1:] == '\n':
            # la ligne se termine par un CRLF donc KO
            if _line[-2:] == '\r\n':
                _return = False
                break
    return _return

def isOuvrable():
    return True

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
#    st.write(uploaded_file)

    _name = uploaded_file.name
#    st.write(uploaded_file.readlines())
#    bytes_data = uploaded_file.read()
#    st.code(bytes_data)

    # To convert to a string based IO:
#    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#    st.write(stringio)

    # To convert to a string based IO:

    stringio = StringIO(uploaded_file.getvalue().decode("latin_1"))
    string_datas = stringio.readlines()

    if not isFileLF(string_datas):
        st.error("Ce n'est pas un format LF.")

    _liste_erreur = []
    _dico_tags = {}
    _liste_sommet = []
    _liste_entite = []

    crobstacles.controleObstacle("", "", string_datas, _liste_erreur, _liste_sommet, _liste_entite, _dico_tags)

    if len(_liste_erreur)>0:
        st.subheader("Liste des anomalies")
        st.write(_liste_erreur)
    st.subheader("Liste des champs dans le fichier")
    st.write(string_datas)

    st.stop()

pass
st.stop()


_repertoire = 'data' + os.sep + 'BINOD_REJET'
_fichier = '001040_PN-110920231512.TXT;1'
print(_fichier)

_liste_erreur = []
_dico_tags = {}
_liste_sommet = []
_liste_entite = []

crobstacles.controleObstacle(_repertoire, _fichier,'', _liste_erreur, _liste_sommet, _liste_entite, _dico_tags)

st.write(_liste_erreur)

print("------------> les erreurs ")
for _erreur in _liste_erreur:
    print(_erreur)
