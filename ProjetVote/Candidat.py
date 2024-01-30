import random

class Candidat:
    compteur = 0
    liste_nom=['Martin','Bernard','Petit','Laurent','Dupont','LeGall','Henry','Duval','Jouve','Baron']
    liste_prenom=['Louis','Gabriel','Arthur','Emma','Rose','Marceau','Tom','Iris','Chloe','Theo']
    def __init__(self):
        self._nom = random.choice(Candidat.liste_nom)
        self._prenom = random.choice(Candidat.liste_prenom)
        self._charisme = random.randint(1,10)
        self._age = random.randint(18,85)
        self._x = random.randint(0,100)
        self._y = random.randint(0,100)
        Candidat.compteur+=1
        self.id = Candidat.compteur

    def __hash__(self):
        return hash(self.id)

    def nom(self):
        return self._nom

    def prenom(self):
        return self._prenom


    def age(self):
        return self._age

    def charisme(self):
        return self._charisme
    
    def x(self):
        return self._x
    
    def y(self):
        return self._y
        
def generate_candidats(n):
    l=[]
    for i in range(n):
        l.append(Candidat())
    return l

l=generate_candidats(10)
