from copy import deepcopy
import sys, os, zipfile, json, shutil

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

# controler_arg_file_mscz()

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