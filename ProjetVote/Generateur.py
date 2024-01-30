from Candidat.py import Candidat
from random import randint,choice


def generate_candidats(n):
    liste_nom={Martin,Bernard,Petit,Laurent,Dupont,LeGall,Henry,Duval,Jouve,Baron}
    liste_prenom={Louis,Gabriel,Arthur,Emma,Rose,Marceau,Tom,Iris,Chloe,Theo}

    liste_candidats=[]
    for i in range(n):
        nom = random.choice(liste_nom)
        prenom = random.choice(liste_prenom)
        charisme = randint(1,10)
        age = randint(18,85)
        """il reste a ajouter une methode pour x et y - coordonnees politiques"""
        liste_candidats.append(Candidat(nom,prenom,age,charisme))
    return liste_candidats
    
