# instruction pour hekp: tu peux lancer python main.py -f file.mscz -p param.json, ou l'exécuter simplement pour utiliser le GUI
import sys, os, zipfile, json
from copy import deepcopy
from utils import *
from mscx_functions import *
from audiosettings_functions import *
from file_manip_functions import *

mscz_file_indicated, json_param_exists = False, False #solution par défaut
GUI = False # pour l'instant, on utilise la bonne vieille manière "input"

if GUI ==True:
    # require additional library tkinter
    # from fenetre2 import DesignOutilMusescoreApp_fenetre2
    break


if len(sys.argv)>1:
    mscz_file_indicated, mscz_file = controler_arg_file_mscz() #ok
    json_param_exists, json_file = controler_arg_fichier_json() #to do

if mscz_file_indicated == False:
    if GUI:
        mscz_file, json_param_exists, json_file = GUI_get_mscz() #to do (à adapter)
        # si l'utilisateur appelle la fonction sans indiquer le fichier mscz, on ne prend rien d'autre en compte.
    else:
        mscz_file, json_param_exists, json_file = CLI_get_mscz_and_json_files() #ok => (file manip.py)
        # si l'utilisateur appelle la fonction sans indiquer le fichier mscz, on ne prend rien d'autre en compte.
    
if json_param_exists == True:
    param = get_param_from_json_file(json_file) # à faire quand on aura une structure pour les json

dir_mscz = os.path.dirname(mscz_file)


content_mscx, content_audiosettings, temp_mscx_folder = unzip_mscz(mscz_file) #ok
content_mscx = remove_nuances(content_mscx) #ok
list_voices_separated, content_mscx_separated = separate_voice(content_mscx)
path_to_mscx = save_mscx(content_mscx_separated, mscz_file)

# ### temporary stop
# print("terminé")
# sys.exit()
# ###


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

export_mp3(json_job_path, GUI) #export des mp3 sans métronome

# if param_metronome == True:
    # change_ini_file(num_line_to_change, False, path_ini_file)
    # TODO: json_job_path_metronome = alterate_json_job_file(json_job_path)
    # export_mp3(json_job_path_metronome, GUI)
    # change_ini_file(num_line_to_change, True, path_ini_file)

clear_unused_files(liste_dossiers_temp, liste_fichiers_mscz, json_job_path) #on garde le mscz tutti, qu'il sera possible d'input dans le script
