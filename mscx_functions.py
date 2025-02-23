from copy import deepcopy
import sys, os, zipfile, json, shutil

def remove_nuances(content_mscx):
    """
    It removes the unwanted content (volume nuances, Fermata (point d'orgue)) of the mscx file. It copies line per line content_mscx but skips sections
    Arguments:
        content_mscx: list(string)     #raw content of the extracted mscz file
    Returns:
        content_mscx: list(string)     # filtred mscx content
    """
    mots_skip_intro = ['<Dynamic>','<Spanner type="HairPin">','<Fermata>']
    mots_skip_end = ['</Dynamic>','</Spanner>','</Fermata>']
    #<Dynamic> et </Dynamic> => nuance volume (f, mp ppp)
    #<Spanner type="HairPin"> et le prochain </Spanner> => crescendo, diminuendo, decrescendo
    #<Fermata> ... </Fermata> => pt d'orgue
    # les Rallentando, les Ritardando (lié au tempo, on garde => (<Spanner type="GradualTempoChange">)
    content_temp =[]
    for i in range(len(mots_skip_end)):
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

def separate_voice(content_mscx):
    """
    A bit of informations: there is two ways to write subvoices in Musescore (Soprane 1 and Soprane 2, for example):
    - with the chord (technically, it is on the same voice, but it sounds 2 sound. It's a quick way, sounds and displays all right, but it has to be precessed to separate the sub-voices for the work files. Also, it only works if the 2 sub-voices have the same rythm)
    - use of the regular sub-voice (ctrl + alt + 1 or 2, but takes more time)
    One of the goal of the program is to isolate each subvoices and raise its volume to generate its audio
    Here, the code detects the number of subvoices for each voices with the 2 ways (function detect_voices()).
    Then it lauches the separation of the mscx file
    Arguments:
        content_mscx: list(string)              # content of the mscx file, without the volume nuances
    Returns:
        list_voice_separated                    # list of the detected subvoices according to the method
        content_mscx_separated: list(string)    # content ready to be exported, with each sub-voices accounted as one independant voice and without volume nuances
    """

    # First, we detect the frontiers between the mscx file's head, body_def and body_notes
    line_body_def = 0
    for k, line in enumerate(content_mscx):
        if "</Order>" in line:
            line_body_def = k+1
        elif '<Part id="' in line and line_body_def==0: # il arrive que le tag <Order> ne soit pas utilisé => on prend la ligne de la première occurence du tag <Part>
            line_body_def = k
        elif "</Part>" in line:
            line_body_notes = k+1
        elif "</Score>" in line:
            line_end_score = k

    liste_voices_sous_voix_MS, liste_voices_accord, liste_voice_line = detect_voices(content_mscx[line_body_notes:]) # [id, nb_voix]
    # Chaque liste_voices est une list composée de [id, nb_ss_voix]
    liste_voices_final=[] # de type nom, id old, id_
    content_body_def, liste_name_id, correspondance_id_initial_incremente = separate_body_def_accord(content_mscx[line_body_def:line_body_notes], liste_voices_sous_voix_MS, liste_voices_accord)

    liste_measure_to_change_by_staff_according_to_sous_voix = separate_body_notes_sous_voix(content_mscx[line_body_notes:], liste_voices_sous_voix_MS)
    content_mscx_body_notes = separate_body_notes_accord(content_mscx[line_body_notes:], correspondance_id_initial_incremente,liste_measure_to_change_by_staff_according_to_sous_voix)

    content_mscx_separated = content_mscx[:line_body_def] + content_body_def + content_mscx_body_notes + content_mscx[line_end_score:]
    
    return liste_name_id, content_mscx_separated 

def detect_voices(content_mscx):
    """
    Called by separate_voice()
    it detects the number of subvoices in each voices, with each method, it puts it into a matrix, and indicates the line number of the beggining of each voices.
    Arguments:
        content_mscx: list(string) # ...
    Returns:
        liste_ss_voix_MS: list(id voix, nb sous-voix)           # list of the voices and number of subvoices in it 
        liste_ss_voix_accord: list(id voix, nb sous-voix)       # list of the voices and number of subvoices in it
        liste_voice_line: list(id voix, num_line voix)         # list of the line number in the mscx file of the beggining of the voice 
    """
    liste_voice_line=[]
    for k,line in enumerate(content_mscx):
        if '<Staff id="' in line:
            id = line.split('<Staff id="')[1][0]
            liste_voice_line.append([id, k])
    liste_ss_voix_MS = []
    liste_ss_voix_accord = []
    for k in range(len(liste_voice_line)):
        if k<len(liste_voice_line)-1:
            ligne_fin = liste_voice_line[k+1][1]-1
        else:
            ligne_fin = len(content_mscx)
        ligne_debut = liste_voice_line[k][1]
        in_measure = False
        in_chord = False
        nb_ss_voix_MS = 0
        nb_ss_voix_accord = 0
        for line in content_mscx[ligne_debut:ligne_fin]:
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
        liste_ss_voix_MS.append([liste_voice_line[k][0], nb_ss_voix_MS])
        liste_ss_voix_accord.append([liste_voice_line[k][0], nb_ss_voix_accord])
    return liste_ss_voix_MS, liste_ss_voix_accord, liste_voice_line

def separate_body_notes_sous_voix(content_mscx, liste_voices: list): # théoriquement ok
    """
    In order to combine the notes from the accord and sous-voix methods in the separate_body_notes_accord() function, we must obtain the measure number and content where the sous-voix need to be separated 
    
    idée grossière:
    # 1) Pour chaque <Staff> original avec besoin_separation==True appelé i:
        # a) pour chaque <Measure>, on identifie le nombre de <voice>
            # Si 1, on ne fait rien (continue)
            # Si 2, on enregistre dans var_temp_1 le premier contenu de la balise <voice>, dans var_temp_2, on reprend le contenu de var_temp_1 en modifiant le contenu de <Chord> par le <Chord> compris dans le 2è <voice> (nécessaire reprendre à partir du var_temp_1 car si première mesure => peut manquer infos)
            # on append ensuite à liste(i) [num_mesure, var_temp_1, var_temp_2]
            # si >2, à voir plus tard
    # 2) on renvoie [id_initial(i), liste(i)]

    Arguments:
        content_mscx: list(string)              # content of the mscx file (only the last part of the file with the notes), without the volume nuances
    Returns:
        liste_measure_to_change_by_staff_according_to_sous_voix: list(int, list)     # a list with 1 entry per staff that requires separation. the list in the list contain the measure number and content that must be separated in regard to the sous-voix method
    """
    liste_measure_to_change_by_staff = []
    for i in liste_voices:
        if i[1]==1: # s'il n'y a qu'une sous-voix dans la voix => pas besoin de séparer => on passe au suivant
            continue
        else:
            liste_measure_to_change = []
            in_staff=False
            id_initial = i[0]
            num_mesure=0
            count_chord=0
            for num_line,line in enumerate(content_mscx):
                if f'<Staff id="{id_initial}">' in line:
                    in_staff=True
                elif in_staff==True:
                    if "</Staff>" in line:
                        liste_measure_to_change_by_staff.append([id_initial, liste_measure_to_change])
                        # print("--------------------------")
                        break
                    elif "<Measure>" in line:
                        count_voice=0
                        ligne_mesure=num_line
                        num_mesure+=1
                    elif "<Chord>" in line and count_chord==0:  # utile ici pour déterminer le moment où il faut les déterminer la partie commune des 2 sous-voix (au delà de cette ligne, la sous-voix 1 et 2 diffèrent)
                        count_chord+=1
                        ligne_chord_1_voice_1=num_line
                    elif "<voice>" in line:
                        count_voice+=1
                        if count_voice==2:
                            ligne_voice_2=num_line
                    elif "</Measure>" in line:
                        if count_voice==2:
                            ss_voix_1 = content_mscx[ligne_mesure:ligne_voice_2] + [line]
                            if num_mesure==1: # Il faut faire la distinction car sinon, manque balise ouvrante Measure et Voice aux mesures >1
                                ss_voix_2 = content_mscx[ligne_mesure:ligne_chord_1_voice_1] + content_mscx[ligne_voice_2+1:num_line+1]
                                # print(ss_voix_2)
                            else:
                                # print("bonjour")
                                ss_voix_2 = content_mscx[ligne_mesure:ligne_chord_1_voice_1] + [content_mscx[ligne_mesure]] + content_mscx[ligne_voice_2:num_line+1]
                                # print("")
                            # for line_ss_voix in ss_voix_2:
                            #     print(line_ss_voix)
                            # print("\n")
                            liste_measure_to_change.append([num_mesure, ss_voix_1, ss_voix_2])
            if len(liste_measure_to_change)>0: # devrait être tout le temps le cas
                liste_measure_to_change_by_staff.append([id_initial, liste_measure_to_change])
    
    return liste_measure_to_change_by_staff

def separate_body_def_accord(content_mscx, liste_voices_sous_voix_MS, liste_voices_accord): # normalement ok, à voir si retourne correspondance_id_initial_incremente = [id initial, name_initial, [ids], [names]]
    """
    Description à faire

    # 1) faire une liste [trackName, id] 🗸
    # 2) définir la liste de voix en combinant liste_voices_sous_voix_MS et liste_voices_accord 🗸
    # 3) à chaque <Part id= >, mettre à jour la valeur id
    # 4) Pour chaque <Part id= > qui doit être séparé, 
        # a) dupliquer, màj le id+=1, ajouter "2" au <trackName>
        # b) sur l'original, ajouter "1" au  <trackName>
    # 5) Renvoyer le contenu body_def et la liste [trackName, id_initial]
    """
    liste_name_id = []
    for line in content_mscx:
        if "<Part id=" in line:
            id = line.split('<Part id="')[-1].split('">')[0]
        if line.find("      <trackName>")==0:
            name = line.split('<trackName>')[-1].split("</trackName>")[0]
            liste_name_id.append([name, id])

    liste_id_toseparate =[]
    for i in liste_voices_accord:
        id_accord = i[0]
        nb_voix_accord = i[1]
        for j in liste_voices_sous_voix_MS:
            if id_accord==j[0]:
                nb_voix_ss_voix = j[1]
        nb_voix = max(nb_voix_accord, nb_voix_ss_voix)
        to_separate= nb_voix >=2
        liste_id_toseparate.append([id_accord, to_separate, nb_voix])
    
    # liste [name, id_initial, id_incrementé]
    correspondance_id_initial_incremente =[]
    total_voix = 0
    liste=[]
    for i in liste_id_toseparate:
        temp=[]
        nb_voix = i[2]
        id_initial = i[0]
        temp_id = []
        temp_name = []
        for k in liste_name_id:
            if k[1]==id_initial:
                name_initial = k[0]
                break
        for j in range(1,nb_voix+1):
            if nb_voix == 1:
                name_temp = name_initial
            else:
                name_temp = f"{name_initial} {str(j)}"
            total_voix += 1
            liste.append([name_temp, id_initial, total_voix])
            temp_id.append(total_voix)
            temp_name.append(name_temp)
        correspondance_id_initial_incremente.append([id_initial, name_initial, temp_id, temp_name])

    content_body_def=[]
    for k,line in enumerate(content_mscx):
        if "<Part id=" in line:
            num_line_part = k
            id_initial = line.split('<Part id="')[-1].split('">')[0]
        elif "<Staff id=" in line:
            num_line_staff = k
        elif line.find("      <trackName>")==0: # permet de s'assurer de ne prendre que la ligne avec la bonne indentation
            num_line_name = k
        elif "</Part>" in line:
            num_line_end = k+1
            for i in correspondance_id_initial_incremente:
                if i[0]==id_initial:
                    for j in range(len(i[2])):
                        content_body_def.append(content_mscx[num_line_part].replace(f'id="{id_initial}"', f'id="{i[2][j]}"' ))
                        content_body_def.append(content_mscx[num_line_staff].replace(f'id="{id_initial}"', f'id="{i[2][j]}"' ))
                        content_body_def += content_mscx[num_line_staff+1:num_line_name]
                        content_body_def.append(content_mscx[num_line_name].replace(i[1], i[3][j]))
                        # print(content_mscx[num_line_name].replace(i[1], i[3][j]))
                        # content_body_def +=content_mscx[num_line_name+1:num_line_end]
                        content_body_def +=content_mscx[num_line_name+1:num_line_end]
    
    return content_body_def, liste_name_id, correspondance_id_initial_incremente # autre chose ???

def separate_body_notes_accord(content_mscx_body_notes, correspondance_id_initial_incremente, liste_measure_to_change_by_staff_according_to_sous_voix): #liste_voices_accord = [id, nb_ss_voix_accord]
    """
    info function:

    Arguments:
        
    Returns:
        new_content_mscx_body_notes: list(str)
    # notes pour moi
        # à amener comme variable: 
            # - liste des mesures avec modifs par sous-voix, le contenu de ces sous-voix
            # - liste des Staff à dédoubler

        # 1) faire une liste [nom_voix, id_initiale, id_incrementee] 🗸
        # 2) Pour chaque <Staff> original, mettre à jour l'id selon id_incrémentée 🗸
        # 3) Pour chacun des <Staff> qui doivent être séparés:
            # a) Pour chaque <Chord> de chaque <Measure>, on identifie le nombre de <Note>
                # Si 1, on check si dans le contenu de separate_body_notes_sousvoix, à cette <Measure>, il y a une séparation faite au niveau de la sous-voix
                    # I) Si oui, on va copier les deux différentes <Notes> et les placer dans les 2 différentes var temp 1 et 2 (cas 1.I)
                    # II) Si non, on copie tel quel le <Chord> dans la var temp 1 et 2 (cas 1.II)
                        # (Il y a un parti pris que si il y a un accord + une sous-voix, alors pouet et tant pis pour la séparation méthode accord)
                # Si 2, on copie la première <Note> du <Chord> dans la var temp 2 et la 2è <Note> dans la var temp 1 (Dans l'ordre du ficher texte, la première note est la plus grave et donc va dans la sous-voix n°2) (cas 2)
                # {futur release} Si >2, dans un premier temps, copier dans variable temp 1, et il y aura des notes superposées. Plus tard, configurer pour créer une 3è voix => doit compter le nb de voix, compliqué.
            # b) on remplace le contenu du <Staff> par var temp 1, et on crée un 2è <Staff> avec un id+1, et on ajoute le contenu de var temp 2
        # 4) renvoyer le contenu body_notes

        # from separate_body_notes_sous_voix()
        # liste_measure_to_change_by_staff = list([id_initial, list([num_mesure, ss_voix_1, ss_voix_2])])
        # ss_voix_{i} ont tout le contenu entre <Measure> et </Measure> (n'ont peut-être pas la bonne indentation, par contre)
        # Problème: dans le script ci-dessous, on fait le contrôle de séparation accord par accord. Dans le cas 1.I, c'est indiqué qu'on copie les <Notes> dans les différentes var_temp. Or, ss_voix_[i], contient la mesure entière
        # => dans le code ci-dessous, il faut faire une exception si cas 1.I, on n'analyse pas la fin de la mesure et on passe jusqu'aux instruction de if "</Measure>" in line

        # from separate_body_def_accord()
        # correspondance_id_initial_incremente = list([id_initial, name, list(name_new), list(id_new)])
    """
    str_beggining_measure   = "      <Measure>\n        <voice>\n"
    str_end_measure         = "          </voice>\n        </Measure>\n"
    new_content_mscx_body_notes = []
    for item in correspondance_id_initial_incremente:
        id_initial = item[0]
        id_new = item[2] # = list(item[2]) ou # .append(item[2]) ou # = [item[2]] ?? doit être appelable avec id_new[0]
        in_staff=False
        measure_to_change = []

        for i in liste_measure_to_change_by_staff_according_to_sous_voix: # from separate_body_notes_sous_voix()
            if i[0] == id_initial:
                measure_to_change = i[1] # = list(id[1]) ou # .append(i[1]) ou # = [i[1]] ??
                break

        if len(measure_to_change)==0: # si la liste de mesure à changer selon la méthode separate_body_notes_sous_voix() est vide
            if len(id_new)==1: # si la liste de mesure à changer selon la méthode separate_body_notes_sous_voix() est vide
                # remplacer le id_initial par id_new, pas besoin de changer le name, garder le même contenu
                for num_line,line in enumerate(content_mscx_body_notes):
                    if f'<Staff id="{id_initial}">' in line:
                        num_line_staff = num_line
                        staff_line = line.replace(f'<Staff id="{id_initial}">', f'<Staff id="{id_new[0]}">')
                        in_staff=True
                    elif in_staff == True:
                        if "</Staff>" in line:
                            new_content_mscx_body_notes += [staff_line] + content_mscx_body_notes[num_line_staff+1:num_line+1]
                            break
                continue # continue la boucle for item in correspondance
        
        for num_line,line in enumerate(content_mscx_body_notes):
            if f'<Staff id="{id_initial}">' in line:
                in_staff=True
                num_mesure = 0
                staff_line_1 = line.replace(f'<Staff id="{id_initial}">', f'<Staff id="{id_new[0]}">')
                staff_line_2 = line.replace(f'<Staff id="{id_initial}">', f'<Staff id="{id_new[1]}">')
                temp_1 = []
                temp_1.append(staff_line_1)
                temp_2 = []
                temp_2.append(staff_line_2)
                line_staff = num_line
            elif in_staff==True:
                if "</Staff>" in line:
                    new_content_mscx_body_notes += temp_1 + [line]
                    new_content_mscx_body_notes += temp_2 + [line]
                    break
                elif "<Measure>" in line:
                    ligne_mesure=num_line
                    num_mesure += 1
                    if num_mesure==1 and num_line-line_staff >1:
                        # S'il y a qch entre le staff et la première measure (généralement au staff n°1)
                        temp_1 += content_mscx_body_notes[line_staff+1:num_line] # seulement pour la sous-voix 1
                    cas = ""
                    temp_content_chord_voix_1 = []
                    temp_content_chord_voix_2 = []
                    ligne_mesure_str = line
                    ligne_voice_str = content_mscx_body_notes[num_line+1]
                
                # elif "<KeySig>" in line:
                #     line_keysig = num_line
                # elif "</TimeSig>" in line:
                #     temp_content_chord_voix_1 += content_mscx_body_notes[line_keysig:num_line+1]
                #     temp_content_chord_voix_2 += content_mscx_body_notes[line_keysig:num_line+1]
                elif "<KeySig>" in line:
                    line_keysig = num_line
                elif "</KeySig>" in line:
                    temp_content_chord_voix_1 += content_mscx_body_notes[line_keysig:num_line+1]
                    temp_content_chord_voix_2 += content_mscx_body_notes[line_keysig:num_line+1]
                elif "<TimeSig>" in line:
                    line_timesig = num_line
                elif "</TimeSig>" in line:
                    temp_content_chord_voix_1 += content_mscx_body_notes[line_timesig:num_line+1]
                    temp_content_chord_voix_2 += content_mscx_body_notes[line_timesig:num_line+1]                    
                    # print("")
                elif "<Chord>" in line:
                    nb_notes_in_accord = 0
                    max_nb_notes_in_accord_in_measure = 0
                    ligne_chord=num_line
                    list_ligne_note =[]
                    list_ligne_fin_note =[]
                elif "<Note>" in line:
                    nb_notes_in_accord += 1
                    list_ligne_note.append(num_line)
                elif "</Note>" in line:
                    list_ligne_fin_note.append(num_line)
                elif "</Chord>" in line:
                    # temp_content_chord_voix_1 = []
                    # temp_content_chord_voix_2 = [] # Ce n'est pas adapté de faire le reset à cet emplacement
                    list_ligne_fin_chord = num_line
                    max_nb_notes_in_accord_in_measure = max(max_nb_notes_in_accord_in_measure, nb_notes_in_accord)
                    if nb_notes_in_accord == 1:
                        # #cas 1) => on check si dans le contenu de separate_body_notes_sousvoix, à cette <Measure>, il y a une séparation faite au niveau de la sous-voix
                        # loop_break =False
                        # for i in measure_to_change:
                        #     if num_mesure == i[0]:
                        #         # cas 1.I) => on va copier l'entièreté de la mesure
                        #         loop_break = True
                        #         contenu_mesure_ss_voix_1 = i[1]
                        #         contenu_mesure_ss_voix_2 = i[2]
                        #         cas = "1.I"
                        #         # tout ce qu'il y aura entre cette ligne et la ligne "</Measure>" ne sera pas pris en considération
                        #         break
                        # if loop_break == False:
                            # cas 1.II) => Il n'y a pas besoin de séparation ni par la méthode accord ni par sous-voix, => on copie tel quel le <Chord> dans la var temp 1 et 2
                        temp_content_chord_voix_1 +=content_mscx_body_notes[ligne_chord:num_line+1]
                        temp_content_chord_voix_2 += content_mscx_body_notes[ligne_chord:num_line+1]
                    elif nb_notes_in_accord == 2:
                        # cas 2) => on copie la première <Note> du <Chord> dans la var temp 2 et la 2è <Note> dans la var temp 1 (Dans l'ordre du ficher texte, la première note est la plus grave et donc va dans la sous-voix n°2)
                        temp_content_chord_voix_2 += content_mscx_body_notes[ligne_chord:list_ligne_fin_note[0]] + content_mscx_body_notes[list_ligne_fin_note[1]:num_line+1]
                        temp_content_chord_voix_1 += content_mscx_body_notes[ligne_chord:list_ligne_note[0]] + content_mscx_body_notes[list_ligne_note[1]:num_line+1]
                        # les variables temp_content_chord_voix_{i} contiennent ce qui se trouve entre <Chord> et </Chord>
                elif "</Measure>" in line:
                    for i in measure_to_change: # est-ce que la mesure a >1 sous-voix ?
                        if num_mesure == i[0]:
                            # cas 1.I) => on va copier l'entièreté de la mesure
                            contenu_mesure_ss_voix_1 = i[1]
                            contenu_mesure_ss_voix_2 = i[2]
                            cas = "1.I"
                            break
                    if cas == "1.I":
                        # on va copier l'entièreté de la mesure dans les variables 
                        temp_1 += contenu_mesure_ss_voix_1
                        temp_2 += contenu_mesure_ss_voix_2
                        contenu_mesure_ss_voix_1 = []
                        contenu_mesure_ss_voix_2 = []
                        # print("")
                    else:
                        temp_1.append(str_beggining_measure)
                        temp_1 += temp_content_chord_voix_1
                        temp_1.append(str_end_measure)
                        temp_2.append(str_beggining_measure)
                        temp_2 += temp_content_chord_voix_2
                        temp_2.append(str_end_measure)
    return new_content_mscx_body_notes