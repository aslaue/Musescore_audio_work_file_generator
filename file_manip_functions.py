from copy import deepcopy
import sys, os, zipfile, json, shutil

def CLI_get_mscz():
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

#def zip_mscz