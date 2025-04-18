## Qu'est-ce qu'on appelle un fichier de travail ?
Un fichier de travail est un fichier audio généré à partir d'une partition MuseScore. Il peut être utile notamment dans une chorale. Il met en avant une voix spécifique qui ressort des autres voix et de l'accompagnement. 
## Pourquoi utiliser le script pour générer les fichiers de travail ?
La génération du fichier en elle-même ne prend pas tant de temps que ça. Cependant, dans une chorale, chaque voix a besoin du fichier de travail (4 ou 8 génération de fichiers), et le changement de setup pour générer les fichiers est chronophage. (Si vous voulez voir toutes les étapes pour créer un fichier de travail manuellement, consulter ==cette page==)
Le script crée une version épurée de la partition, change les volume et la sonorité des voix pour générer les fichiers de travail, sans avoir besoin d'input humain à chaque génération de fichier

## Comment faire fonctionner le script
- Télécharger l'archive la plus récente du projet en cliquant sur ==ce lien==.
- Exécuter dans python le fichier main.py (cliquer ==ici== pour afficher un guide d'installation de python)
- Dans les fenêtres qui s'affichent, indiquer à partir de quel partition MuseScore générer les fichiers de travail, la configuration (volumes, sonorité des instruments pour les voix à mettre en avant)
- Laisser mouliner un peu
- Vos fichiers de travail ont été générés dans le dossier dans la partition

## De quoi mon script a besoin pour fonctionner:
- Du logiciel MuseScore (version  ≥ 4.0)
- De python (testé sur la version 3.11, mais la 3.)
- De partition en format mscz
- facultatif mais vivement recommandé: librairie python Tkinter (guide d'installation **ici**)