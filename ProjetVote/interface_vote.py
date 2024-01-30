from tkinter import *
from tkinter import messagebox
from tkinter import ttk  # Import du module Treeview

from matplotlib import *

# Creation de la fenetre principale
fenetre = Tk()
fenetre.title("Vote")
fenetre.geometry("800x800")
fenetre.minsize(500, 500)
fenetre.maxsize(900, 900)

label = Label(fenetre, text="Différents systèmes de vote", height=2, font=30)
#label.pack(side=TOP)

# Fonction de centrage d'une fenetre
def centrage_fenetre(window):
    eval_ = window.nametowidget('.').eval
    eval_('tk::PlaceWindow %s center' % window)


# Creation d'un canvas
#monCanvas = Canvas(fenetre, width=500, height=500, bg="ivory")
#monCanvas.place(x=150, y=150)


# Utilisation de Treeview pour faire un tableau
tree = ttk.Treeview(fenetre, columns=("Nom"))
tree.heading("#0", text="ID")
tree.heading("Nom", text="Nom")
tree.pack(padx=10, pady=10)

# Ajout d'une scrollbar
scrollbar = ttk.Scrollbar(fenetre, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack()


# Variable global "nom" pour pouvoir recuperer l'entree de l'utilisateur
nom = ""

# Definition global de entry_x et entry_y
x = 0
y = 0

canvas = None

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
    entry.place(x=18, y=20)


    # Message de retour à l'appui du bouton "Valider"
    def callback():
        global nom # Recuperation de la variable global nom
        nom = entry.get()
        messagebox.showinfo("Ajout d'un candidat","Candidat(e) ajouté(e) avec succès")
        fenetre_ajout.destroy() # Fermeture de la fenetre

        # Ajout du nom du candidat au tableau
        tree.insert("", "end", text=len(tree.get_children()) + 1, values=(nom))


        #nom_label.config(text=nom)

        # Ajout du nom du candidat dans la grille
        #add_candidate_to_grid(nom)


    bouton_fin = Button(fenetre_ajout, text="Valider", command=callback)
    bouton_fin.place(x=60, y=50)

    centrage_fenetre(fenetre_ajout)



bouton_new = Button(fenetre, text="Nouveau candidat", command=ajout_candidat)
bouton_new.place(x=20, y=70)


def affichage_fenetre_grille():
    # Nouvelle fenetre contenant la grille "The Political Compass"

    fenetre_grille = Tk()
    fenetre_grille.title("The Political Compass")
    fenetre_grille.geometry("800x800")
    fenetre_grille.minsize(500, 500)
    fenetre_grille.maxsize(900, 900)

    # Creation d'un canvas
    canvas = Canvas(fenetre_grille, width=500, height=500, bg="white")

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
    color_frame.pack(side=RIGHT)

    color_label = Label(color_frame, text="Legende")
    color_label.pack()


    # Fonction permettant de placer un nouveau point sur la grille
    def placer_point(canvas):
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

            canvas.create_oval(x-5, y-5, x+5, y+5)


        bouton_fin_point = Button(fenetre_point, text="Valider", command=callback_point())
        bouton_fin_point.place(x=115, y=200)


    bouton_point = Button(fenetre_grille, text="Nouveau point", command=placer_point(canvas))
    bouton_point.pack()


    fenetre_grille.mainloop()


    # Creation d'une grille qui s'adapte a la taille de la fenetre
    """for i in range(10):
        fenetre_grille.columnconfigure(i, weight=1, minsize=75)
        fenetre_grille.rowconfigure(i, weight=1, minsize=50)

        for j in range(10):
            frame = Frame(fenetre_grille, relief=RAISED, borderwidth=1)
            frame.grid(row=i, column=j, padx=5, pady=5)
            label = Label(frame, text=f"Row {i}\nColumn {j}")
            label.pack(padx=2, pady=2)"""


bouton_suivant = Button(fenetre, text="Affichage de la grille", command=affichage_fenetre_grille)
bouton_suivant.pack(side=BOTTOM)

centrage_fenetre(fenetre)

fenetre.mainloop()