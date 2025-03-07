Il faut que le GUI prenne en compte les aspects de json_param. Ceux-ci n'ont pas encore été clairement établis.  
Entre autre:

- [ ] la matrice des volumes list(list\[int]) - unité soit en dB, soit en % (aucune idée si les valeurs sont linéaire ou log)
- [ ] Quelle voix est en accompagnement (réduction piano, qui est généralement à volume = 60%, ne pas dédoubler cette voix)
- [ ] volume pour la voix principale, volume pour les voix secondaires et volume pour l'accompagnement (déjà existant dans la version solo > à adapter)
- [ ] sélection du fichier mscz (idem  v solo)

Dans une v2, on pourra inclure les options suivantes:

- [ ] suppression des fichiers temporaires (v1: par défaut oui, sauf pour le mscz traité)
- [ ] génération des fichiers avec métronome (v1: par défaut oui)
- [ ] génération d'un fichier tutti (v1 par défaut oui)
- [ ] génération d'un fichier avec les nuances (v1: par défaut non)
- [ ] voix à ne pas faire entendre dans les mp3 (v1: possible en mettant volume à 0 dans la matrice)
- [ ] prise en compte de toute les voix ?
- [ ] préfixe/suffixe des fichiers mp3 générés
- [ ] enregistrement des settings dans un fichiers json_param
- [ ] importation du fichier json_param
- [ ] sélection du fichier ini pour le métronome si pas trouvé automatiquement
- [ ] sélection du fichier exe/appimage pour l'exécution du fichier batch si pas trouvé automatiquement
- [ ] instrument de la voix principale dans son fichier mp3 (v1: par défaut hautbois et clarinette
- [ ] voulez-vous lancer l'exécution du batch ou le faire plus tard de votre côté ?

Dans le GUI, inclure toutes les options et griser celles qui sont en WIP (et qui n'ont pas encore été implémentée dans le code)

Dans l'ordre le GUI affichera les fenêtres suivantes:
1. Sélection des fichiers
    1. sélection du fichier mscz
    2. WIP - bool: json_param_exists > if True: sélection du fichier mscz
2. Voix détectées 
    1. voix d'accompagnement
    2. WIP - voix à faire entendre dans l'audio et pour laquelle ne pas générer de fichier audio
    3. WIP - Voulez-vous créer un fichier tutti ?
4. volume    
    1. volume des voix secondaires
    2. volume de l'accompagnement
4. matrice des volumes
5. Instruments
   1. WIP - Voulez-vous générer des fichiers audio avec et sans métronome ? (décoché = seulement sans métronome)
   2. WIP - Voulez-vous générer des fichiers avec et sans nuance ? (décoché = seulement sans nuance)
   3. WIP - pour la voix x, quel instrument 
6. Finitions
    1. WIP - Voulez-vous supprimer les fichiers temporaires ? ["garder seulement le fichier mscz","garder les mscz des voix", ""]
    2. WIP - Voulez-vous enregistrer les paramètres indiqués ? (Pour pouvoir relancer rapidement ce programme en cas de changement)
    3. WIP - préfixe/suffixe des fichiers mp3 (laisser vide pour garder la configuration par défaut)
    4. WIP - Voulez-vous lancer l'exécution du batch immédiatement ou le faire plus tard de votre côté ?
7. WIP - (si problème dans le code) - indication du fichier .ini
8. WIP - (si problème dans le code) - indication du fichier .exe/.appimage