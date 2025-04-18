from copy import deepcopy
import sys, os, zipfile, json, shutil
from utils import controle_version_partition

def CLI_get_mscz_and_json_files():
    """
    In case the user did not put the arguments when calling the main function, this function gets the information of the mscz file location and its eventual json parameter file
    Arguments:
        -

    Returns:
        input 1: string                 # path to the mscz file
        json_param_exists: boolean      # indicates if a json parameter file is filled out
        json_file: string               # path to the eventual json parameter file
    """
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

def unzip_mscz(mscz_file):
    """
    It unzip the mscz file into a temp folder (created for the occasion or purged if it already existed). The folder is located at the mscz location.
    It then reads the mscx file (XML format type), as well as the json file.
    Arguments:
        mscz_file: string     #path and name of the mscz file
    Returns:
        content_mscx: list(string)    # content of the mscx file (XML format-like), one line per element of the list
        content_audiosettings: dict   # content of the json file, formatted in dictionnary
        dir_tmp: string               # path to the unzipped files
    """
    dir_mscz = os.path.dirname(mscz_file)
    dir_temp = mscz_file.replace(".mscz", "_tutti")
    if os.path.isdir(dir_temp):
        shutil.rmtree(dir_temp)
    os.mkdir(dir_temp)
    with zipfile.ZipFile(mscz_file,'r') as zf:
        zf.extractall(path=dir_temp)
    for file in os.listdir(dir_temp):
        if file.endswith(".mscx"):
            filename_mscx = file
    # with open(dir_temp + "/" + os.path.basename(mscz_file).replace(".mscz",".mscx"), 'r') as mscx_file: # j'ai changé car si le mscz est enregistré puis renommé, le mscx garde l'ancien nom
    with open(dir_temp + "/" + filename_mscx, 'r') as mscx_file:
        content_mscx = mscx_file.readlines() # retourne une liste de str
    version_fichier = controle_version_partition(content_mscx) # s'assure que la partition est en version >=4, sinon la structure de fichier ne correspond pas => message erreur et arrêt du programme
    with open(dir_temp + "/audiosettings.json", 'r') as audiosettings_file:
        content_audiosettings = json.load(audiosettings_file) # retourne un dictionnaire
    return content_mscx, content_audiosettings, dir_temp, version_fichier

def create_folder_per_voice(dir_tutti: str, audiosettings_og: dict, voice_list: list=["Piano", "S", "A", "T", "B"]):
    """
    Early draft, it won't look like this at the end.
    Should probably be made into a wrapper function that also dispatches the respective audiosettings files. (in the main??)
    No need for a list in most ToF cases, just detect voices.
    """

    for voice in voice_list:

        voicedir = dir_tutti.replace("tutti", voice)
        shutil.copytree(dir_tutti, voicedir)
        #zip mscz

def save_mscx(content_mscx, mscz_file):
    """
    Saves the mscx file after its content was filtered and separated. The file will then be wrapped into a mscz file

    Arguments:
        content_mscz: list(string)      # file content to write into the file
    mscz_file: string                   # location of the original mscz, where the mscx file will be saved
    
    Returns:
        mscx_file: string               # path to the mscx file
    """
    mscx_file = mscz_file.replace(".mscz", ".mscx")
    # content_mscx_string =""
    # for line in content_mscx:
    #     content_mscx_string+=line
    with open(mscx_file ,'w') as file:
        # file.writelines(content_mscx_string)
        file.writelines(content_mscx)
    return mscx_file
    
def save_json(content_json, dir_mscz):
    """
    Saves the json instruction file listing the mscz files to convert to mp3

    Arguments:
        content_json: list(string)      # file content to write into the file
        dir_mscz: string                # location of the original mscz. Also the location where the json file will be saved
    
    Returns:
        json_file: string               # path to the json_file
    """
    json_file = dir_mscz + "generate_audio.json"
    # content_mscx_string =""
    # for line in content_mscx:
    #     content_mscx_string+=line
    with open(json_file ,'w') as file:
        # file.writelines(content_mscx_string)
        file.writelines(content_json)
    return json_file

def export_mp3(json_job_path, GUI, version_fichier):
    """
    execute the command to convert the mscz to mp3, following the json file.
    Arguments:
        json_job_path: string       # path to the json file containing the instruction
        GUI: boolean                # determining if the instruction to find the execution file are with CLI or with GUI (WIP) 
    Returns:
        -
    """
    import sys
    if sys.platform =="linux":
        # sous linux, l'utilisation la plus courante de MuseScore ≥4.0 est via Appimage => il faut localiser le fichier Appimage
        if GUI == False:
            appimage_file = input("indiquer le chemin du fichier Appimage de Musescore:\n")
        else:
            #TODO
            print()
        if os.path.isfile(appimage_file):
            command = f"./{appimage_file} -j {json_job_path}"
            controle_version_musescore(version_fichier, f"./{appimage_file} --version", command)
    elif "win" in sys.platform:
        default_MS_path = "C:\\Program Files\\MuseScore 4\\bin\\Musescore4.exe"
        if os.path.isfile(default_MS_path):
            command = f"./{default_MS_path} -j {json_job_path}"
            controle_version_musescore(version_fichier, f"./{default_MS_path} --version", command)
        else:
            if GUI == False:
                exe_file = input("indiquer le chemin de l'exécutable de Musescore:\n")
            else:
                #TODO
                print()
            if os.path.isfile(exe_file):
                command = f"./{exe_file} -j {json_job_path}"
                controle_version_musescore(version_fichier, f"./{exe_file} --version", command)
    elif "darwin" in sys.platform: # pour MacOS
        #TODO
        print()
    if command in vars():
        os.popen(command).read()[:-1]
    else:
        print("Le fichier du programme n'a pas été trouvé. On t'invite à chercher comment exécuter par toi même le fichier json.\nDes pistes se trouvent ici: 'https://musescore.org/en/handbook/3/command-line-options#EXAMPLES'")
        print(f"La commande à exécuter dans le terminal est du type \"mscore -j {json_job_path}\"")
    return

def obtain_state_metronome():
    """
    The function goes into the config .ini file of MuseScore and checks whether or not the Metronome is enabled.
    It returns the location of the file in order to modify it later in the change_ini_file function, as well as the parameter location in the file and the statement
    Returns:
        num_line_to_change
        state_initial
        path_ini_file
    """
    if "linux" in sys.platform:
        try:
            path_ini_file = os.environ['XDG_CONFIG_HOME'] + "/MuseScore/MuseScore4.ini"
            if os.path.isfile(path_ini_file) == False:
                path_ini_file = os.environ['HOME'] + "/.config/MuseScore/MuseScore4.ini"
        except:
            path_ini_file = os.environ['HOME'] + "/.config/MuseScore/MuseScore4.ini"
    elif "win" in sys.platform:
        path_ini_file = path_ini_file = os.environ["APPDATA"] + "/MuseScore/MuseScore4.ini"
        

    if os.path.isfile(path_ini_file) == False:
        if GUI:
            #TODO: transformer le CLI en fenêtre GUI
            # print("Le fichier ini n'a pas été trouvé automatiquement. Vérifier que le logiciel MuseScore 4 a été ouvert au moins une fois (les version antérieures à la V4.0.0 ne fonctionnent pas avec ce programme)")
            # if "win" in sys.platform: # spécificité windows MS4 portable: hint
            #     print("Ayant détecté le système d'exploitation Windows, dans le cas où vous utilisez une version de MuseScore 4 portable, le fichier ini se trouve dans l'arborescence du dossier contenant l'exécutable portable.\nPlus exactement, depuis le dossier 'MuseScore 4 Portable' (ou nom similaire), indiquer au prompt le path complet pointant vers '.../MuseScore 4 Portable/Data/settings/MuseScore/MuseScore4.ini'")
            pass
            #TODO: ajouter la fonctionnalité askfile => se baser sur fenêtre 1
        else:
            print("Le fichier ini n'a pas été trouvé automatiquement. Vérifier que le logiciel MuseScore 4 a été ouvert au moins une fois (les version antérieures à la V4.0.0 ne fonctionnent pas avec ce programme)")
            if "win" in sys.platform: # spécificité windows MS4 portable: hint
                print("Ayant détecté le système d'exploitation Windows, dans le cas où vous utilisez une version de MuseScore 4 portable, le fichier ini se trouve dans l'arborescence du dossier contenant l'exécutable portable.\nPlus exactement, depuis le dossier 'MuseScore 4 Portable' (ou nom similaire), indiquer au prompt le path complet pointant vers '.../MuseScore 4 Portable/Data/settings/MuseScore/MuseScore4.ini'")
            path_ini_file = input("Veuillez indiquer le fichier ini de Musescore:\n")

    file = open(path_ini_file, 'r')
    data = file.readlines()

    found = False
    for num_line,line in enumerate(data):
        if "playback\\metronomeEnabled=" in line:
            num_line_to_change = num_line
            found = True
            break
    if found==False: # si à la fin, la ligne n'a pas été trouvée
        # 2 possibilités: 
        # - soit on dit que pas trouvé et tant pis (mais c'est ennuyant)
        # - soit on ajoute la ligne vu qu'elle n'existe pas (on la fixe en False)
        if False:
            print("Le fichier ini a été trouvé, mais ne contient pas de ligne pour le métronome. Veuillez vous assurer d'avoir ouvert une fois MuseScore 4, avoir créé une partition, l'avoir enregistré une fois avec le métronome activé, et une fois sans l'activé, puis fermer MuseScore avant de relancer le script")
            return False, False, ""
        else:
            pass
            with open(path_ini_file, 'a') as file:
                file.write("playback\\metronomeEnabled=False")
            num_line_to_change = num_line +1
            state_initial = False
            return num_line_to_change, state_initial, path_ini_file
    
    line_to_change = data[num_line_to_change]
    print(line_to_change)
    if "true" in line_to_change:
        state_initial = True
    elif "false" in line_to_change:
        state_initial = False
        
    return num_line_to_change, state_initial, path_ini_file

def change_ini_file(num_line_to_change, state_initial, path_ini_file):
    """
    As the name implies, the function change the MuseScore 4 settings .ini file to toggle the metronome
    """
    file = open(path_ini_file, 'r')
    data = file.readlines()
    line_to_change = data[num_line_to_change]
    if state_initial == True:
        line_changed = line_to_change.replace("true","false")
    else:
        line_changed = line_to_change.replace("false","true")

    new_data = data[:num_line_to_change] + [line_changed] + data[num_line_to_change+1:]

    with open(path_ini_file,'w') as file:
        file.writelines(new_data)



#def zip_mscz