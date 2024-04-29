#!/bin/bash

# Rend le script Python exécutable
chmod +x ./gitlab_main/__main__.py

# Navigue dans le bon répertoire
cd gitlab_main || exit

# Active l'environnement virtuel
source ../ProjectEnv/bin/activate

# Exécute le script Python avec Python 3
python3 __main__.py