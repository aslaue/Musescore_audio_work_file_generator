# Ce qu'il fait
Dans le cas où une portée a à un moment 2 sous-voix dans la même mesure, puis la mesure suivante n'a plus qu'une sous-voix
![7d35d64777f2687b707a04331ae167cf.png](../../_resources/7d35d64777f2687b707a04331ae167cf.png)
Il générera une partition de ce type:
![95fd3d1a5bf32f37278d3806e8539dc2.png](../../_resources/95fd3d1a5bf32f37278d3806e8539dc2.png)
Attention à ce que la deuxième mesure du mscz initial n'ait pas de sous-voix sous forme de silence:
![3b090f5ae7ac49062cdd680058d7ca64.png](../../_resources/3b090f5ae7ac49062cdd680058d7ca64.png)

# Ce qu'il ne fait pas:
## Combinaison cheloue
Dans une situation où il y a une combinaison d'accord et sous-voix comme ceci (il y a donc 3 sous-voix):
![583121a88bb2cdd4c528bdcc84200452.png](../../_resources/583121a88bb2cdd4c528bdcc84200452.png)
Le code ne pourra pas effectuer la séparation en une fois.
Il générera une partition de ce type:
![98ccdff219a00de2418cb1e566604676.png](../../_resources/98ccdff219a00de2418cb1e566604676.png)
Cependant, rien ne vous empêche de relancer une deuxième fois le code sur le mscz généré pour séparer la première voix des soprano afin d'obtenir 3 voix de soprano distincte
## Les brackets
Étant donné que le fichier mscz généré n'a pas vocation à être utilisé en mode graphique, nous ne nous sommes pas cassés le c\*\* à modifier l'affichage des brackets. L'affichage actuel ressemble à ça après process
![b03161d4fe6634d45b47576c63f3b529.png](../../_resources/b03161d4fe6634d45b47576c63f3b529.png)