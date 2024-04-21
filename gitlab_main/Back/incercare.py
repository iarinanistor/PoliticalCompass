
from random import uniform
from Individus import Individus
from Candidat import Candidat

cand1 = Candidat("Martin","chloe",4,50,60,60)
cand2 = Candidat("Grand","Nathan",5,46,42,55)
cand3 = Candidat("Petit","John",3,42,15,15)
l_candidats = [cand1,cand2,cand3]

ind1 = Individus("ind1",50,50,l_candidats)
print(ind1.poids)
#on fait un boucle imaginaire comme dans la generation aleatoire 
for i in range(100):
    poid = 1
    c = uniform(0, 1)
    #on veut ajouter ces choses dans le liste de cette individu
    #comment on sait prendre cette individu pour les ajouter comme ca:
    ind1.c.append(c)
    ind1.poids.append(poid)
