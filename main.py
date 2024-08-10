# instruction pour hekp: tu peux lancer python main.py -f file.mscz -p param.json, ou l'exécuter simplement pour utiliser le GUI

mscz_file_indicated, mscz_file = controler_arg_file_mscz()
json_param_exists, json_file = controler_arg_fichier_json()

if mscz_file_indicated == False:
    # mscz_file,json_param_exists, json_file = GUI_get_mscz() # si l'utilisateur appelle la fonction sans indiquer le fichier mscz, on ne prend rien d'autre en compte.
    mscz_file,json_param_exists, json_file = CLI_get_mscz() # si l'utilisateur appelle la fonction sans indiquer le fichier mscz, on ne prend rien d'autre en compte.
    
if json_param_exists == True:
    param = get_param_from_json_file(json_file)

dir_mscz = get_dir_from_mscz()

content_mscx, temp_mscx_folder = extract_mscx(mscz_file)
content_mscx = remove_nuances(content_mscx)
list_voices_separated, content_mscx_separated = detect_voices(content_mscx)


if json_param_exists ==False:
    # param = GUI_get_param(list_voices)
    param = CLI_get_param(list_voices)

######################
#   Metronome
######################

######################
#   change instrument sound
######################

liste_dossiers_temp = create_folder_per_voices(param, dir_mscz, content_mscx_separated) # ça crée aussi le fichier mscx de chaque voix
generate_json_volume_per_voice(param)
liste_fichiers_mscz = zip_folders(liste_dossiers_temp)
export_mp3(liste_fichiers_mscz, dir_mscz)
clear_unused_files(liste_dossiers_temp, liste_fichiers_mscz, temp_mscx_folder)
