# instruction pour hekp: tu peux lancer python main.py -f file.mscz -p param.json, ou l'exécuter simplement pour utiliser le GUI
import sys, os, zipfile, json
from copy import deepcopy
from utils import *
from mscx_functions import *
from audiosettings_functions import *
from file_manip_functions import *

mscz_file_indicated, json_param_exists = False, False #solution par défaut

global GUI # à indiquer dans un config.py ?


try:
    import tkinter
    GUI = True
except:
    GUI = False
    print("La librairie GUI n'a pas pu être chargée. Le programme peut continuer, mais avec des options limitées. Installer la librairie avec \"pip install tkinter\"")
    if input("Voulez-vous continuer ?' [Y/n]\n") in ["Y","y", "O", "o",""]:
        pass
    else:
        print("Arrêt du programme")
        sys.exit()

# GUI = False
# global GUI_parameters

if GUI ==True:
    # Language = get_language() #TODO
    GUI_parameters = {
        "window_definition": "1200x800+50+50",
        # "Language": Language # à décider comment mettre en place
    } # à indiquer dans un config.py ?
    from GUI.Fenetres.Fenetre_1 import Fenetre_1
    from GUI.Fenetres.Fenetre_2 import Fenetre_2
    from GUI.Fenetres.Fenetre_3 import Fenetre_3
    from GUI.Fenetres.Fenetre_4 import Fenetre_4


if len(sys.argv)>1:
    mscz_file_indicated, mscz_file = controler_arg_file_mscz() #ok
    json_param_exists, json_file = controler_arg_fichier_json() #to do

if mscz_file_indicated == False:
    if GUI:
        # if False:
        app1 = Fenetre_1(GUI_parameters)
        app1.run()
        mscz_file = app1.mscz_file_var.get()
        json_file = app1.json_file_var.get()
        if os.path.isfile(json_file):
            json_param_exists = True
        else:
            json_param_exists = False
        # else:
        #     mscz_file="/home/alexandre/Documents/Medley_BG3_LN_AP_V2.mscz"
        #     json_file=""
        #     json_param_exists=False

    else:
        mscz_file, json_param_exists, json_file = CLI_get_mscz_and_json_files() #ok => (file manip.py)
        # si l'utilisateur appelle la fonction sans indiquer le fichier mscz, on ne prend rien d'autre en compte.

if json_param_exists == True:
    param = get_param_from_json_file(json_file) #TODO
    # à faire quand on aura une structure des paramètres pour le json

dir_mscz = os.path.dirname(mscz_file)

content_mscx, content_audiosettings, temp_mscx_folder, version_fichier = unzip_mscz(mscz_file) #ok

content_mscx = remove_nuances(content_mscx) #ok

line_body_def, line_body_notes, line_end_score, liste_voices_sous_voix_MS, liste_voices_accord, liste_name_id, list_dict_initial = identify_voices(content_mscx)

# liste_name_id = [[name, staff_id],...]
# list_dict_initial =[]
# for i in liste_name_id:
#     dict_temp = {
#         "trackname": i[0],
#         "id_staff": i[1],
#         "is_accompagnement": False
#     }
#     list_dict_initial.append(dict_temp)


# user input: déclaration des voix d'accompagnement
list_voix_accompagnement, gen_tutti = get_voix_accompagnement(liste_name_id, Fenetre_2,GUI_parameters, GUI) # Cette andouille a décidé que une variable globale ne se retouvait pas dans la fonction. C'est pas justement à ça que sert une variable globale ? Sinon, à la place de se casser le ***, on peut le passer comme argument

# print("list_dict_initial", list_dict_initial)
# print(list_voix_accompagnement)
list_dict_initial = update_list_initial(list_dict_initial, list_voix_accompagnement)
# print("list_dict_initial", list_dict_initial)

content_mscx_separated, correspondance_id_initial_incremente, list_dict_final = separate_voice(content_mscx, line_body_def, line_body_notes, line_end_score, liste_voices_sous_voix_MS, liste_voices_accord, liste_name_id, list_voix_accompagnement, list_dict_initial)
# correspondance_id_initial_incremente ~[id_initial, name_initial, list(id_new), list(name_new]]

# list_dict_final = update_list_final(list_dict_initial, list_dict_final)

path_to_mscx = save_mscx(content_mscx_separated, mscz_file)
# print("fichier sauvé")

####### pas besoin de générer la matrice des volumes, les valeurs de volumes sont fixées
# if GUI:
#     app3 = Fenetre_3(GUI_parameters, len(list_voix_accompagnement))
#     app3.run()
#     volume_voix_acc = app3.volume_voix_acc.get()
#     volume_voix_sec = app3.volume_voix_sec.get()
#     # to transfer to a function
# else:
#     pass
#     #TODO en CLI
#     # volume_voix_acc =
#     # volume_voix_sec =
# matrix, intitule_lignes_matrix, intitule_colonne_matrix, liste_voix_id_nom_new = generate_volume_matrix(volume_voix_acc, volume_voix_sec, correspondance_id_initial_incremente, list_voix_accompagnement, gen_tutti)
OSEF, intitule_lignes_matrix, intitule_colonne_matrix, liste_voix_id_name_new = generate_volume_matrix(0, 0, correspondance_id_initial_incremente, list_voix_accompagnement, gen_tutti)


# if GUI:
#     app4 = Fenetre_4(GUI_parameters, matrix, intitule_lignes_matrix, intitule_colonne_matrix)
#     app4.run()
#     matrix = app4.text_var.get()
# # pas d'alternative en l'absence de GUI, on garde la matrice par défaut

### temporary stop
print("terminé")
sys.exit()
###


if json_param_exists ==False:
    if GUI:
        param = GUI_get_param(list_voices)
    else:
        param = CLI_get_param(list_voices)

if json_param_exists == False and param["export_param"]==True:
    export_json_param_file(param, dir_mscz) # attention à ne pas exporter le fichier json dans le dossier temp, sinon il sera supprimé

######################
#   Metronome
######################
num_line_to_change, state_initial, path_ini_file = obtain_state_metronome()
# TODO: param_metronome = ... # True = exporte toutes les voix avec et sans métronome / False = exporte les voix sans métronome seulement

######################
#   change instrument sound
######################

#for voice in list_voices_separated:
liste_dossiers_temp = create_folder_per_voice(param, dir_mscz, content_mscx_separated) # ça crée aussi le fichier mscx + audiosettings de chaque voix
# generate_json_volume_per_voice(param) 
liste_fichiers_mscz = zip_folders(liste_dossiers_temp) #Les fichiers doivent être zippés sans dossier intermédiaire, et l'extension doit être changée à .mscz
#/for

json_job_path = generate_json_job_file(liste_fichiers_mscz, dir_mscz)

if state_initial == True: #pour la première volée d'exportation, on vérifie que le métronome est bien désactivé
    change_ini_file(num_line_to_change, state_initial, path_ini_file)

export_mp3(json_job_path, GUI, version_fichier) #export des mp3 sans métronome

# if param_metronome == True:
    # change_ini_file(num_line_to_change, False, path_ini_file)
    # TODO: json_job_path_metronome = alterate_json_job_file(json_job_path)
    # export_mp3(json_job_path_metronome, GUI)
    # change_ini_file(num_line_to_change, True, path_ini_file)

clear_unused_files(liste_dossiers_temp, liste_fichiers_mscz, json_job_path) #on garde le mscz tutti, qu'il sera possible d'input dans le script
