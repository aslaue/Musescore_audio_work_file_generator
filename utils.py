from copy import deepcopy
import sys, os, zipfile, json, shutil
# from main import GUI

def controle_version_partition(content_mscx):
    """
    Cette fonction contrôle que la partition a bien été enregistrée par une version de MuseScore ≥ 4.0, sinon, elle arrête le programme.
    Elle rend attentif aux problèmes qui peuvent advenir si la version de la partition est supérieure à celle pour laquelle le script a été testé.
    Arguments:
        content_mscx: list(str) # contenu du fichier mscx (on n'a besoin que de la ligne 2 en vrai)
    Returns:
        version_fichier: str    # indique la version de MuseScore avec laquelle a été enregistrée la partition
    """
    version_acceptee_min = 4
    version_acceptee_max = 4.5 # version au 18.04.2025, à mettre à jour

    for line in content_mscx:
        if "<museScore version=\"" in line: # normalement en ligne 2
            version_fichier = line.split('"')[1]
            break
    print("version de la partition: ",version_fichier)
    if float(version_fichier) < version_acceptee_min:
        string_to_display = "Attention, la partition que vous souhaitez traiter a été enregistrer sur une version ancienne de MuseScore (version {}) qui ne fonctionne pas avec ce script. Veuillez ouvrir et enregistrer votre partition dans une version supérieure ou égale à la 4.0, et utiliser ce fichier pour être traité par le script".format(version_fichier)
        from tkinter import messagebox
        messagebox.showerror(title = "Erreur fatale", message = string_to_display)
        sys.exit() # arrêt du programme
    elif float(version_fichier) > version_acceptee_max:
        string_to_display = "La version dans laquelle a été enregistrée le fichier de partition MuseScore à traiter est plus récente que celle sur lequel le présent script a été testé. Il se peut que le script ne fonctionne pas correctement.\n"+\
        "Si cela devait arriver, deux solutions s'offrent à vous:\n"+\
        " - Télécharger une version mise à jour du script au lien suivant: ...\n"+\
        "Pour plus d'information sur comment rétrograder: ...."
        messagebox.showwarning(message = string_to_display)
    return version_fichier

def controle_version_musescore(version_fichier, commande_version, commande_generation_mp3):
    """
    Cette fonction va regarder que la version de Musescore installée soit supérieure ou égale à la version avec laquelle a été enregistrée la partition, et dans le cas contraire, va afficher un message d'erreur invitant à mettre à jour, puis à exécuter la commande de génération des fichier audio. Après cela, la fonction arrête le programme.
    Utile dans la situation assez improbable où une partition qui n'a pas été ouverte sur le logiciel MuseScore en local est traitée par le script, et que la version de la partition est supérieure au logiciel
    Lorsque la fonction main est lancée depuis VS Codium (et j'imagine VS Code aussi), le fichier Appimage ne peut pas être exécuté pour obtenir la version du logiciel. Dans ce cas, le programme affiche un message d'erreur invitant à lancer le main avec python, indique la commande à exécuter dans un terminal puis ferme le programme.

    Arguments:
        version_fichier: str            # indique la version de MuseScore avec laquelle a été enregistrée la partition
        commande_version: str           # contient la commande à exécuter pour afficher la version du logiciel (contient les subtilités liée à l'OS et l'emplacement de l'exécutable)
        commande_generation_mp3: str    # contient la commande à exécuter pour générer les fichiers mp3 à partir du fichier JSON (à afficher dans le cas d'une erreur critique)
    """
    import subprocess

    # Exécution de la commande
    resultat = subprocess.run(commande_version, shell=True, capture_output=True, text=True)

    if "required file not found" in resultat.stderr:
        str_to_display = "VS Code (ou le logiciel que vous avez utilisé pour exécuter le script) ne permet pas d'utiliser le logiciel MuseScore par le biais des lignes de commandes et la génération des fichiers mp3 ne peut se faire automatiquement.\n"+\
        "Veuillez exécuter cette ligne de commande dans votre terminal:\n"+\
        commande_generation_mp3 +\
        "\nCependant, il n'est pas possible de contrôler que la version de la partition (version {}) soit bien inférieure ou égale à la version de MuseScore. Veuillez vous assurer de cela manuellement, et mettre à jour votre logiciel de MuseScore si nécessaire\n".format(version_fichier)+\
        "De plus, la suppression des fichiers temporaires devra se faire manuellement.\nPour éviter ces désagrément dans le futur, veuillez exécutez ce script directement avec python, sans passer par VS Code."
        from tkinter import messagebox
        messagebox.showwarning(message = string_to_display)
        import sys
        sys.exit()
    if "MuseScore" in resultat.stdout:
        version_musescore = resultat.stdout.split(" ")[-1]
        # print(version_musescore)
    else:
        for i in resultat.stderr.split("\n"):
            if "MuseScore" in i:
                version_musescore = i.split(" ")[-1]
                # print(version_musescore)
                break
    version_split = version_musescore.split(".")
    version_musescore = float(f"{version_split[0]}.{version_split[1]}")
    # version_fichier = "4.6"

    if float(version_fichier) > version_musescore:
        str_to_display = f"La version de MuseScore installée (version {version_musescore}) est inférieure à la version de la partition (version {version_fichier}). Il n'est pas possibe de procéder à la génération des fichiers de travail sans une mise à jour du programme.\n" + \
        "Après avoir mis à jour le programme, vous pourrez simplement exécuter la commande suivante:\n" + \
        commande_generation_mp3 + \
        "\nAprès la génération des fichiers de travail, il faudra également supprimer manuellement les fichiers temporaires"
        from tkinter import messagebox
        messagebox.showerror(message = str_to_display)
        import sys
        sys.exit()

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

def generate_volume_matrix(volume_voix_acc, volume_voix_sec, correspondance_id_initial_incremente, list_voix_accompagnement, gen_tutti):
    """
    Cette fonction génère une matrice des volumes. chaque ligne i de la matrice correspond à un fichier de travail, et chaque colonne j correspond au volume de l'instrument qui doit être joué. Ainsi une valeur (i,j) de 60, indique que le volume de l'instrument j sera de 60% dans le fichier de travail i.
    L'élément j,j (volume de la voix principale) sera de 100%, par défaut, les voix secondaires et les voix d'accompagnement (éléments i,j ∀i!=j) sont déterminées par volume_voix_sec et volume_voix_acc. Il est possible d'affiner ces paramètres dans la fenêtre GUI 4

    Arguments:
        volume_voix_acc: str        # 0-100%, défini dans la fenêtre GUI 3
        volume_voix_sec: str        # 0-100%, défini dans la fenêtre GUI 3
        correspondance_id_initial_incremente: list([str, str, list(str), list(str)])        # one set per initial_id. For each set, the list contains the new_id and the new_name ~ [id_initial, name_initial, list(id_new), list(name_new]]  
        list_voix_accompagnement: list[str, int]    # liste les noms des voix et les ID des voix d'accompagnement (qui n'auront pas de fichier de travail attribué)
        gen_tutti

    Return
        matrix
        intitule_lignes_matrix: list(str)   # correspond à la liste de noms complets des voix qui auront un fichier de travail + tutti
        intitule_colonne_matrix: list(str)  # correspond à la liste de noms complets des voix sans distinction
        liste_voix_id_nom_new: list([str, str]) #list([id_new, name_new)]] 
    """
    # correspondance_id_initial_incremente prend en compte la méthode des accord, mais prend-elle en compte la méthode MS ? à vérifier
    liste_voix_principales = []
    liste_voix_id_name_new = []
    for j in correspondance_id_initial_incremente:
        # partie génération liste_voix_id_nom
        for k in range(len(j[2])):
            liste_voix_id_name_new.append([j[2][k],j[3][k]])
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

    return matrix, intitule_lignes_matrix, intitule_colonne_matrix, liste_voix_id_name_new

def get_voix_accompagnement(liste_name_id, Fenetre_2, GUI_parameters, GUI):
    """
    Appelle la fenêtre GUI 2 pour déterminer les voix d'accompagnement (qui n'auront pas de fichier de travail attribué). 

    Returns:
        list_voix_accompagnement: list[str, int]    # liste les noms des voix et les ID des voix d'accompagnement (qui n'auront pas de fichier de travail attribué)
        gen_tutti: bool                             # UI, détermine si le fichier de travail tutti sera généré
    """
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
