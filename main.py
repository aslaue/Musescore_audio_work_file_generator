# instruction pour hekp: tu peux lancer python main.py -f file.mscz -p param.json, ou l'exécuter simplement pour utiliser le GUI
import sys, os, zipfile, json
from copy import deepcopy

mscz_file_indicated, json_param_exists = False, False #solution par défaut
GUI = False # pour l'instant, on utilise la bonne vieille manière "input"


if len(sys.argv)>1:
    mscz_file_indicated, mscz_file = controler_arg_file_mscz() #ok
    json_param_exists, json_file = controler_arg_fichier_json() #to do

if mscz_file_indicated == False:
    if GUI:
        mscz_file, json_param_exists, json_file = GUI_get_mscz() #to do (à adapter)
        # si l'utilisateur appelle la fonction sans indiquer le fichier mscz, on ne prend rien d'autre en compte.
    else:
        mscz_file, json_param_exists, json_file = CLI_get_mscz() #ok
        # si l'utilisateur appelle la fonction sans indiquer le fichier mscz, on ne prend rien d'autre en compte.
    
if json_param_exists == True:
    param = get_param_from_json_file(json_file) # à faire quand on aura une structure pour les json

dir_mscz = os.path.dirname(mscz_file)

content_mscx, content_audiosettings, temp_mscx_folder = unzip_mscz(mscz_file) #ok
content_mscx = remove_nuances(content_mscx) #ok
list_voices_separated, content_mscx_separated = detect_voices(content_mscx)


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

######################
#   change instrument sound
######################

liste_dossiers_temp = create_folder_per_voices(param, dir_mscz, content_mscx_separated) # ça crée aussi le fichier mscx de chaque voix
generate_json_volume_per_voice(param)
liste_fichiers_mscz = zip_folders(liste_dossiers_temp)
json_job_path = generate_json_job_file(liste_fichiers_mscz, dir_mscz)
export_mp3(json_job_path)
clear_unused_files(liste_dossiers_temp, liste_fichiers_mscz, temp_mscx_folder)
