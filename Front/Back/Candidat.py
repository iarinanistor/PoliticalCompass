import random

class Candidat:
    compteur = 0
    liste_nom=['Martin','Bernard','Petit','Laurent','Dupont','LeGall','Henry','Duval','Jouve','Baron']
    liste_prenom=['Louis','Gabriel','Arthur','Emma','Rose','Marceau','Tom','Iris','Chloe','Theo']
    def __init__(self,nom,prenom,charisme,age,x,y):
        self._nom = nom
        self._prenom = prenom
        self._charisme = charisme
        self._age = age
        self._x = x
        self._y = y
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
    
    def random_candidat(x,y):
        return Candidat( random.choice(Candidat.liste_nom),
                    random.choice(Candidat.liste_prenom),
                    random.randint(1,100),
                    random.randint(18,85),
                    random.random()*x,
                    random.random()*y
                    )
    def generate_candidats(n,x,y):
        l=[]
        for i in range(n):
            l.append(Candidat.random_candidat(x,y))
        return l

    #Methode qui affiche un candidat
    def affiche_candidat(candidat):
        '''
        Parameters:
            candidat : Candidat
        Returns:
            void : l'affichage d'un candidat
        '''
        return print(candidat.nom()+" "+candidat.prenom()+" age:"+str(candidat.age())+" charisme:"+str(candidat.charisme()))
