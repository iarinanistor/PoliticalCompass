### Importation des bibliotheques
from tkinter import *
from tkinter import messagebox
from tkinter import ttk  # Import du module Treeview

from matplotlib import *
from random import randint

### Fenetre principale

# Creation de la fenetre principale
fenetre = Tk()
fenetre.title("Vote")
fenetre.geometry("800x800")
fenetre.minsize(1100, 800)
fenetre.maxsize(1200, 900)

label = Label(fenetre, text="Différents systèmes de vote", height=2, font=30)
#label.pack(side=TOP)

# Fonction de centrage d'une fenetre
"""def centrage_fenetre(window):
    eval_ = window.nametowidget('.').eval
    eval_('tk::PlaceWindow %s center' % window)"""

def centrage_fenetre(window):
    window.update_idletasks()   # Force la mise à jour des taches en cours
    width = window.winfo_width()    # Recuperation de la largeur de la fenetre
    height = window.winfo_height()  # Recuperation de la hauteur de la fenetre

    # Calcul pour centrer la fenetre par rapport aux dimensions de l'ecran
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')
    #window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


# Creation d'un canvas
#monCanvas = Canvas(fenetre, width=500, height=500, bg="ivory")
#monCanvas.place(x=150, y=150)


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

# Ajout d'une scrollbar
scrollbar = ttk.Scrollbar(frame_tab, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)


### Definition des differentes variables globales necessaires

# Variable global "nom" pour pouvoir recuperer l'entree de l'utilisateur
nom = ""

# Definition global de entry_x et entry_y
x = 0
y = 0

canvas = None

liste_candidats = []
liste_couleurs = []
liste_coordonnees = []

###

# Creation d'une etiquette pour pouvoir ecrire le nom du candidat
nom_label = Label(fenetre, text=nom)
nom_label.place(x=100, y=100)


# Creation du bouton d'ajout d'un nouveau candidat
def ajout_candidat():
    #Creation d'une fenetre pop-up
    fenetre_ajout = Toplevel(fenetre)
    fenetre_ajout.title("Ajout d'un candidat")
    fenetre_ajout.geometry("200x100")
    fenetre_ajout.resizable(width=False, height=False)

    label_ajout = Label(fenetre_ajout, text="Nom du candidat :")
    label_ajout.pack()

    # Ajout d'une zone texte ou l'utilisateur peut entrer le nom du candidat
    entry = Entry(fenetre_ajout)
    entry.pack(pady= 5)


    # Message de retour à l'appui du bouton "Valider"
    def callback():
        global nom # Recuperation de la variable global nom
        nom = entry.get()
        messagebox.showinfo("Ajout d'un candidat","Candidat(e) ajouté(e) avec succès")
        fenetre_ajout.destroy() # Fermeture de la fenetre

        x = randint(0,500)
        y = randint(0,500)

        # Ajout du nom du candidat au tableau
        tree.insert("", "end", text=len(tree.get_children()) + 1, values=(nom, x, y))

        global liste_candidats
        liste_candidats.append(nom)
        liste_coordonnees.append((x,y))
        color = "#{:06x}".format(randint(0, 0xFFFFFF)) # Couleur aleatoire attribuee a chaque candidat
        liste_couleurs.append(color)

        #nom_label.config(text=nom)

        # Ajout du nom du candidat dans la grille
        #add_candidate_to_grid(nom)


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
    fenetre_grille.geometry("800x800")
    fenetre_grille.minsize(800, 800)
    fenetre_grille.maxsize(1000, 1000)

    # Creation d'un canvas
    frame_canvas = Frame(fenetre_grille)
    frame_canvas.pack(side=LEFT, padx=(20, 0), pady=(0, 200))

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
    color_frame = Frame(fenetre_grille)
    color_frame.pack(side=RIGHT, padx=(0, 50), pady=(0, 500))

    color_label = Label(color_frame, text="Legende :")
    color_label.pack(side=TOP, padx=30)

    # Liste des candidats
    listbox_candidats = Listbox(color_frame)
    listbox_candidats.pack(side=BOTTOM, pady=(10, 0))

    for i in range(len(liste_candidats)):
        coord_x, coord_y = liste_coordonnees[i]
        canvas.create_oval(coord_x-5, coord_y-5, coord_x+5, coord_y+5, fill=liste_couleurs[i])
        listbox_candidats.insert(END, liste_couleurs[i], liste_candidats[i])


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
            global x # Recuperation de la variable global x
            global y # Recuperation de la variable global y

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


bouton_suivant = Button(fenetre, text="Affichage de la grille", command=affichage_fenetre_grille)
bouton_suivant.pack(side=BOTTOM, pady=20)

centrage_fenetre(fenetre)

fenetre.mainloop()


### Tests et utilitaires

# Creation d'une grille qui s'adapte a la taille de la fenetre
"""for i in range(10):
    fenetre_grille.columnconfigure(i, weight=1, minsize=75)
    fenetre_grille.rowconfigure(i, weight=1, minsize=50)

    for j in range(10):
        frame = Frame(fenetre_grille, relief=RAISED, borderwidth=1)
        frame.grid(row=i, column=j, padx=5, pady=5)
        label = Label(frame, text=f"Row {i}\nColumn {j}")
        label.pack(padx=2, pady=2)"""
