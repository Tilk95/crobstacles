import streamlit as st
import crobstacles
import os
from io import StringIO
import pandas as pd


st.set_page_config(layout="wide")

st.header("CONTROLE DES FICHIERS OBSTACLES")

def returnTagValue(p_tag_name,p_liste_tags):
    if p_tag_name in p_liste_tags:
        if p_liste_tags[p_tag_name] == '':
            return '*vide*'
        return p_liste_tags[p_tag_name]
    else:
        return "absent"

def voirEnteteObstacle(p_liste_tags,p_error):
    st.divider()
    _color = 'green'
    if p_error is True:
        _color = 'red'

    _text =f'#### NOM OBSTACLE : :{_color}[{returnTagValue("NOM",p_liste_tags)}]'
    st.markdown(_text)
    _text = f"ID METIER : :blue[{returnTagValue("IDMETIER",p_liste_tags)}]"
    _text += f" | ANCIENNETE : :blue[{returnTagValue("ANCIENNETE",p_liste_tags)}]"
    _text += f" | NATURE OBSTACLE : :blue[{returnTagValue("NATUREOBST",p_liste_tags)}]"
    _text += f" | NOMBRE DE DEBOUCHES : :blue[{returnTagValue("NBRDEBOUCHE",p_liste_tags)}]"
    _text += f" | NOMBRE DE SOMMETS : :blue[{returnTagValue("NBRSOMMET",p_liste_tags)}]"

    st.markdown(_text)

    _text = f"DE LA LIGNE : :blue[{returnTagValue("DE LA LIGNE",p_liste_tags)}]"
    _text += f" | PKDEBUT : :blue[{returnTagValue("PKDEBUT",p_liste_tags)}]"
    _text += f" | PKFIN : :blue[{returnTagValue("PKFIN",p_liste_tags)}]"
    st.markdown(_text)

    _text = f"DE LA VOIE : :blue[{returnTagValue("DE LA VOIE",p_liste_tags)}]"
    _text += f" | LIBELLE VOIE : :blue[{returnTagValue("LIBELLE VOIE",p_liste_tags)}]"
    _text += f" | NOM LOCAL VOIE : :blue[{returnTagValue("NOM LOCAL VOIE",p_liste_tags)}]"
    _text += f" | VOIE DE SERVICE : :blue[{returnTagValue("VOIE DE SERVICE",p_liste_tags)}]"

    st.markdown(_text)


    st.divider()


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

uploaded_file = st.file_uploader("Choisissez un fichier obstacle à analyser")
if uploaded_file is not None:
#    st.write(uploaded_file)

    _error = False

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
        _error = True
        st.error("Ce n'est pas un format LF.")

    _liste_erreur = []
    _dico_tags = {}
    _liste_sommet = []
    _liste_entite = []

    _return = crobstacles.controleObstacle("", "", string_datas, _liste_erreur, _liste_sommet, _liste_entite, _dico_tags)

    if _return == 99:
        _error = True
        st.error("Ce n'est pas un fichier OBSTACLE.")
        st.stop()

    if len(_liste_erreur) > 0:
        _error = True

    if _dico_tags is not None:
        voirEnteteObstacle(_dico_tags,_error)


    if len(_liste_erreur) > 0:
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
