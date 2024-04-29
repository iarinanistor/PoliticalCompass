#!/bin/bash

#uniquement pour mac avec puce arm( M1 ,M2 , M3 )

# Création de l'environnement virtuel nommé ProjectEnv
python3 -m venv ProjectEnv

# Activation de l'environnement virtuel
source ../ProjectEnv/bin/activate

# Mise à jour de pip (optionnel mais recommandé)
pip install --upgrade pip

# Installation des dépendances à partir du fichier requirements.txt
pip install -r requirements.txt

echo "L'environnement virtuel et les dépendances ont été installés."
