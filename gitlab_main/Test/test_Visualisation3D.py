from Back.Visialisation3D import visualiser_surface_3d
from Back.Map import Map

if __name__ == '__main__':
    a="Triangulaire"
    b="Uniforme"
    c="Exponentiel"
    d="Beta"   


    pop = [[None]*100]*100 # obligatoire pour creer la matrice
    nbIndividus = 10000 # mettre un grand nombre d'individus pour avoir une meilleur vision de la generation , attetion temps de calcule important pour  la genereration
    map = Map(None,population=pop,generationX=100,generationY=100)
    map.generation_pers((49,50,50),d,nbIndividus) # generation de la population
    print("fin generation")
    map.creer_L_population()# creation de la liste 
    visualiser_surface_3d(map)