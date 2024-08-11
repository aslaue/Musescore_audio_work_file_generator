def controler_arg_file_mscz():
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

def controler_arg_fichier_json():
    import sys
    # print(sys.argv)
    json_param_exists =False
    for k,i in enumerate(sys.argv[1:]):
        if i=="-p":
            json_file = sys.argv[k+1]
            json_file =True
            break
    if json_param_exists ==True:
        if json_file.endswith(".json") and os.path.isfile(json_file):
            # l'extension du fichier correspond, et le fichier existe
            return json_param_exists, json_file
    return False, ""

def CLI_get_mscz():
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

def extract_mscx(mscz_file):
    import os
    dir_mscz = os.path.dirname(mscz_file)
    dir_temp = dir_mscz + "/temp"
    if os.path.isdir(dir_temp):
        import shutil
        shutil.rmtree(dir_temp)
    os.mkdir(dir_temp)
    with zipfile.ZipFile(mscz_file,'r') as zf:
        zf.extractall(path=dir_temp)
    with open(dir_temp + "/" + os.path.basename(mscz_file).replace(".mscz",".mscx"), 'r') as mscx_file:
        content_mscx = mscx_file.readlines() # retourne une liste de str
    return content_mscx, dir_temp

def remove_nuances(content_mscx):
    mots_skip_intro = ['<Dynamic>','<Spanner type="HairPin">','<Fermata>']
    mots_skip_end = ['</Dynamic>','</Spanner>','</Fermata>']
    #<Dynamic> et </Dynamic> => nuance volume (f, mp ppp)
    #<Spanner type="HairPin"> et le prochain </Spanner> => crescendo, diminuendo, decrescendo
    #<Fermata> ... </Fermata> => pt d'orgue
    # les diminuendo, les Rallentando, les Ritardando aussi ?
    content_temp =[]
    for i in len(mots_skip_end):
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
