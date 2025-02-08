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