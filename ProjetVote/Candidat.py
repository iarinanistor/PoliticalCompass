class Candidat:
    compteur = 0
    def __init__(self,nom,prenom,age,charisme,x=None,y=None):
        self._nom = nom
        self._prenom = prenom
        self._age = age 
        self._charisme = charisme
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
        
