import os
from datetime import datetime

def quel_encoding(p_file,p_debug=False):

    r_encoding = ''
    encodings = ['utf-8', 'latin_1']  # add more
    for e in encodings:
        try:
            fh = open(p_file, 'r', encoding=e)
            fh.readlines()
            fh.seek(0)
            fh.close()

        except UnicodeDecodeError:
            if p_debug:
                print('got unicode error with %s , trying different encoding' % e)
        else:
            if p_debug:
                print('opening the file with encoding:  %s ' % e)
            r_encoding = e
            break

    return r_encoding

def isFileLF(p_file):
    _return = True
    with open(p_file, 'rb') as f:
        _lines_binaire = f.readlines()
        _idx = 0
        for _line_binaire in _lines_binaire:
            _idx += 1
            _line = _line_binaire
            if _line[-1:]==b'\n':
                # la ligne se termine par un CRLF donc KO
                if _line[-2:] == b'\r\n':
                    _return = False
                    break
            else:
                # Ligne non vide doit se terminer par un LF
                if _line!='':
                    _return = False
                    break

    return _return

def MyisNumber(p_string):
    _string = p_string.strip()
    _int = True

    try:
        _int = int(_string)
        _int = True
    except:
        _int = False

    return _int

def IsReal(p_string):
    _string = p_string.strip()
    _return = True

    _string = _string.replace(',','.')
    try:
        _int = float(_string)
    except:
        _return = False

    return _return

def StringToReal(p_string):

    _string = p_string.strip()
    _int = 0

    _string = _string.replace(',','.')
    try:
        _int = float(_string)
    except:
        _int = 0

    return _int


def decoupeTag(p_tag):
    _var = ''
    _value = ''

    if p_tag.count("=") == 1:
       _split = p_tag.split("=")
       _var = _split[0].strip()
       _value = _split[1]
    else:
        _var = p_tag
        _value = ''

    _var = _var.strip()
    _value = _value.strip()

    return _var,_value

def controleChamp(p_champName,p_champValue,p_champLenMax,p_champOBLIGATOIRE,
                  p_champListeValeursAutorisees,p_liste='',p_debug=False):

    _error = False
    _error_string = ''

    _liste_autorisee = ''
    if len(p_champListeValeursAutorisees) > 0:
        _liste_autorisee = ' ('+','.join(p_champListeValeursAutorisees)+')'

    _temp = p_champValue.strip()
    if len(_temp) > 0:
        if len(_temp) > p_champLenMax:
            _error = True
            _error_string = f"[{p_champName}] Champ limité à {p_champLenMax} caractère(s){_liste_autorisee}."
        else:
            if _temp not in p_champListeValeursAutorisees and len(p_champListeValeursAutorisees)>0 :
                _error = True
                _error_string = f"[{p_champName}] Valeur '{_temp}' non autorisée{_liste_autorisee}."
    else:
        if p_champOBLIGATOIRE:
            _error_string = (f"[{p_champName}] Champ obligatoire non renseigné{_liste_autorisee}.")
            _error = True
    if _error:
        if  p_liste != None:
            p_liste.append(_error_string)
        if p_debug:
            print(_error_string)

    return not _error

def ChampManquant(p_nom,p_flag,p_liste=''):
    if p_flag==0 and p_liste is not None:
        _error_string = f"[Structure incorrecte] : champ {p_nom} manquant."
        p_liste.append(_error_string)


def controleObstacle(p_repertoire,p_fichier,p_lines,p_liste_erreur,p_liste_sommet,p_liste_entite,p_dico_tags):

    K_HEADER_START = '[DESIGNATION]'
    K_HEADER_END = '[FIN FICHIER]'

    _return =  0

    _repertoire = p_repertoire
    _fichier = p_fichier

    _liste_erreur = p_liste_erreur
    _liste_sommet = p_liste_sommet
    _liste_entite = p_liste_entite
    _dico_tags = p_dico_tags

    if len(p_lines)>0:
        _lines = p_lines
        print(p_lines)
    else:
        # - le fichier existe ?
        _file = _repertoire + os.sep + _fichier

        if os.path.exists(_file) == False:
            _liste_erreur.append("[ERROR] Fichier non trouvé")
            return 10

        # - quel encodage
        encodings_type = quel_encoding(_file,False)

        if encodings_type == '':
            _liste_erreur.append("[ERROR] Encodage inconnu, attendu latin_1 (CP1252,ISO-8859-1)")
            return 10

        if encodings_type == 'utf-8':
            _liste_erreur.append("[ERROR] Encodage utf-8 interdit, attendu latin_1 (CP1252,ISO-8859-1)")
            return 10
        # --------------------------------------------------------------------------
        # On lit le fichier pour voir si fin de ligne est en LF ou CRLF
        # --------------------------------------------------------------------------
        _b_format_lf = isFileLF(_file)
        if not _b_format_lf:
            _liste_erreur.append("[ERROR] Fichier format CRLF, attendu LF")
            return 10

        with open(_file, 'r') as f:
            _lines = f.readlines()
    # --------------------------------------------------------------------------------
    # tout semble ok maintenant on va regarder le contenu du fichier
    # --------------------------------------------------------------------------------

    _file_nb_lines = len(_lines)
    for _idx in range(_file_nb_lines):
        _lines[_idx] = _lines[_idx].replace("\n","").replace("\r","")

    if _lines[0]!=K_HEADER_START:
        _liste_erreur.append("[ERROR] ce n'est pas un fichier obstacle")
        return 10

    if _lines[_file_nb_lines-1]!=K_HEADER_END:
        _liste_erreur.append("[ERROR] ce n'est pas un fichier obstacle")
        return 10

    # -- Initialisation des variables
    FLAG_NOM = 0
    FLAG_IDMETIER = 0
    FLAG_ANCIENNETE = 0
    FLAG_NATUREOBST = 0
    FLAG_AVISGABARIT = 0
    FLAG_NUMEROAVIS = 0
    FLAG_PKDEBUT = 0
    FLAG_PKFIN = 0
    FLAG_SITUATION = 0
    FLAG_ELECTRIFICATION = 0
    FLAG_DE_LA_VOIE = 0
    FLAG_LIBELLE_VOIE = 0
    FLAG_NOM_LOCAL_VOIE = 0
    FLAG_VOIE_DE_SERVICE = 0
    FLAG_SENS_CIRCULATION = 0
    FLAG_IPCS = 0
    FLAG_DE_LA_LIGNE = 0
    FLAG_DATERELEVE = 0
    FLAG_NBRDEBOUCHE = 0
    FLAG_OBS1 = 0
    FLAG_OBS2 = 0
    FLAG_OBS3 = 0
    FLAG_DEBOUCHE=0

    OBS_NOM = ''
    OBS_IDMETIER = ''
    OBS_ANCIENNETE = ''
    OBS_NATUREOBST = ''
    OBS_AVISGABARIT = ''
    OBS_NUMEROAVIS = ''
    OBS_PKDEBUT = ''
    OBS_PKFIN = ''
    OBS_SITUATION = ''
    OBS_ELECTRIFICATION = ''
    OBS_DE_LA_VOIE = ''
    OBS_LIBELLE_VOIE = ''
    OBS_NOM_LOCAL_VOIE = ''
    OBS_VOIE_DE_SERVICE = ''
    OBS_SENS_CIRCULATION = ''
    OBS_IPCS = ''
    OBS_DE_LA_LIGNE = ''
    OBS_DATERELEVE = ''
    OBS_NBRDEBOUCHE = 0
    OBS_OBS1 = ''
    OBS_OBS2 = ''
    OBS_OBS3 = ''

    # -------------------------------------------------------------------------------
    # Détermination s'il s'agit d'une suppression
    # -------------------------------------------------------------------------------
    FLAG_SUPPRESSION = 0

    for _line in _lines:
        _var,_value = decoupeTag(_line)
        if _var == 'ANCIENNETE':
            if _value == 'SUPPRESSION':
                FLAG_SUPPRESSION = 1
                FLAG_ANCIENNETE = 1

    # --------------------------------------------------------------------------------
    # - Recherche nombre de débouchés
    # - max = 1
    # --------------------------------------------------------------------------------
    _NbDebouche = 0
    _error = False

    for _line in _lines:
        _var,_value = decoupeTag(_line)

        if _var == 'NBRDEBOUCHE':
            FLAG_NBRDEBOUCHE = 1
            OBS_NBRDEBOUCHE = 0
            _error = not controleChamp("NBRDEBOUCHE", _value, 100, True, ['0','1'], _liste_erreur)
            if not _error:
                if MyisNumber(_value):
                    _NbDebouche = int(_value)
                    OBS_NBRDEBOUCHE = _NbDebouche
                else:
                    _NbDebouche = 0
                    _error = True
                    _error_string = f"[NBRDEBOUCHE] Valeur '{_value}' erronée."
                    _liste_erreur.append(_error_string)
                    break

    OBS_NBRDEBOUCHE = _NbDebouche

    if _error:
        return 10


    # -------------------------------------------------------------------------
    # Récupération des données
    # -------------------------------------------------------------------------
    FLAG_DEB_ALIGNEMENT = 0
    FLAG_DEB_COURBE_GAUCHE = 0
    FLAG_DEB_COURBE_DROITE = 0
    FLAG_DEB_SENSDEVERS = 0
    FLAG_DEB_DEVERS = 0
    FLAG_DEB_REPRESENTATION_TYPE = 0
    FLAG_DEB_NBRARC = 0
    FLAG_DEB_NBRSOMMET = 0

    DEB_ALIGNEMENT = ''
    DEB_COURBE_GAUCHE = 0
    COURBE_DROITE = 0
    DEB_SENSDEVERS = ''
    DEB_DEVERS = ''
    DEB_REPRESENTATION_TYPE = ''
    DEB_NBRARC = 0
    DEB_NBRSOMMET = 0

    # --------------------------------------------------------------------------
    # - Traitement d'un fichier obstacle
    # --------------------------------------------------------------------------
    if FLAG_SUPPRESSION == 1:
        # - Cas d'une suppression
        # - On recherche : NOM (50c ), IDMETIER ( 9c ),,

        for _line in _lines:
            _var, _value = decoupeTag(_line)

            if _var == 'NOM':
                FLAG_NOM = 1
                OBS_NOM = _value
                _error = not controleChamp("NOM", _value, 50, False, '', _liste_erreur)

            if _var == 'IDMETIER':
                FLAG_IDMETIER = 1
                OBS_IDMETIER = _value
                _error = not controleChamp("IDMETIER", _value, 9, False, '', _liste_erreur)

    else:
        # - Pas Suppression
        for _line in _lines:
            _var, _value = decoupeTag(_line)

            if _var == 'NOM':
                FLAG_NOM = 1
                OBS_NOM = _value
                _error = not controleChamp("NOM", _value, 50, False, '', _liste_erreur)

            if _var == 'IDMETIER':
                FLAG_IDMETIER = 1
                OBS_IDMETIER = _value
                _error = not controleChamp("IDMETIER", _value, 9, False, '', _liste_erreur)

            if _var == 'ANCIENNETE':
                FLAG_ANCIENNETE = 1
                OBS_ANCIENNETE = _value
                _error = not controleChamp("ANCIENNETE", _value, 11, True, ['NOUVEAU', 'EXISTANT', 'SUPPRESSION'],
                                           _liste_erreur)

            if _var == 'NATUREOBST':
                FLAG_NATUREOBST = 1
                OBS_NATUREOBST = _value
                _error = not controleChamp("NATUREOBST", _value, 10, True, ['DEFINITIF', 'PROVISOIRE'], _liste_erreur)

            if _var == 'AVISGABARIT':
                FLAG_AVISGABARIT = 1
                OBS_AVISGABARIT = _value
                _error = not controleChamp("AVISGABARIT", _value, 3, True, ['OUI', 'NON'], _liste_erreur)

            if _var == 'NUMEROAVIS':
                FLAG_NUMEROAVIS = 1
                OBS_AVISGABARIT = ''

            if _var == 'PKDEBUT':
                FLAG_PKDEBUT = 1
                OBS_PKDEBUT = 0
                _error = not controleChamp("PKDEBUT", _value, 100, True, '', _liste_erreur)
                if not _error:
                    if IsReal(_value):
                        OBS_PKDEBUT = StringToReal(_value) * 1000
                    else:
                        _error = True
                        _error_string = f"[PKDEBUT] Valeur '{_value}' erronée."
                        _liste_erreur.append(_error_string)

            if _var == 'PKFIN':
                FLAG_PKFIN = 1
                OBS_PKFIN = 0
                _error = not controleChamp("PKFIN", _value, 100, True, '', _liste_erreur)
                if not _error:
                    if IsReal(_value):
                        OBS_PKFIN = StringToReal(_value) * 1000
                    else:
                        _error = True
                        _error_string = f"[PKFIN] Valeur '{_value}' erronée."
                        _liste_erreur.append(_error_string)

            if _var == 'SITUATION':
                FLAG_SITUATION = 1
                OBS_SITUATION = _value
                _error = not controleChamp("SITUATION", _value, 4, True, ['GARE', 'VOIE'], _liste_erreur)

            if _var == 'ELECTRIFICATION':
                FLAG_ELECTRIFICATION = 1
                OBS_ELECTRIFICATION = _value
                _error = not controleChamp("ELECTRIFICATION", _value, 3, True, ['OUI', 'NON'], _liste_erreur)

            if _var == 'DE LA VOIE':
                FLAG_DE_LA_VOIE = 1
                OBS_DE_LA_VOIE = _value
                _error = not controleChamp("DE LA VOIE", _value, 6, True, '', _liste_erreur)

            if _var == 'LIBELLE VOIE':
                FLAG_LIBELLE_VOIE = 1
                OBS_LIBELLE_VOIE = _value
                _error = not controleChamp("LIBELLE VOIE", _value, 120, False, '', _liste_erreur)

            if _var == 'NOM LOCAL VOIE':
                FLAG_NOM_LOCAL_VOIE = 1
                OBS_NOM_LOCAL_VOIE = _value
                _error = not controleChamp("NOM LOCAL VOIE", _value, 6, False, '', _liste_erreur)

            if _var == 'VOIE DE SERVICE':
                FLAG_VOIE_DE_SERVICE = 1
                OBS_VOIE_DE_SERVICE = _value
                _error = not controleChamp("VOIE DE SERVICE", _value, 3, True, ['OUI', 'NON'], _liste_erreur)

            if _var == 'SENS CIRCULATION':
                FLAG_SENS_CIRCULATION = 1
                OBS_SENS_CIRCULATION = _value
                _error = not controleChamp("SENS CIRCULATION", _value, 11, True, ['CROISSANT', 'DECROISSANT', 'BANALISE'],
                                           _liste_erreur)

            if _var == 'IPCS':
                FLAG_IPCS = 1
                OBS_IPCS = _value
                _error = not controleChamp("IPCS", _value, 3, True, ['OUI', 'NON'], _liste_erreur)

            if _var == 'DE LA LIGNE':
                FLAG_DE_LA_LIGNE = 1
                OBS_DE_LA_LIGNE = _value
                _error = not controleChamp("DE LA LIGNE", _value, 6, True, '', _liste_erreur)

            if _var == 'DATERELEVE':
                FLAG_DATERELEVE = 1
                OBS_DATERELEVE = _value
                _error = not controleChamp("DATERELEVE", _value, 10, True, '', _liste_erreur)

                if not _error:
                    # CONTROLE DATERELEVE format attendu JJ-MM-AAAA
                    date_format = '%d-%m-%Y'
                    try:
                        date_obj = datetime.strptime(_value, date_format)
                    except:
                        _error = True
                        _error_string = f"[DATERELEVE] Valeur '{_value}' non autorisée, format attendu JJ-MM-AAAA."
                        _liste_erreur.append(_error_string)

            if _var == 'NBRDEBOUCHE':
                FLAG_NBRDEBOUCHE = 1
                OBS_NBRDEBOUCHE = _value
                _error = not controleChamp("NBRDEBOUCHE", _value, 1, True, ['0', '1'], _liste_erreur)

            if _var == 'OBS1':
                FLAG_OBS1 = 1
                OBS_OBS1 = _value
                _error = not controleChamp("OBS1", _value, 50, True, '', _liste_erreur)

            if _var == 'OBS2':
                FLAG_OBS2 = 1
                OBS_OBS2 = _value
                _error = not controleChamp("OBS2", _value, 50, True, '', _liste_erreur)

            if _var == 'OBS3':
                FLAG_OBS3 = 1
                OBS_OBS3 = _value
                _error = not controleChamp("OBS3", _value, 50, True, '', _liste_erreur)

    # ---------------------------------------------------------------------------------------------
    # chargement du débouché 1
    # ---------------------------------------------------------------------------------------------
    _mode_debouche = False
    _tag = '[DEBOUCHE N°1]'

    # --------------------------------------------------------------------------------------------
    # on recherche le nombre de sommets du débouché 1
    # --------------------------------------------------------------------------------------------

    for _line in _lines:
        _var, _value = decoupeTag(_line)

        if _var == _tag:
            _mode_debouche = True

        if _var == 'NBRSOMMET':
            FLAG_DEB_NBRSOMMET = 1
            DEB_NBRSOMMET = 0
            _error = not controleChamp("NBRSOMMET", _value, 3, True, '', _liste_erreur)

            if not _error:
                if MyisNumber(_value):
                    _int = int(_value)
                    DEB_NBRSOMMET = _int

                    if _int < 2 or _int > 200:
                        _error = True
                        _error_string = f"[NBRSOMMET] Valeur '{_value}' non autorisée, compris en 2 et 200."
                        _liste_erreur.append(_error_string)

    if not _mode_debouche and DEB_NBRSOMMET>0:
        _liste_erreur.append("[DEBOUCHE N°1] tag non trouvé dans le fichier.")

    _mode_debouche = False

    for _line in _lines:
        _var, _value = decoupeTag(_line)

        if _var == _tag:
            _mode_debouche = True

        if _mode_debouche:
            if _var == 'ALIGNEMENT':
                FLAG_DEB_ALIGNEMENT = 1
                DEB_ALIGNEMENT = ''
                _error = not controleChamp("ALIGNEMENT", _value, 3, True, ['OUI', 'NON'], _liste_erreur)

            # --- Courbe gauche -1 ou 70 99999
            if _var == 'COURBE GAUCHE':
                FLAG_DEB_COURBE_GAUCHE = 1
                DEB_COURBE_GAUCHE = 0
                _error = not controleChamp("COURBE GAUCHE", _value, 5, True, '', _liste_erreur)
                if not _error:
                    if MyisNumber(_value):
                        _int = int(_value)
                        DEB_COURBE_GAUCHE = _int

                        if not (_int == -1 or (_int >= 70 and _int <= 99999)):
                            _error = True
                            _error_string = f"[COURBE GAUCHE] Valeur '{_value}' non autorisée, -1 ou compris en 70 et 99999."
                            _liste_erreur.append(_error_string)

            # --- Courbe droite -1 ou 70 99999
            if _var == 'COURBE DROITE':
                FLAG_DEB_COURBE_DROITE = 1
                DEB_COURBE_DROITE = 0
                _error = not controleChamp("COURBE DROITE", _value, 5, True, '', _liste_erreur)
                if not _error:
                    if MyisNumber(_value):
                        _int = int(_value)
                        DEB_COURBE_DROITE = _int
                        if not (_int == -1 or (_int >= 70 and _int <= 99999)):
                            _error = True
                            _error_string = f"[COURBE DROITE] Valeur '{_value}' non autorisée, -1 ou compris en 70 et 99999."
                            _liste_erreur.append(_error_string)

            if _var == 'SENSDEVERS':
                FLAG_DEB_SENSDEVERS = 1
                DEB_SENSDEVERS = ''
                _error = not controleChamp("SENSDEVERS", _value, 6, True, ['DROITE', 'GAUCHE', 'ZERO'], _liste_erreur)

            if _var == 'DEVERS':
                FLAG_DEB_DEVERS = 1
                DEB_DEVERS = _value
                _error = not controleChamp("DEVERS", _value, 1, True, ['0'], _liste_erreur)

            if _var == 'REPRESENTATION TYPE':
                FLAG_DEB_REPRESENTATION_TYPE = 1
                DEB_REPRESENTATION_TYPE = _value
                _error = not controleChamp("REPRESENTATION TYPE", _value, 7, True, ['PLANCHE'], _liste_erreur)

            if _var == 'NBRARC':
                FLAG_DEB_NBRARC = 1
                DEB_NBRARC = _value
                _error = not controleChamp("NBRARC", _value, 1, True, ['0'], _liste_erreur)

    # --------------------------------------------------------------------------------------------------------------------
    # On traite les données ENTITE et SOMMET
    # ---------------------------------------------------------------------------------------------------------------------
    _mode_debouche = False

    _record = {}
    _next_idx = 0
    _current_sommet = 0
    _set_sommet = set()
    _set_entite = set()
    _line_cpt = 0

    for _line in _lines:
        _var, _value = decoupeTag(_line)
        _line_cpt += 1

        if _var == _tag:
            _mode_debouche = True

        if _mode_debouche:
            if len(_var) > 6:
                if _var[:6] == 'SOMMET':
                    _current_sommet = 0
                    _next_idx += 1
                    if _var in _set_sommet:
                        _error = True
                        _error_string = f"[{_var}] déja présent."
                        _liste_erreur.append(_error_string)
                    else:
                        _set_sommet.add(_var)
                        _idx_temp = _var[6:]
                        if not MyisNumber(_idx_temp):
                            _error = True
                            _error_string = f"[{_var}] format incorrect."
                            _liste_erreur.append(_error_string)
                        else:
                            _idx = int(_idx_temp)
                            if _idx != _next_idx:
                                _error = True
                                _error_string = f"[{_var}] erreur de séquence dans la description de l'obstacle, attendu {_next_idx}."
                                _liste_erreur.append(_error_string)
                            else:
                                _current_sommet = _idx
                                # -- on test si les coordonnées sont valides
                                _x = 0.0
                                _y = 0.0
                                if '|' not in _value or len(_value.split("|")) != 2:
                                    _error = True
                                    _error_string = f"[{_var}] format de donnée inconnue, attendu xxx.xxx|yyy.yyy."
                                    _liste_erreur.append(_error_string)
                                else:
                                    _data = _value.split("|")
                                    if not IsReal(_data[0]) or not IsReal(_data[1]):
                                        _error = True
                                        _error_string = f"[{_var}] format de donnée inconnue, attendu xxx.xxx|yyy.yyy."
                                        _liste_erreur.append(_error_string)
                                    else:
                                        # -- enfin les x et y semblent corrects
                                        _x = StringToReal(_data[0])
                                        _y = StringToReal(_data[1])
                                        _record = {'line': _line_cpt, 'idx': _idx, 'name': _var, 'x': _x, 'y': _y}
                                        _liste_sommet.append(_record)

                if _var[:6] == 'ENTITE':
                    if not (_var not in _set_entite):
                        _error = True
                        _error_string = f"[{_var}] déja présent."
                        _liste_erreur.append(_error_string)
                    else:
                        _set_entite.add(_var)
                        _idx_temp = _var[6:]
                        if not MyisNumber(_idx_temp):
                            _error = True
                            _error_string = f"[{_var}] format incorrect."
                            _liste_erreur.append(_error_string)
                        else:
                            _idx = int(_idx_temp)
                            if _idx != _current_sommet:
                                _error = True
                                _error_string = f"[{_var}] erreur de séquence dans la description de l'obstacle, attendu {_current_sommet}."
                                _liste_erreur.append(_error_string)
                            else:
                                _current_entite = _idx_temp
                                # -- on test si les coordonnées sont valides
                                _error = not controleChamp(_var, _value, 7, True, ['SEGMENT', 'FIN'], _liste_erreur)
                                if not _error:
                                    _record = {'line': _line_cpt, 'idx': _idx, 'name': _var, 'type': _value}
                                    _liste_entite.append(_record)
            pass

    # -----------------------------------------------------------------------------------
    # Test les données manquantes
    # -----------------------------------------------------------------------------------

    ChampManquant("NOM", FLAG_NOM, _liste_erreur)
    ChampManquant("IDMETIER", FLAG_IDMETIER, _liste_erreur)
    ChampManquant("ANCIENNETE", FLAG_ANCIENNETE, _liste_erreur)

    if FLAG_SUPPRESSION == 0:
        ChampManquant("NATUREOBST", FLAG_NATUREOBST, _liste_erreur)
        ChampManquant("AVISGABARIT", FLAG_AVISGABARIT, _liste_erreur)
        ChampManquant("PKDEBUT", FLAG_PKDEBUT, _liste_erreur)
        ChampManquant("PKFIN", FLAG_PKFIN, _liste_erreur)
        ChampManquant("SITUATION", FLAG_SITUATION, _liste_erreur)
        ChampManquant("ELECTRIFICATION", FLAG_ELECTRIFICATION, _liste_erreur)
        ChampManquant("DE LA VOIE", FLAG_DE_LA_LIGNE, _liste_erreur)
        ChampManquant("LIBELLE VOIE", FLAG_LIBELLE_VOIE, _liste_erreur)
        ChampManquant("NOM LOCAL VOIE", FLAG_NOM_LOCAL_VOIE, _liste_erreur)
        ChampManquant("VOIE DE SERVICE", FLAG_VOIE_DE_SERVICE, _liste_erreur)
        ChampManquant("SENS CIRCULATION", FLAG_SENS_CIRCULATION, _liste_erreur)
        ChampManquant("IPCS", FLAG_IPCS, _liste_erreur)

        ChampManquant("DE LA LIGNE", FLAG_DE_LA_LIGNE, _liste_erreur)
        ChampManquant("DATERELEVE", FLAG_DATERELEVE, _liste_erreur)
        ChampManquant("NBRDEBOUCHE", FLAG_NBRDEBOUCHE, _liste_erreur)

        ChampManquant("OBS1", FLAG_OBS1, _liste_erreur)
        ChampManquant("OBS2", FLAG_OBS2, _liste_erreur)
        ChampManquant("OBS3", FLAG_OBS3, _liste_erreur)

        ChampManquant("ALIGNEMENT", FLAG_DEB_ALIGNEMENT, _liste_erreur)
        ChampManquant("COURBE GAUCHE", FLAG_DEB_COURBE_GAUCHE, _liste_erreur)
        ChampManquant("COURBE DROITE", FLAG_DEB_COURBE_DROITE, _liste_erreur)

        ChampManquant("SENSDEVERS", FLAG_DEB_SENSDEVERS, _liste_erreur)
        ChampManquant("DEVERS", FLAG_DEB_DEVERS, _liste_erreur)
        ChampManquant("REPRESENTATION TYPE", FLAG_DEB_REPRESENTATION_TYPE, _liste_erreur)

        ChampManquant("NBRARC", FLAG_DEB_NBRARC, _liste_erreur)
        ChampManquant("NBRSOMMET", FLAG_DEB_NBRSOMMET, _liste_erreur)
        ChampManquant("OBS3", FLAG_OBS3, _liste_erreur)

    # -- test la cohérence des points du débouché
    # dans _liste_sommet tous les sommets
    # dans _liste_entite, le entités associées

    if DEB_NBRSOMMET > 0:
        _error_2 = False

        if len(_liste_sommet) != DEB_NBRSOMMET:
            _error = True
            _error_2 = True
            _liste_erreur.append(f"[DEBOUCHE] Nombre de SOMMETxxx <> nombre de sommets déclarés dans NBRSOMMET.")

        if len(_liste_entite) != DEB_NBRSOMMET:
            _error = True
            _error_2 = True
            _liste_erreur.append(f"[DEBOUCHE] Nombre de ENTITExxx <> nombre de sommets déclarés dans NBRSOMMET.")

        if not _error_2:
            # -- on regarde si la balise de fin est bien présente
            if _liste_entite[-1]['type'] != 'FIN':
                _liste_erreur.append(f"[DEBOUCHE] Il manque la balise de fermeture ENTITTExxx=FIN.")

            # -- on controle si pour chaque ENTITExxx il y a un SOMMETxxx
            for _idx in range(DEB_NBRSOMMET):
                _entite = _liste_entite[_idx]['name']
                _sommet = _liste_sommet[_idx]['name']
                if _entite[6:] != _sommet[6:]:
                    _liste_erreur.append(f"[DEBOUCHE] incohérence {_entite} et {_sommet}")

            pass

    # - on enregistre tous les tags du fichier:
    _idx_line = 0
    for _line in _lines:
        _var, _value = decoupeTag(_line)
        _idx_line += 1
        _record = {"line": _idx_line, "tag": _var, "value": _value}
        if _dico_tags is not None:
            _dico_tags[_var] = _value


if __name__ == "__main__":
    # execute only if run as a script
    _repertoire = 'data' + os.sep + 'BINOD_REJET'
    _fichier = '001040_PN-110920231512.TXT;1'
    print(_fichier)

    _liste_erreur = []
    _dico_tags = {}
    _liste_sommet = []
    _liste_entite = []

    controleObstacle(_repertoire, _fichier, '',_liste_erreur, _liste_sommet, _liste_entite, _dico_tags)
    print("------------> les erreurs ")
    for _erreur in _liste_erreur:
        print(_erreur)
