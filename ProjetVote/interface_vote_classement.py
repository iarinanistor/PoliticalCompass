### Importation des bibliotheques
from tkinter import *
from tkinter import messagebox
from tkinter import ttk  # Import du module Treeview

#from matplotlib import *
from random import randint

import bib_objet
import votes


### Fenetre principale

# Creation de la fenetre principale
fenetre = Tk()
fenetre.title("Vote")
fenetre.geometry("800x800")
fenetre.minsize(1100, 800)
fenetre.maxsize(1200, 900)


# Fonction de centrage d'une fenetre
def centrage_fenetre(window):
    window.update_idletasks()   # Force la mise à jour des taches en cours
    width = window.winfo_width()    # Recuperation de la largeur de la fenetre
    height = window.winfo_height()  # Recuperation de la hauteur de la fenetre

    # Calcul pour centrer la fenetre par rapport aux dimensions de l'ecran
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')
    #window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


# Creation d'un frame pour contenir le tableau
frame_tab = Frame(fenetre)
frame_tab.pack(padx=10, pady=30)


# Utilisation de Treeview pour faire un tableau
tree = ttk.Treeview(frame_tab, columns=("Nom", "x", "y"))
tree.heading("#0", text="Id")
tree.heading("Nom", text="Nom")
tree.heading("x", text="x")
tree.heading("y", text="y")
tree.pack(side=LEFT)

# Ajout d'une scrollbar au tableau
scrollbar = ttk.Scrollbar(frame_tab, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)


### Definition des differentes variables globales necessaires

#Variables globales de type list qui contiennent les differents candidats
liste_candidats = []
liste_couleurs = []
liste_coordonnees = []

#Variable globale de type list qui contient la liste des candidats classés selon une méthode de vote
classement = []


###

# Creation du bouton d'ajout d'un nouveau candidat
def ajout_candidat():
    #Creation d'une fenetre pop-up
    fenetre_ajout = Toplevel(fenetre)
    fenetre_ajout.title("Ajout d'un candidat")
    fenetre_ajout.geometry("200x250")
    fenetre_ajout.resizable(width=False, height=False)

    label_ajout = Label(fenetre_ajout, text="Nom du candidat :")
    label_ajout.pack()

    # Ajout d'une zone texte ou l'utilisateur peut entrer le nom du candidat
    entry = Entry(fenetre_ajout)
    entry.pack(pady= 5)

    label_ajout_x = Label(fenetre_ajout, text="x :")
    label_ajout_x.pack()
    entry_cand_x = Entry(fenetre_ajout)
    entry_cand_x.pack(pady= 5)

    label_ajout_y = Label(fenetre_ajout, text="y :")
    label_ajout_y.pack()
    entry_cand_y = Entry(fenetre_ajout)
    entry_cand_y.pack(pady= 5)


    # Message de retour à l'appui du bouton "Valider"
    def callback():
        nom = entry.get()
        x = entry_cand_x.get()
        y = entry_cand_y.get()
        messagebox.showinfo("Ajout d'un candidat","Candidat(e) ajouté(e) avec succès")
        fenetre_ajout.destroy() # Fermeture de la fenetre

        #x = randint(0,500)
        #y = randint(0,500)

        # Ajout du nom du candidat au tableau
        tree.insert("", "end", text=len(tree.get_children()) + 1, values=(nom, x, y))

        cand = bib_objet.Candidat(nom=nom, prenom="Test", charisme=randint(0,10), age=randint(1,100), x=int(x), y=int(y))

        global liste_candidats
        liste_candidats.append(cand)

        liste_coordonnees.append((int(x), int(y)))
        color = "#{:06x}".format(randint(0, 0xFFFFFF)) # Couleur aleatoire attribuee a chaque candidat
        liste_couleurs.append(color)


    bouton_fin = Button(fenetre_ajout, text="Valider", command=callback)
    bouton_fin.pack()

    centrage_fenetre(fenetre_ajout)



bouton_new = Button(fenetre, text="Nouveau candidat", command=ajout_candidat)
bouton_new.pack()


### Fenetre contenant la grille

def affichage_fenetre_grille():
    # Nouvelle fenetre contenant la grille "The Political Compass"

    fenetre_grille = Tk()
    fenetre_grille.title("The Political Compass")
    fenetre_grille.geometry("1600x1000")
    fenetre_grille.minsize(800, 800)
    fenetre_grille.maxsize(1920, 1080)


    # Creation d'un canvas contenant la grille
    frame_canvas = Frame(fenetre_grille)
    frame_canvas.pack() #padx=(20, 0), pady=(0, 200))

    global canvas
    canvas = Canvas(frame_canvas, width=500, height=500, bg="white")
    canvas.pack(side=TOP)

    # Tracage du quadrillage de la grille
    for i in range(0, 500, 10):
        if (i != 250):
            canvas.create_line(0, i, 500, i, width=1, fill="light gray")
            canvas.create_line(i, 0, i, 500, width=1, fill="light gray")

    # Tracage des lignes centrales
    canvas.create_line(0, 250, 500, 250, width=1, fill="black")
    canvas.create_line(250, 0, 250, 500, width=1, fill="black")

    canvas.pack(padx=10, pady=30)

    # Creation de la legende
    frame_legende = Frame(fenetre_grille)
    frame_legende.pack(side=RIGHT, padx=(0, 100), pady=(0, 100))

    label_legende = Label(frame_legende, text="Legende :")
    label_legende.pack(side=TOP, padx=(0, 30), pady=(0, 10))

    # Liste des candidats
    listbox_candidats = Listbox(frame_legende, height=20)
    listbox_candidats.pack(side=LEFT)

    for i in range(len(liste_candidats)):
        coord_x, coord_y = liste_coordonnees[i]
        canvas.create_oval(coord_x-5, coord_y-5, coord_x+5, coord_y+5, fill=liste_couleurs[i])
        listbox_candidats.insert(END, liste_couleurs[i], liste_candidats[i].nom())

    # Ajout d'une scrollbar a la legende
    scrollbar_liste = ttk.Scrollbar(frame_legende, orient=VERTICAL, command=listbox_candidats.yview)
    listbox_candidats.configure(yscrollcommand=scrollbar_liste.set)
    scrollbar_liste.pack(side=RIGHT, fill=Y)


    # Fonction permettant de placer un nouveau point sur la grille
    def placer_point():
        fenetre_point = Toplevel(fenetre_grille)
        fenetre_point.title("Nouveau point")
        fenetre_point.geometry("300x300")
        fenetre_point.resizable(width=False, height=False)


        for i in range(2):
            fenetre_grille.columnconfigure(i, weight=1, minsize=75)
            fenetre_grille.rowconfigure(i, weight=1, minsize=50)

        frame_x = Frame(fenetre_point, relief=RAISED, borderwidth=1)
        frame_x.grid(row=0, column=0)
        label_x = Label(frame_x, text="x :")
        label_x.pack(padx=2, pady=2)

        frame_ent_x = Frame(fenetre_point, relief=RAISED, borderwidth=1)
        frame_ent_x.grid(row=0, column=1)
        entry_x = Entry(frame_x)
        entry_x.pack()

        frame_y = Frame(fenetre_point, relief=RAISED, borderwidth=1)
        frame_y.grid(row=1, column=0)
        label_y = Label(frame_x, text="y :")
        label_y.pack(padx=2, pady=2)

        frame_ent_y = Frame(fenetre_point, relief=RAISED, borderwidth=1)
        frame_ent_y.grid(row=1, column=1)
        entry_y = Entry(frame_y)
        entry_y.pack()


        # Message de retour à l'appui du bouton "Valider"
        def callback_point():
            x = int(entry_x.get())
            y = int(entry_y.get())
            messagebox.showinfo("Ajout d'un Point","Point ajouté avec succès")

            fenetre_point.destroy() # Fermeture de la fenetre

            # Couleur aléatoire
            color = "#{:06x}".format(randint(0, 0xFFFFFF))

            canvas.create_oval(x-5, y-5, x+5, y+5, fill=color)


        bouton_fin_point = Button(fenetre_point, text="Valider", command=callback_point)
        bouton_fin_point.place(x=115, y=200)


    bouton_point = Button(frame_canvas, text="Nouveau point", command=placer_point)
    bouton_point.pack(side=BOTTOM)

    centrage_fenetre(fenetre_grille)

    fenetre_grille.mainloop()


### Suite de la fenetre principale

bouton_suivant = Button(fenetre, text="Affichage de la grille", command=affichage_fenetre_grille)
bouton_suivant.pack(side=BOTTOM, pady=20)


# Fonction de generation pour la methode de Condorcet
def generation_condorcet():
    fenetre_generation = Toplevel(fenetre)
    fenetre_generation.title("Méthode de Condorcet")
    fenetre_generation.geometry("800x800")
    fenetre_generation.resizable(width=False, height=False)

    # Liste des candidats classés selon la methode de Condorcet
    listbox_classement = Listbox(fenetre_generation)
    listbox_classement.pack(pady=50)


    def calcul_classement_condorcet():
        global classement

        m = bib_objet.Map(liste_electeur=liste_candidats, generationX=500, generationY=500)
        m.generationAleatoire()

        classement = m.condorcet()

        for i in range(len(classement)):
            listbox_classement.insert(END, str(i+1), classement[i].nom())


    bouton_liste = Button(fenetre_generation, text="Classement", command=calcul_classement_condorcet)
    bouton_liste.pack()


# Fonction de generation pour la methode de la pluralite
def generation_pluralite():
    fenetre_generation = Toplevel(fenetre)
    fenetre_generation.title("Méthode de la Pluralité")
    fenetre_generation.geometry("800x800")
    fenetre_generation.resizable(width=False, height=False)

    # Liste des candidats classés selon la methode de la pluralite
    listbox_classement = Listbox(fenetre_generation)
    listbox_classement.pack(pady=50)


    def calcul_classement_pluralite():
        global classement

        m = bib_objet.Map(liste_electeur=liste_candidats, generationX=500, generationY=500)
        m.generationAleatoire()

        classement = m.Pluralite()

        for i in range(len(classement)):
            listbox_classement.insert(END, str(i+1), classement[i])


    bouton_liste = Button(fenetre_generation, text="Classement", command=calcul_classement_pluralite)
    bouton_liste.pack()


# Fonction de generation pour la methode de Borda
def generation_borda():
    fenetre_generation = Toplevel(fenetre)
    fenetre_generation.title("Méthode de Borda")
    fenetre_generation.geometry("800x800")
    fenetre_generation.resizable(width=False, height=False)

    # Liste des candidats classés selon la methode de Borda
    listbox_classement = Listbox(fenetre_generation)
    listbox_classement.pack(pady=50)


    def calcul_classement_borda():
        global classement

        m = bib_objet.Map(liste_electeur=liste_candidats, generationX=500, generationY=500)
        m.generationAleatoire()

        classement = m.Borda()

        for i in range(len(classement)):
            listbox_classement.insert(END, str(i+1), classement[i])


    bouton_liste = Button(fenetre_generation, text="Classement", command=calcul_classement_borda)
    bouton_liste.pack()


# Fonction de generation pour la methode de STV
def generation_stv():
    fenetre_generation = Toplevel(fenetre)
    fenetre_generation.title("Méthode de STV")
    fenetre_generation.geometry("800x800")
    fenetre_generation.resizable(width=False, height=False)

    # Liste des candidats classés selon la methode de STV
    listbox_classement = Listbox(fenetre_generation)
    listbox_classement.pack(pady=50)


    def calcul_classement_STV():
        global classement

        m = bib_objet.Map(liste_electeur=liste_candidats, generationX=500, generationY=500)
        m.generationAleatoire()

        classement = m.STV()

        for i in range(len(classement)):
            listbox_classement.insert(END, str(i+1), classement[i])


    bouton_liste = Button(fenetre_generation, text="Classement", command=calcul_classement_STV)
    bouton_liste.pack()


# Fonction de generation pour la methode de l'approbation
def generation_approbation():
    fenetre_generation = Toplevel(fenetre)
    fenetre_generation.title("Méthode de l'approbation'")
    fenetre_generation.geometry("800x800")
    fenetre_generation.resizable(width=False, height=False)

    # Liste des candidats classés selon la methode de STV
    listbox_classement = Listbox(fenetre_generation)
    listbox_classement.pack(pady=50)


    def calcul_classement_approbation():
        global classement

        m = bib_objet.Map(liste_electeur=liste_candidats, generationX=500, generationY=500)
        m.generationAleatoire()

        classement = m.Approbation()

        for i in range(len(classement)):
            listbox_classement.insert(END, str(i+1), classement[i])


    bouton_liste = Button(fenetre_generation, text="Classement", command=calcul_classement_approbation)
    bouton_liste.pack()


label = Label(fenetre, text="Différents systèmes de vote :", height=2, font=30)
label.pack(pady=(30, 0))


frame_methodes_vote = Frame(fenetre, relief=SUNKEN)
frame_methodes_vote.pack()

frame_methodes_vote2 = Frame(fenetre, relief=SUNKEN)
frame_methodes_vote2.pack()


bouton_suivant = Button(frame_methodes_vote, text="Affichage Classement Condorcet", command=generation_condorcet)
bouton_suivant.pack(side=LEFT, padx=20, pady=20)


bouton_suivant = Button(frame_methodes_vote2, text="Affichage Classement Pluralité", command=generation_pluralite)
bouton_suivant.pack(side=LEFT, padx=20,  pady=20)


bouton_suivant = Button(frame_methodes_vote, text="Affichage Classement Borda") #, command=generation_borda)
bouton_suivant.pack(side=RIGHT, padx=20, pady=20)


bouton_suivant = Button(frame_methodes_vote2, text="Affichage Classement Stv") #, command=generation_stv)
bouton_suivant.pack(side=LEFT, padx=20,  pady=20)


bouton_suivant = Button(frame_methodes_vote2, text="Affichage Classement Approbation") #, command=generation_approbation)
bouton_suivant.pack(side=RIGHT, padx=20,  pady=20)


centrage_fenetre(fenetre)

fenetre.mainloop()

