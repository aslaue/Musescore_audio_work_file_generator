def controler_arg_file_mscz():
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
    import sys
    # print(sys.argv)
    json_param_exists =False
    for k,i in enumerate(sys.argv[1:]):
        if i=="-p":
            json_file = sys.argv[k+1]
            json_file =True
            break
    if json_param_exists ==True:
        if json_file.endswith(".json") and os.path.isfile(json_file):
            # l'extension du fichier correspond, et le fichier existe
            return json_param_exists, json_file
    return False, ""

# controler_arg_fichier_json()

def CLI_get_mscz():
    input1 = input("Indiquer le chemin du fichier mscz:\n")
    if os.path.isfile(input1) and input1.endswith(".mscz"):
        input2 = input("indiquer l'éventuel fichier de paramètre json (laisser vide et pressez ENTER si vous n'en avez pas):\n")
        if os.path.isfile(input2):
            return input1, True, input2
        else:
            return input1, False, ""
    else:
        input("aucun fichier détecté, arrêt du programme, presser entre pour fermer la fenêtre")
        quit()

# CLI_get_mscz()

def extract_mscx(mscz_file):
    import os
    dir_mscz = os.path.dirname(mscz_file)
    dir_temp = dir_mscz + "/temp"
    if os.path.isdir(dir_temp):
        import shutil
        shutil.rmtree(dir_temp)
    os.mkdir(dir_temp)
    with zipfile.ZipFile(mscz_file,'r') as zf:
        zf.extractall(path=dir_temp)
    with open(dir_temp + "/" + os.path.basename(mscz_file).replace(".mscz",".mscx"), 'r') as mscx_file:
        content_mscx = mscx_file.readlines() # retourne une liste de str
    return content_mscx, dir_temp

def remove_nuances(content_mscx):
    mots_skip_intro = ['<Dynamic>','<Spanner type="HairPin">','<Fermata>']
    mots_skip_end = ['</Dynamic>','</Spanner>','</Fermata>']
    #<Dynamic> et </Dynamic> => nuance volume (f, mp ppp)
    #<Spanner type="HairPin"> et le prochain </Spanner> => crescendo, diminuendo, decrescendo
    #<Fermata> ... </Fermata> => pt d'orgue
    # les Rallentando, les Ritardando (lié au tempo, on garde => (<Spanner type="GradualTempoChange">)
    content_temp =[]
    for i in len(mots_skip_end):
        mot_intro = mots_skip_intro[i]
        mot_end = mots_skip_end[i]
        skipping = False
        for line in content_mscx:
            if skipping ==True:
                if mot_end in line:
                    skipping=False
                    continue
            elif skipping == False and mot_intro in line:
                skipping =True
                continue
            else: #skipping == False and mot_intro not in line
                content_temp.append(line)
        #une fois tout le document parcouru sous le regard d'un critère d'exclusion
        content_mscx = content_temp
        content_temp =[]
    return content_mscx
# content_mscx = remove_nuances(content_mscx) 



# list_voices_separated, content_mscx_separated = separate_voice(content_mscx)
def separate_voice(content_mscx):
    liste_voices_sous_voix_MS, liste_voices_accord, liste_voice_line = detect_voices(content_mscx) # [id, nb_voix]
    nb_voices_MS, nb_voices_accord = 0,0
    for i in liste_ss_voix_MS:
        nb_voices_MS+=i[1]
    for i in liste_ss_voix_accord:
        nb_voices_accord+=i[1]    
    print(f"il y a {nb_voices_MS} sous-voix détectées par MuseScore: \n{liste_voices_sous_voix_MS}\nIl y a {nb_ss_voix_accord} voix détectée avec les accords: \n{liste_voices_accord} \n")
    choice = input("indiquer 0 s'il n'y a rien à séparer, indiquer 1 si la détection de sous-voix par Musescore vous convient, indiquer 2 si la détection des voix avec les accords vous convient, [WIP indiquer 3 pour une combinaison des deux]")
    if choice =="1":
        content_mscx_separated = separate_voices_implemented_MS(content_mscx, liste_voice_line)
        list_voice_separated = liste_voices_sous_voix_MS
    if choice =="2":
        content_mscx_separated = separate_voices_accord(content_mscx, liste_voice_line, liste_voices_accord)
        list_voice_separated = liste_voices_accord
    return list_voice_separated, content_mscx_separated 


def detect_voices(content_mscx):
    liste_voice_line=[]
    for k,line in enumerate(content_mscx):
        if '<Staff id="' in line:
            id = line.split('<Staff id="')[0]
            liste_voice_line.append([id, k])
    liste_ss_voix_MS = []
    liste_ss_voix_accord = []
    for k in range(len(liste_voice_line)):
        if k<len(liste_voice_line):
            ligne_fin = liste_voice_line[k+1][1]
        else:
            ligne_fin = len(content_mscx)
        ligne_debut = liste_voice_line[k][1]
        in_measure = False
        in_chord = False
        nb_ss_voix_MS = 0
        nb_ss_voix_accord = 0
        for line in content[ligne_debut:ligne_fin]:
            # sous-voix MS
            if "<Measure>" in line:
                count_MS=0
                in_measure=True
            elif in_measure==True:
                if "<voice>" in line:
                    count_MS+=1
                elif "</Measure>" in line:
                    in_measure=False
                    nb_ss_voix_MS = max(count_MS,nb_ss_voix_MS)
            # sous-voix accord
            if "<Chord>" in line:
                count_accord=0
                in_chord=True
            elif in_chord==True:
                if "<Note>" in line:
                    count_accord+=1
                elif "</Chord>" in line:
                    in_chord = False
                    nb_ss_voix_accord = max(count_accord, nb_ss_voix_accord)
        liste_ss_voix_MS.append([liste_voices_sous_voix_MS[k][0], nb_ss_voix_MS])
        liste_ss_voix_accord.append([liste_voices_accord[k][0], nb_ss_voix_accord])
    return liste_ss_voix_MS, liste_ss_voix_accord, liste_voice_line


def separate_content_accord(content_mscx, liste_voice_line, liste_voices_accord): #liste_voices_accord = [id, nb_ss_voix_accord]
    content_mscx_separated = []
    id_staff = 0
    for k in range(len(liste_voice_line)):
        id = liste_voices_accord[k][0]
        nb_ss_voix_accord = liste_voices_accord[k][1]
        if k<len(liste_voice_line):
            ligne_fin = liste_voice_line[k+1][1]
        else:
            ligne_fin = len(content_mscx)
        ligne_debut = liste_voice_line[k][1]
        
        if liste_voices_accord[1][k]==1:
            temp = content_mscx[ligne_debut].split('"')
            content_mscx[ligne_debut] = temp[0] + f'"{id_staff}"' +temp[2] #        '<Staff id="...">'
            id_staff+=1
            continue
            #il n'y a rien à séparer => rien à modifier
        
        content1 = []
        content2 = []
        only_second_voice=False
        in_note = False
        temp_content = []
        for k in range(ligne_debut,ligne_fin):
            ####### il faut ne pas créer une var temporaire tant que in_note==True, puis une fois </Note,>, on regarde si la prochaine ligne est "<Note>" si non => c1 et c2 append var_temp, si oui seul c1 append var_temp et seul c2 append le prochain <Note> 
            line = content_mscx[k]
            #Si la ligne est hors du tag <Note>, c1 et c2 copient (cas 3)
            #Si on est dans un tag <Note>, et qu'il n'y a qu'une seule note, c1 et c2 copient (cas 1), alors que s'il y a plus d'une note, c1 copie la première note et c2 la 2è (cas 2).
            #pour cela, dès qu'on entre dans un tag <Note>, on enregistre les lignes dans une variable temporaire.
            #si au moment de </Note>, il n'y a pas d'autre tag <Note> qui suit => c1 et c2 copient le contenu de la variable temporaire (cas 1)
            #sinon, à la fin du premier tag <Note>, c1 enregistre le contenu de var temp (cas 2.1), et le 2è tag est uniquement enregistré par c2 (cas 2.2)
            if "<Note>" not in line and in_note ==False: #  cas 3
                content1.append(line)
                content2.append(line)
            elif "<Note>" in line:
                temp_content.append(line)
                in_note = True
            elif "</Note>" in line:
                in_note = False
                temp_content.append(line)
                if only_second_voice == True: # cas 2.2
                    for i in temp_content:
                        content2.append(i)
                    temp_content =[]
                elif "<Note>" in content_mscx[k+1]: # cas 2.1 s'il y a un autre tag <Note> à la ligne suivante
                    for i in temp_content:
                        content1.append(i)
                    temp_content=[]
                    only_second_voice=True
                else: # cas 1
                    for i in temp_content:
                        content1.append(i)
                        content2.append(i)
                    temp_content=[]
            elif in_note == True:
                temp_content.append(line)
            if "</Chord>" in line:
                only_second_voice=False
        # Attention, content1 reprend la ss-voix 2 et inversemment.
        # on ajuste la valeur ID dans la partie partition
        temp = content2[0].split('"')
        content2[0] = temp[0] + f'"{id_staff}"' +temp[2] #        '<Staff id="...">'
        id_staff+=1
        temp = content1[0].split('"')
        content1[0] = temp[0] + f'"{id_staff}"' +temp[2] #        '<Staff id="...">'
        id_staff+=1
        
        liste_voices_accord, content1 = change_id(content1, id, liste_voices_accord) #increase le id de "<Staff id=""> de la ss-voix et des voix suivantes dans la partie partition
        content_mscx_separated.append(content2,content1)
    content_mscx = change_head(content_mscx, liste_voices_accord) ## qu'est ce que ça fait déjà ? ça ajoute une voix dans les définitions ? avant la partie partition
    content_mscx_separated =  combine_head(content_mscx, content_mscx_separated)
    return content_mscx_separated

def change_head(content_mscx, liste_voices_accord): #liste_voices_accord = [id, nb_ss_voix_accord]
    # dupliquer la définition lorsque division ss-voix
    for i in range(len(liste_voices_accord)):
        if liste_voices_accord[i][1] >1:
            id = liste_voices_accord[i][0]
            in_loop = False
            variable_temp = []
            line_beginning = 0
            trackname_already_passed = False
            #changer la définition de la ss-voix 1 et dupliquer pour la ss-voix 2 puis adapter
            for k,line in enumerate(content_mscx):
                if f'<Part id="{id}">' in line:
                    line_beginning = k
                    in_loop = True
                    variable_temp.append(line)
                    # copier le contenu dans une variable  
                if in_loop==True:
                    if "<trackName>" in line and trackname_already_passed ==False: # change line = <trackName>Soprano</trackName> into <trackName>Soprano 2</trackName>
                        split_line = line.split("</trackName>")
                        line = split_line[0] + " 2"+ split_line[1]
                        content_mscx[k] = line
                        line = line.replace("2","1")
                        trackname_already_passed =True
                    elif "<longName>" in line: # <longName>Soprano</longName>
                        split_line = line.split("</longName>")
                        line = split_line[0] + " 2"+ split_line[1]
                        content_mscx[k] = line
                        line = line.replace("2","1")
                    elif "<shortName>" in line: # <shortName>S.</shortName>
                        split_line = line.split("</shortName>")
                        line = split_line[0] + " 2"+ split_line[1]
                        content_mscx[k] = line
                        line = line.replace("2","1")
                        
                    variable_temp.append(line)
                    if "</Part>" in line:
                        break
            content_mscx = [content_mscx[:line_beginning-1], variable_temp, content_mscx[line_beginning:]]
    increment = 0
    for k,line in enumerate(content_mscx):
        if '<Staff id="1">' in line: # début partie partition
            break
        if '<Part id="' in line:
            id = int(line.split('<Part id="')[1].split('"')[0])
            content_mscx[k] = line.replace(str(id),str(id+1))
            content_mscx[k+1] = content_mscx[k+1].replace(str(id),str(id+1))
            increment+=1 
    # incrémente les id
    return content_mscx

# content_mscx_separated =  combine_head(content_mscx, content_mscx_separated)
def combine_head(content_mscx, content_mscx_separated):
    for k, line in enumerate(content_mscx):
        if '<Staff id="1">' in line: # début partie partition
            break
    return [content_mscx[:k-1], content_mscx_separated]
