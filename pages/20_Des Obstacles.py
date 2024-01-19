import streamlit as st
import crobstacles
import os
from io import StringIO
import pandas as pd


st.set_page_config(layout="wide")

st.header("Contrôler DES fichiers obstacle :book:")

def returnTagValue(p_tag_name,p_liste_tags):
    if p_tag_name in p_liste_tags:
        if p_liste_tags[p_tag_name] == '':
            return '*vide*'
        return p_liste_tags[p_tag_name]
    else:
        return "absent"


def listeErrorToPanda(p_liste_errors,p_panda):
    st.write("Errors")

    _idx = 0

    for _error in p_liste_errors:
        _idx += 1
        _value = {'CHAMP':_idx,'VALEUR':_error}
#        p_panda.(_value)


    st.write(p_panda)

    pass

def voirEnteteObstacle(p_liste_tags,p_error):
    st.divider()
    _color = 'green'
    if p_error is True:
        _color = 'red'

    _text =f'#### NOM OBSTACLE : :{_color}[{returnTagValue("NOM",p_liste_tags)}]'
    st.markdown(_text)
    _text = f"ID METIER : :blue[{returnTagValue('IDMETIER',p_liste_tags)}]"

    _text += f" | ANCIENNETE : :blue[{returnTagValue('ANCIENNETE',p_liste_tags)}]"
    _text += f" | NATURE OBSTACLE : :blue[{returnTagValue('NATUREOBST',p_liste_tags)}]"
    _text += f" | NOMBRE DE DEBOUCHES : :blue[{returnTagValue('NBRDEBOUCHE',p_liste_tags)}]"
    _text += f" | NOMBRE DE SOMMETS : :blue[{returnTagValue('NBRSOMMET',p_liste_tags)}]"

    st.markdown(_text)

    _text = f"DE LA LIGNE : :blue[{returnTagValue('DE LA LIGNE',p_liste_tags)}]"
    _text += f" | PKDEBUT : :blue[{returnTagValue('PKDEBUT',p_liste_tags)}]"
    _text += f" | PKFIN : :blue[{returnTagValue('PKFIN',p_liste_tags)}]"
    st.markdown(_text)

    _text = f"DE LA VOIE : :blue[{returnTagValue('DE LA VOIE',p_liste_tags)}]"
    _text += f" | LIBELLE VOIE : :blue[{returnTagValue('LIBELLE VOIE',p_liste_tags)}]"
    _text += f" | NOM LOCAL VOIE : :blue[{returnTagValue('NOM LOCAL VOIE',p_liste_tags)}]"
    _text += f" | VOIE DE SERVICE : :blue[{returnTagValue('VOIE DE SERVICE',p_liste_tags)}]"

    st.markdown(_text)

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

#-------------------------------------------------------------------------------------------------
# lecture des fichiers OBSTACLES
#-------------------------------------------------------------------------------------------------

uploaded_files = st.file_uploader("Choisissez un fichier obstacle à analyser",accept_multiple_files=True)

if len(uploaded_files) <= 0:
    st.stop()

# ------------------------------------------------------------------------
# on analyse tous les fichiers
# ------------------------------------------------------------------------
_liste_files = []
_cpt_fichiers = 0
_cpt_erreurs = 0

pandaPDFiles = pd.DataFrame(columns=["Valide", "OBSTACLE", "LF", "Fichier OBSTACLE","Nom","NB SOMMETS","NB d'Erreurs","Description des erreurs"])

for uploaded_file in uploaded_files:

    _cpt_fichiers+=1
    _liste_erreur = []
    _dico_tags = {}
    _liste_sommet = []
    _liste_entite = []

    #st.text(uploaded_file.name)
    _error = False

    # - Lecture du fichier pour contrôle LF
    stringio = StringIO(uploaded_file.getvalue().decode("latin_1"))
    string_datas = stringio.readlines()
    _b_fichier_mode_lf = True

    if not isFileLF(string_datas):
        _b_fichier_mode_lf = False
        _error = True
#        st.error("Ce n'est pas un format LF.")

    # ---- Controle le fichier ---------------

    _return = crobstacles.controleObstacle("", "", string_datas, _liste_erreur, _liste_sommet, _liste_entite, _dico_tags)

    # -- test si fichier type obstacle

    _b_fichier_obstacle = True
    if _return == 99:
        _error = True
        _b_fichier_obstacle = False
#        st.error("Ce n'est pas un fichier OBSTACLE.")

    if len(_liste_erreur)>0:
        _error = True

    _record = []

    _st_ok = 'O'
    if not _error:
        _record.append("OUI")
    else:
        _record.append("NON")
        _cpt_erreurs+=1

    if _b_fichier_obstacle:
        _record.append("OUI")
    else:
        _record.append("NON")

    if _b_fichier_mode_lf:
        _record.append("OUI")
    else:
        _record.append("NON")

    _record.append(uploaded_file.name)
    try:
        _nom = _dico_tags["NOM"]
        _record.append(_nom)
    except:
        _record.append("<non trouvé>")

    try:
        _nbrsommet = _dico_tags["NBRSOMMET"]
        _record.append(str(_nbrsommet))
    except:
        _record.append("<non trouvé>")

    # - les erreurs
    if len(_liste_erreur)>0:
        _record.append(str(len(_liste_erreur)))
#        _record.append(_liste_erreur)
        _record.append(';'.join(_liste_erreur))
    else:
        _record.append("")
        _record.append("")

    pandaPDFiles.loc[len(pandaPDFiles)] = _record



st.divider()

if _cpt_erreurs>0:
    _text = f"## :red[{_cpt_erreurs} Anomalie(s) détectée(s) dans {_cpt_fichiers}.] :sob:"
else:
    _text = f"## :green[ 0 Anomalie dans les {_cpt_fichiers}] fiches obstacles :+1:"

st.markdown(_text)


st.dataframe(
    pandaPDFiles,
    hide_index = False
)

