from copy import deepcopy
import sys, os, zipfile, json, shutil
# from main import GUI

def controler_arg_file_mscz():
    """
    with the execution command, the mscz file can be optionnally indicated. (otherwise, it is done later in the code). If the file is given, the code controls that it exists
    Returns:
        mscz_file_indicated: bool     # True if a mscz file was indicated and that it exists
        mscz_file: string             # gives the path and name of the mscz file if indicated, else empty string
    """
    import sys
    # print(sys.argv)
    mscz_file_indicated =False
    for k,i in enumerate(sys.argv[1:]):
        if i=="-f":
            mscz_file = sys.argv[k+1]
            mscz_file_indicated =True
            break
    if mscz_file_indicated ==True:
        if mscz_file.endswith(".mscz") and os.path.isfile(mscz_file):
            # l'extension du fichier correspond, et le fichier existe
            return mscz_file_indicated, mscz_file
    return False, ""

# controler_arg_file_mscz()

def controler_arg_fichier_json():
    
    """
    with the execution command, a json file can be optionnally indicated to give predetermined parameters. If the file is given, the code controls that it exists
    Returns:
        json_param_exists: bool     # True if a JSON file was indicated and that it exists
        json_file: string           # gives the path and name of the JSON file if indicated, else empty string
    """
    import sys
    # print(sys.argv)
    json_param_exists =False
    for k,i in enumerate(sys.argv[1:]):
        if i=="-p":
            json_file = sys.argv[k+1]
            json_param_exists =True
            break
    if json_param_exists ==True:
        if json_file.endswith(".json") and os.path.isfile(json_file):
            # l'extension du fichier correspond, et le fichier existe
            return json_param_exists, json_file
    return False, ""

def generate_json_job_file(liste_fichiers_mscz, dir_mscz):
    """
    generates the Json batch file. It contains the mscz files to convert into mp3. By default, there will be 1 pair of mscz/mp3 file per voices and 1 pair of tutti
    The mp3 files will have the same name as their mscz counterpart
    
    Arguments:
        liste_fichiers_mscz: list(string)       # list of the mscz files
        dir_mscz: string                        # location of the original mscz. Also the location where the json file will be saved
    
    Returns:
        json_file: string               # path to the json_file

    The command to execute the conversion is of the type 'mscore -j file.json'
    The structure of the json file is the following : from https://musescore.org/en/handbook/3/command-line-options#EXAMPLES
    #
        [
            {
                "in": "Reunion.mscz",
                "out": "Reunion-coloured.pdf",
                "plugin": "colornotes.qml"
            },
            {
                "in": "Reunion.mscz",
                "out": [
                "Reunion.pdf",
                [ "Reunion (part for ", ").pdf" ],
                "Reunion.musicxml",
                "Reunion.mid"
                ]
            },
            {
                "in": "Piece with excerpts.mscz",
                "out": [
                "Piece with excerpts (Partitura).pdf",
                [ "Piece with excerpts (part for ", ").pdf" ],
                "Piece with excerpts.mid"
                ]
            }
        ]
    """
    content_json = \
    "[\n"
    for k,i in enumerate(liste_fichiers_mscz):
        input_file = i
        output_file = input_file.replace(".mscz",".mp3")
        content_json += \
        "   {\n" + \
        f"        \"in\":\"{input_file}\",\n" + \
        f"        \"out\":\"{output_file}\"\n"
        if k+1<len(liste_fichiers_mscz):
            content_json += "   },\n"
        else:
            content_json += "   }\n" # pas de virgule si c'est le dernier élément de la liste

    content_json+= "]"
    from file_manip_functions import save_json # est-ce que c'est nécessaire ?
    json_file = save_json(content_json, dir_mscz)
    return json_file

def generate_volume_matrix(volume_voix_acc, volume_voix_sec, liste_name_id, correspondance_id_initial_incremente, list_voix_accompagnement, gen_tutti):
    # correspondance_id_initial_incremente prend en compte la méthode des accord, mais prend-elle en compte la méthode MS ? à vérifier
    liste_voix_principales = []
    for j in correspondance_id_initial_incremente:
        id_initial =j[0]
        is_accompagnement = False
        for i in list_voix_accompagnement:
            if id_initial == i[1]:
                is_accompagnement=True
                break
        if not is_accompagnement:
            nb_ss_voix = len(j[3])
            for k in range(nb_ss_voix):
                id_new = j[2][k]
                name_new = j[3][k]
                liste_voix_principales.append([id_new, name_new])
    # chaque ligne i de matrice de volume correspond à une voix principale. Chaque élément i,j correspond au volume de la voix j (qui comprend également les voix d'accompagnement) dans le fichier de travail de la voix principale i
    # L'ordre des colonnes est voix principale dans le même ordre que les lignes, puis les voix d'accompagnement
    # le volume vaut 100% (volume de la voix principale dans son fichier de travail) lorsque i==j
    # le volume vaut volume_voix_sec si i!=j et j<=len(liste_voix_principale)
    # le volume vaut volume_voix_acc si j>len(liste_voix_principale)
    matrix = []
    for k_i, i in enumerate(liste_voix_principales):
        ligne_volume = ""
        for k_j, j in enumerate(liste_voix_principales):
            if k_i == k_j: # volume de la voix principale dans son fichier audio
                ligne_volume+= "100 "
                # intitule_lignes_matrix.append(j[1])
                # intitule_colonne_matrix.append(j[1])
            else:
                ligne_volume+= f"{volume_voix_sec} "
                # intitule_lignes_matrix.append(j[1])
                # intitule_colonne_matrix.append(j[1])
        for k_j, j in enumerate(list_voix_accompagnement, k_j+1):
            # intitule_colonne_matrix.append(j[0])
            ligne_volume+=f"{volume_voix_acc} "
        matrix.append(ligne_volume)

    if gen_tutti:
        ligne_volume = ""
        for i in liste_voix_principales:
            ligne_volume+= f"{volume_voix_sec} "
        for i in list_voix_accompagnement:
            ligne_volume+=f"{volume_voix_acc} "
        matrix.append(ligne_volume)

    intitule_lignes_matrix = []
    intitule_colonne_matrix = []
    for j in liste_voix_principales:
            intitule_lignes_matrix.append(j[1])
            intitule_colonne_matrix.append(j[1])
    for j in list_voix_accompagnement:
        intitule_colonne_matrix.append(j[0])
    if gen_tutti:
        intitule_lignes_matrix.append("tutti")

    return matrix, intitule_lignes_matrix, intitule_colonne_matrix

def get_voix_accompagnement(liste_name_id, Fenetre_2, GUI_parameters, GUI):
    
    list_voices = []
    for i in liste_name_id:
        list_voices.append(i[0])
    if GUI:
        app2 = Fenetre_2(GUI_parameters, list_voices)
        app2.run()
        list_voix_accompagnement = app2.selected_options
        for j in range(len(list_voix_accompagnement)):
            voix = list_voix_accompagnement[j]
            for k in liste_name_id:
                if voix == k[0]:
                    id = k[1]
                    list_voix_accompagnement[j] = [voix, id]
                    break

        # list_voix_non_principale = app2.selected_options_2
        gen_tutti = app2.var_checkbox_gen_tutti.get()==1
    else:
        print("Voici les voix détectées:")
        for k,voix in enumerate(list_voices):
            print(f"[{k}] {voix}")
        indices = input("Indiquer le ou les indices de la ou les voix d'accompagnement (séparé par des virgules le cas échéant):\n").splir(',')
        list_voix_accompagnement = []
        for indice in indices:
            list_voix_accompagnement.append(list_voices[int(indice)])
        gen_tutti = input("WIP - Voulez-vous créer un fichier tutti ? [Y/n]") in ["Y","y",""]
    return list_voix_accompagnement, gen_tutti
