from PySide6.QtGui import QColor

def generate_unique_colors(int1, int2):
        # Utilisation des entiers pour calculer les composantes RGB
        r =  int(int1) % 256
        g =  int(int2) % 256
        b = int(int1 * int2) % 256
        return QColor(r, g, b)

def normalise_button( nom,prenom,liste):
        x,y=liste[1],liste[2]
        return(nom+" "+prenom,generate_unique_colors(x,y),0,(x,y))

def normalise_button_C( nom,prenom,liste):
        charisme,x,y = liste[0],liste[1],liste[2]
        return (nom,prenom,charisme,x,y)
def normalise_Ind(ind,score):#prend un individus et score en parametre et renvois un element normaliser,c'est a dire compatible avec le front
        return (ind.nom()+" "+ind.prenom(),generate_unique_colors(ind.x(),ind.y()),score,(ind.x(),ind.y()))
def normalise_rechargement(liste):
        tmp=[]
        for i in range(len(liste)):
                tmp.append(normalise_Ind(liste[i],0))
        return tmp
                
def normalise_Ind_Mult(l):
        tmp=[]
        for i in range(len(l)):
                tmp.append(normalise_Ind(l[i],i+1))
        return tmp