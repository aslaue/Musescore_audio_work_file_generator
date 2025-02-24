from copy import deepcopy
import sys, os, zipfile, json, shutil

def CLI_get_mscz_and_json_files():
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
    with open(dir_temp + "/" + os.path.basename(mscz_file).replace(".mscz",".mscx"), 'r') as mscx_file:
        content_mscx = mscx_file.readlines() # retourne une liste de str
    with open(dir_temp + "/audiosettings.json", 'r') as audiosettings_file:
        content_audiosettings = json.load(audiosettings_file) # retourne un dictionnaire
    return content_mscx, content_audiosettings, dir_temp

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
    mscx_file = mscz_file.replace(".mscz", ".mscx")
    # content_mscx_string =""
    # for line in content_mscx:
    #     content_mscx_string+=line
    with open(mscx_file ,'w') as file:
        # file.writelines(content_mscx_string)
        file.writelines(content_mscx)
    return mscx_file
    
def save_json(content_json, dir_mscz):
    json_file = dir_mscz + "generate_audio.json"
    # content_mscx_string =""
    # for line in content_mscx:
    #     content_mscx_string+=line
    with open(json_file ,'w') as file:
        # file.writelines(content_mscx_string)
        file.writelines(content_json)
    return json_file

def export_mp3(json_job_path, GUI):
    import sys
    if sys.platform =="linux":
        # sous linux, l'utilisation la plus courante est via Appimage => il faut localiser le fichier Appimage
        if GUI == False:
            appimage_file = input("indiquer le chemin du fichier Appimage de Musescore:\n")
        else:
            #TODO
            print()
        if os.path.isfile(appimage_file):
                command = f"./{appimage_file} -j {json_job_path}"
    elif "win" in sys.platform:
        default_MS_path = "C:\\Program Files\\MuseScore 4\\bin\\Musescore4.exe"
        if os.path.isfile(default_MS_path):
            command = f"./{default_MS_path} -j {json_job_path}"
        else:
            if GUI == False:
                exe_file = input("indiquer le chemin de l'exécutable de Musescore:\n")
            else:
                #TODO
                print()
            if os.path.isfile(exe_file):
                command = f"./{exe_file} -j {json_job_path}"
    elif "darwin" in sys.platform: # pour MacOS
        #TODO
        print()
    if command in vars():
        os.popen(command).read()[:-1]
    else:
        print("Le fichier du programme n'a pas été trouvé. On t'invite à chercher comment exécuter par toi même le fichier json.\nDes pistes se trouvent ici: 'https://musescore.org/en/handbook/3/command-line-options#EXAMPLES'")
        print(f"La commande à exécuter dans le terminal est du type \"mscore -j {json_job_path}\"")
    return


#def zip_mscz