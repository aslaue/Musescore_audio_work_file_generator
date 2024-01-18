import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfile
from tkinter import messagebox
import os
from fenetre2 import DesignOutilMusescoreApp_fenetre2
from fenetre3 import DesignOutilMusescoreApp_fenetre3
from fenetre4 import DesignOutilMusescoreApp_fenetre4
import sys

def open_file():
    if sys.platform=='linux':
        file = askopenfile(mode ='r', filetypes =[('Musescore Files', '.mscz .musicxml')],initialdir='~/Documents', title='Sélectionner le fichier de partition')
    elif 'win' in sys.platform: # windows
        file = askopenfile(mode ='r', filetypes =[('Musescore Files', '.mscz .musicxml')], title='Sélectionner le fichier de partition')

    if file is not None:
        # content = file.read()
        # print(content)
        path_and_name=str(file).split('name=\'')[1].split('\'')[0]
        if path_and_name.endswith(".mscz")==True:
            convert_to_musicxml(path_and_name)
            path_and_name+=".musicxml"
        return path_and_name
    else:
        return 1

def convert_to_musicxml(path_and_name_mscz):
    # insert code to check if MuseScore exists in $PATH
    # ***
    # if it does not recognise, it displays a tutorial to export in MS4 manually in musicxml file 

    print('conversion mscz > mscz.musicxml en cours')
    print("si une erreur devait apparaitre à cause de mauvaise version de MS, il est possible d'exporter manuellement le fichier en musicxml dans MS4. par exemple \n")
    if sys.platform=='linux':
        commande = 'musescore3 ' + path_and_name_mscz + ' -o ' + path_and_name_mscz + '.musicxml' #le nom du fichier généré sera du type partition.mscz.xml
    # ~ if sys.platform=='': # mac
        # ~ du type mscore [options] [filename …] (Mac and Linux/BSD/Unix)
    if 'win' in sys.platform: # windows
        default_MS_path = ".\MuseScorePortableLegacy3\MuseScorePortable.exe"
        commande = default_MS_path + ' ' + path_and_name_mscz.replace('/','\\') + ' -o ' + path_and_name_mscz.replace('/','\\') + '.musicxml'
        commande = "\"{}\" \"{}\" -o \"{}.musicxml\"".format(default_MS_path , path_and_name_mscz, path_and_name_mscz)
        # print(os.path.exists(path_and_name_mscz))
        # # commande = "pouette"
        # # commande.replace('\\','\\\\').replace('/','\\')
        # messagebox.showinfo("Alerte", "Malheureusement la conversion sur Windows ne fonctionne pas (ou du moins je n'arrive pas à la faire fonctionner par ligne de commmande\nJe suggère en attendant que ce soit réglé d'exporter manuellement le fichier mscz en musicxml")
        # sys.exit()

    print(commande)
    os.popen(commande).read()[:-1]
    if os.path.exists(path_and_name_mscz + '.musicxml'):
        print("\n {} successfully created".format(path_and_name_mscz + '.musicxml')) 
    else:
        messagebox.showinfo("Alerte", "Il y a eu un problème lors de la conversion du fichier mscz en musicxml (le fichier utilisé a probablement été généré par MS4).\n Si ce problème persiste, je te recommande d'exporter manuellement ton fichier musicxml depuis le programme Musescore")
        sys.exit()

def detection_voix(path_and_name):
    with open(path_and_name,'r') as f:
        data=f.readlines()
    
    ligne_voix=[]
    for i in range(0,len(data)):
    	if data[i].find('<score-part id')!=-1:
    		ligne_voix.append(i)
    	if data[i].find('</part-list>')!=-1:
    		break
    measure_nb=0
    for j in range(i,len(data)):
        if data[j].find('<measure number=')!=-1:
            measure_nb=max(measure_nb,(int(data[j].split('"')[1])))
    
    # print("il y a {} mesures".format(measure_nb))
    nb_voix=len(ligne_voix)
    
    # print(ligne_voix)
    # print('Les ' + str(nb_voix) + ' différentes voix détectées sont les suivantes: \n')
    
    id_voix=[]
    nom_voix=[]
    abr_voix=[]
    
    for i in range(0,nb_voix):
    	id_voix.append(data[ligne_voix[i]][20:len(data[ligne_voix[i]])-3])
    	nom_voix.append(data[ligne_voix[i]+1][17:len(data[ligne_voix[i]+1])-13])
    	abr_voix.append(data[ligne_voix[i]+2][25:len(data[ligne_voix[i]+2])-21])

    return id_voix, nom_voix, abr_voix , measure_nb, ligne_voix, data

def automatisation_texte(id_voix, nom_voix, abr_voix):
	str1=""
	for i in range(len(id_voix)):
		str1 += "{}: {} ({})\n".format(id_voix[i],nom_voix[i],abr_voix[i])
		# print(str1)
	# print(str1)
	return str1

def selection_accompagnement_et_parametres_GUI():
	app3 = DesignOutilMusescoreApp_fenetre3(nom_voix)
	app3.run()
	
	voies_acc=app3.selected_options
	fichier_tutti=app3.checkbutton1_var.get()
	option_avancee=app3.checkbutton2_var.get()
	vol_voix_prin=app3.box_vol_voix_prin_var.get()
	vol_voix_acc = app3.box_vol_voix_acc_var.get()
	vol_voix_autre = app3.box_vol_voix_autre_var.get()
	
	# print("voies d'accompagnement",voies_acc)
	# print("fichier tutti?", fichier_tutti)
	# print("options avancées?",option_avancee)
	# print("Volume voix du fichier",vol_voix_prin)
	# print("volume voix accompagnement",vol_voix_acc)
	# print("volume voix autres voix",vol_voix_autre)
	
	if vol_voix_acc == "":
		vol_voix_acc=60
	if vol_voix_autre == "":
		vol_voix_autre=20
	if vol_voix_prin == "":
		vol_voix_prin=100
	
	return voies_acc, fichier_tutti, option_avancee, vol_voix_prin, vol_voix_acc, vol_voix_autre

def changer_volume(data_transformed, ligne_voix_j, volume):
    data_transformed[ligne_voix_j+10] = data[ligne_voix_j+10][0:16] +\
		str(volume*0.787402) +\
		data[ligne_voix_j+10][-10:]
		# str(volume*0.787402) +\
		#Dans MS3, si volume = [100,60,0] => volume Musicxml = [78.7402, 47.2472,0]


def enregistrer_fichier(data_transformed,nom_fichier):
	# print(path_dossier_temporaire + nom_fichier)
	with open(path_dossier_temporaire + nom_fichier,'w') as f:
		f.writelines(data_transformed)
	return path_dossier_temporaire + nom_fichier
#
#
#
#
# FIN DES FONCTIONS
#################################

default_MS_path = ".\MuseScorePortableLegacy3\MuseScorePortable.exe"


## 
path_and_name = open_file()
# print(path_and_name)
#print(os.path.exists(path_and_name))
position=[]
for i,character in enumerate(path_and_name):
    if character =='/':
        position.append(i)

path = path_and_name[0:position[-1]+1]
name = path_and_name[position[-1]+1:]

# print(path)


id_voix, nom_voix, abr_voix , measure_nb, ligne_voix, data = detection_voix(path_and_name)

texte_mis_en_page_voix = automatisation_texte(id_voix, nom_voix, abr_voix)
# print(texte_mis_en_page_voix)

#################################


# print("ok")
app = DesignOutilMusescoreApp_fenetre2(measure_nb, id_voix, nom_voix, texte_mis_en_page_voix)
app.Fenetre2.wait_window()

voies_accompagnement, fichier_tutti, option_avancee, vol_voix_prin, vol_voix_acc, vol_voix_autre = selection_accompagnement_et_parametres_GUI()
# print("voies_accompagnement", voies_accompagnement)

###############################################################################
### génération de la matrice

id_voix_prin, nom_voix_prin, abr_voix_prin, ligne_voix_prin = list(id_voix), list(nom_voix), list(abr_voix), list(ligne_voix)
# ATTENTION, il ne faut pas faire bêtement ligne_voix_prin = ligne_voix, car dans Python, s'il y a une liste L1, et on exécute L2=L1, on ne fait en fait que copier un pointeur, et donc si on suprime L2[0], alors cela suprime aussi L1[0]
ligne_voix_acc = []

# print("ligne_voix",ligne_voix)
# print("len(ligne_voix)",len(ligne_voix))
if len(voies_accompagnement)>0:
	# for n,i in enumerate(nom_voix):
	for n,i in reversed(list(enumerate(nom_voix))):
		# print("\n\n n",n)
		# print(i)
		# print("id_voix_prin",id_voix_prin)
		# print("ligne_voix[n]",ligne_voix[n])
		for j in voies_accompagnement:
			if i==j:
				# print("elimintation", i)
				del id_voix_prin[n]
				del nom_voix_prin[n]
				del abr_voix_prin[n]
				# print(ligne_voix)
				del ligne_voix_prin[n]
				# ligne_voix_acc.append(105)
				# print(ligne_voix)
				ligne_voix_acc.append(ligne_voix[n])
	# print(nom_voix_prin)
	matrix=[]
	for i in range(len(id_voix_prin)):
		row=[]
		row.append(abr_voix_prin[i])
		for j in range(len(id_voix_prin)+1):
			if j==i: # principal
				row.append(vol_voix_prin)
			elif j==len(id_voix_prin): # colonne accompagnement
				row.append(vol_voix_acc)
			else:
				row.append(vol_voix_autre)
		matrix.append(row)
	if fichier_tutti:
		#pour la dernière ligne (accompagnement)
		row=[]
		row.append("tutti")
		for j in range(len(id_voix_prin)+1):
			if j==len(id_voix_prin): # colonne accompagnement
					row.append(vol_voix_acc)
			else:
				row.append(vol_voix_prin)
		matrix.append(row)
else: # s'il n'y a pas de voix d'accompagnement
	matrix=[]
	for i in range(len(id_voix_prin)):
		row=[]
		row.append(abr_voix_prin[i])
		for j in range(len(id_voix_prin)):
			if j==i: # principal
				row.append(vol_voix_prin)
			else:
				row.append(vol_voix_autre)
		matrix.append(row)
	if fichier_tutti:
		#pour la dernière ligne (accompagnement)
		row=[]
		row.append("tutti")
		for j in range(len(id_voix_prin)):
			row.append(vol_voix_prin)
		matrix.append(row)
# print(matrix)

if option_avancee:
	liste_des_voies = "\t"
	for i in abr_voix_prin:
		liste_des_voies += i + "\t"
	if len(voies_accompagnement)>0:
		liste_des_voies += "acc"
	# print(liste_des_voies)
	texte_matrix = ""
	for i in matrix:
		for j in i:
			texte_matrix+=str(j) + "\t"
		texte_matrix+="\n"
	app4 = DesignOutilMusescoreApp_fenetre4(liste_des_voies, texte_matrix)
	# app4 = DesignOutilMusescoreApp_fenetre4()
	app4.run()
	#
	clean_up_temp_folder = app4.clean_up_temp_folder.get()
	clean_up_output_folder = app4.clean_up_output_folder.get()
	delete_temp_folder = app4.delete_temp_folder.get()
	matrix_fenetre4 = app4.text_var.get()
	# print(matrix_fenetre4)
	if matrix_fenetre4!=texte_matrix:
		m=len(matrix)
		n=len(matrix[0])
		matrix=[] 
		for row in matrix_fenetre4.split("\n")[:m]:
			ligne=[]
			ligne.append(row.split("\t")[0])
			for i in row.split("\t")[1:n]:
				ligne.append(int(i))
			matrix.append(ligne)
		# print(matrix)
	# nom_fichier_autre = app4.nom_fichier_autre.get()
	# print(nom_fichier_autre)
else:
	delete_temp_folder=True
	clean_up_output_folder=True
	clean_up_temp_folder=True

###############################################################################
# Génération des fichiers temporaires musicxml

fichiers_musicxml_crees=[]

path_dossier_temporaire = path+'fichiers_temp/'
if not os.path.exists(path_dossier_temporaire):
	os.mkdir(path_dossier_temporaire)
else:
	if clean_up_temp_folder:
		for i in os.listdir(path_dossier_temporaire):
			# print(path_dossier_temporaire + i)
			os.remove(path_dossier_temporaire+i)

nb_voix_prin = len(ligne_voix_prin)
nb_fichiers = len(matrix) # correspond au nombre de lignes de la matrice

for num,i_file in enumerate(range(nb_fichiers)):
    data_transformed = data
    ligne_volume=matrix[num][1:] # on ne prend pas la première colonne (qui équivaut au nom)
    for num2,ligne_voix_i in enumerate(ligne_voix_prin):
        volume = ligne_volume[num2]
        changer_volume(data_transformed, ligne_voix_i, volume)
    if len(voies_accompagnement)>0:
        volume = ligne_volume[-1]
        for ligne_voix_i in ligne_voix_acc:
            changer_volume(data_transformed, ligne_voix_i, volume)
    nom_voix_i = matrix[num][0]
    nom_fichier = '{}_{}.mscz.musicxml'.format(name.split('.')[0] , nom_voix_i.replace('.','') )
    fichiers_musicxml_crees.append(enregistrer_fichier(data_transformed,nom_fichier))



###############################################################################
#### Création du dossier output

path_output = path + "output_" + name.split('.')[0] + '/'
print("path_output",path_output)
if not os.path.exists(path_output):
	os.mkdir(path_output)
else:
	if clean_up_output_folder:
		for i in os.listdir(path_output):
			# print(path_dossier_temporaire + i)
			os.remove(path_output+i)

commande_liste = []
for i in fichiers_musicxml_crees:
    if sys.platform=="linux":
        commande = 'musescore3 ' + i + ' -o ' + i.replace(path_dossier_temporaire,path_output) + ".mp3\n"
    elif "win" in sys.platform:        
        commande = "\"{}\" \"{}\" -o \"{}.mp3\"\n".format(default_MS_path , i , i.replace(path_dossier_temporaire,path_output))
        print(commande)
    commande_liste.append(commande)
# print(commande_liste)

with open(path + "commandes.txt",'w') as f:
    f.writelines(commande_liste)


print("\n ------------------ generation of the mp3 files -------------- \n")
for k,i in enumerate(commande_liste,1):
	print("\n" + i + "\n")
	os.popen(i).read()[:-1]
	print("process {} sur {} terminé".format(k,len(commande_liste)))
	# break


###############################################################################
# Suppression éventuelle des fichiers temporaires
if delete_temp_folder:
	for i in os.listdir(path_dossier_temporaire):
		# print(path_dossier_temporaire + i)
		os.remove(path_dossier_temporaire+i)
	os.removedirs(path_dossier_temporaire)

messagebox.showinfo("Alerte", "Programme terminé correctement, presser \"Enter\" pour fermer la fenêtre")
