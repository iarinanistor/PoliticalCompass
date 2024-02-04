import bib_objet as ob
import Condorsait as Cond
n=2
#======================================
# POO :
l=["MOI","PAS TOI","UN AUTRE","BERNARD","MICHELLE"]
liste_electeur=[ ob.Individus(l[i],i,i)for i in range(len(l))]
ind = ob.Individus("joeur de lol",5,5,liste_electeur)
l=["a", "b", "c", "d"]
electeur=[ob.Individus("victor",-10,10),ob.Individus("Isaac",0,0),ob.Individus("Lyna",-5,-25),ob.Individus("chaby",-30,-30)]
population=[[ob.Individus("1",10,10,electeur),ob.Individus("2",0,0,electeur)],[ob.Individus("3",-5,-5,electeur),ob.Individus("quatre",-10,-10,electeur)]]
map=ob.Map("France",electeur,population)
assert( ind.liste_vote() == ['MICHELLE', 'BERNARD', 'UN AUTRE', 'PAS TOI', 'MOI'])
assert( map.liste_electeur[3].nom == "chaby")
assert(map.population[1][1].liste_vote() == ['Isaac', 'Lyna', 'victor', 'chaby'])
assert(map.listes_listes_votes() == [['Isaac', 'victor', 'Lyna', 'chaby'], ['Isaac', 'victor', 'Lyna', 'chaby'], ['Isaac', 'victor', 'Lyna', 'chaby'], ['Isaac', 'Lyna', 'victor', 'chaby']])
#print(map.condorsait())
print("Test POO : OK ","( 1 /",n,")")

#======================================
# Condorsait :

assert(Cond.genre_combat(['a','b','c','d'],[]) == [('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('b', 'd'), ('c', 'd')])
assert(Cond.combat([['a','b','d','c'],['d','b','c','a'],['c','a','b','d']],('c','b')) == -1) 
assert(Cond.combat([['a','b','d','c'],['d','b','c','a'],['c','a','b','d']],('a','c')) == -1) 
assert(Cond.all_combat([['a','b','d','c'],['d','b','c','a'],['c','a','b','d']]) == {'b': 2, 'a': 2, 'd': 1, 'c': 1})
print("Test Condorsait OK ","( 2 /",n,")")

#=======================================
#Fin des tests
# pytest a fair 
print("Fin des tests","\nOK")