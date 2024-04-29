# jc2iy

Logiciel qui permet de simuler des résultats d'élection pour différentes méthodes de votes.


Génèration d'une population ainsi que des candidats pouvant être élus.

Chaque individu de la population représente un votant qui a une liste ordonnée des candidats (du préféré au moins préféré) selon son orientation politique.

Les différentes méthodes de vote disponibles sont :

    - Copeland
    - Borda
    - Pluralité
    - STV
    - Approbation


## Installation et téléchargement :

Installer au préalable les packages suivants :

[PySide6](https://pypi.org/project/PySide6/) :

```bash
pip install PySide6
```

[icecream](https://pypi.org/project/icecream/) :

```bash
pip install icecream
```

[numpy](https://pypi.org/project/numpy/) :

```bash
pip install numpy
```

Pour les fonctions de reconnaissances vocales et manuelles :

[mediapipe](https://pypi.org/project/mediapipe/) :

```bash
pip install mediapipe
```

[imageio](https://pypi.org/project/imageio/) :

```bash
pip install imageio
```

[fuzzywuzzy](https://pypi.org/project/fuzzywuzzy/) :

```bash
pip install fuzzywuzzy
```

[SpeechRecognition](https://pypi.org/project/SpeechRecognition/) :

```bash
pip install SpeechRecognition
```


Télécharger ce dossier et l'extraire dans votre répertoire courant (ou dans un autre répertoire mais il faudra alors faire de ce répertoire le répertoire courant dans le terminal)


## Lancement :

Dans le terminal, entrer la commande : 

```bash
python __main__.py
```


## Fonctionnalités :

Dans la fenêtre principale, plusieurs options afin de paramétrer la map :

    - Soumission : Ajout d'un rayon de population en entrant le rayon et la position du centre du cercle (x, y)
      ou cliquer directement sur la grille et entrer le nombre d'individus composant la population avec un rayon prédéfini
    - ajouter 0.1 : Augmenter le rayon du cercle de 0.1
    - ajouter -0.1 : Diminuer le rayon du cercle de 0.1
    - Supprimer : Supprimer la population
    - Activer CV : Activer le système de vision par ordinateur
    - Choix du type de génération :
        - Uniforme
        - Beta
        - Exponentiel
        - Triangulaire

    Une fois fini et que tous les paramètres ont été choisis :

    - Créer Map : Créer la map 3D ou 2D (au choix)


Une fois que la map a été créée :

    - Menu :
        - Soumission : Ajout manuel d'un candidat sur la map en entrant son nom, prénom, charisme et sa position (x, y)
        - Générer un Candidat : Génération d'un candidat avec un nom, prénom, charisme et une position (x, y) aléatoire
        - Sauvegarder : Sauvegarde du modèle actuel dans un fichier dont il faut entrer le nom (si non existant, il est automatiquement créé)
        - Recharger : Chargement d'un modèle dans un fichier dont il faut entrer le nom
        - Règles de vote (Liste des différentes règles de vote) :
            - Copeland
            - Borda
            - Pluralite
            - STV
            - Approbation
    
    - Statistiques :
        - Arbre tournoi : Affiche le résultat du tournoi sous forme d'arbre
        - Bilan Carbone : Affiche l'emission carbone depuis le lancement du logiciel
        - Visualisation 3D : Représentation des individus sur une surface 3D

    - Commande vocale


## Données émission carbone :

!! ATTENTION !!

Les mesures faites pour l'émission carbone ont été sur un ordinateur comportant un système AMD et NVIDIA.
Les mesures ont été faites en France de code iso FRA.
Les mesures sont susceptibles de changer d'un ordinateur à un autre.
Les mesures sont susceptibles de changer dans le temps.



## Credits :

Zhou Jeremy

Khamis Yara

Nistor Iarina

Kinane-Daouadji Isaac (scrum master)

Benhaddou Chady