import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import bib_objet as ob
import votes as v

class Chessboard(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Chess')
        self.move_data = {'x': 0, 'y': 0, 'piece': None, 'to': None, 'from': None, 'last': None, 'color': 'w', 'enem_color': 'b'}
        self.create_widgets()

    def plot_map(self, fig):
        ax = fig.add_subplot(111)
        ax.axhline(y=50,color='red')
        ax.axvline(x=50,color='red')
        ax.set_xlim([0,100])
        ax.set_ylim([0,100])
        return ax

    def plot_votants(self, ax, map):
        votants = ob.concat(map.population)
        xv = np.array([votant.x for votant in votants])
        yv = np.array([votant.y for votant in votants])
        ax.scatter(xv, yv,c='powderblue',label='Votants')

    def plot_candidats(self, ax, map):
        l_candidats = map.liste_electeur
        xp = np.array([candidat.x() for candidat in l_candidats])
        yp = np.array([candidat.y() for candidat in l_candidats])
        annotations = [candidat.nom()+" "+candidat.prenom()+" "+str(candidat.age()) for candidat in l_candidats]
        ax.scatter(xp, yp,c='red',s=200,label='Candidats')
        for i, label in enumerate(annotations):
            ax.text(xp[i]-0.6, yp[i]+0.3,label, rotation = -45,
            bbox=dict(boxstyle="sawtooth,pad=0.3", alpha = 0.3))

    def show_winner(self, method, map):
        winner = method(map.liste_electeur,ob.concat(map.population))
        winner_name = winner.nom() + " " + winner.prenom()
        self.announcement_label.config(text=f"The winner according to {method.__name__} method is: ", fg='black')
        self.winner_label.config(text="\n" + winner_name, fg='red', font=("Helvetica", 16, "bold"), justify='center')

    def create_widgets(self):
        # Plot Frame (Northwest)
        self.plot_frame = tk.Frame(self, borderwidth=20)
        self.plot_frame.grid(row=0, column=0, sticky='nsew')

        # Create the plot figure
        map = ob.Map('France',[],[],100,100)
        map.liste_electeur = ob.Candidat.generate_candidats(5,100,100)
        map.generationAleatoire()
        
        self.figure = Figure(figsize=(8, 8), dpi=100)  # Adjust the figsize here
        self.ax = self.plot_map(self.figure)
        self.plot_votants(self.ax,map)
        self.plot_candidats(self.ax,map)

        # Add canvas to display the plot
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Button Frame (Northeast)
        self.button_frame = tk.Frame(self, borderwidth=20)
        self.button_frame.grid(row=0, column=1, sticky='nsew')

        # Add buttons
        button1 = tk.Button(self.button_frame, text="Plurality", command=lambda: self.show_winner(v.pluralite, map))
        button1.pack(side='top')
        button2 = tk.Button(self.button_frame, text="Another Method", command=lambda: self.show_winner(another_method, map))
        button2.pack(side='top')  # Replace another_method with the actual method you want to use

        # Announcement Frame (Southwest)
        self.announcement_frame = tk.Frame(self, borderwidth=20)
        self.announcement_frame.grid(row=1, column=0, sticky='nsew')

        # Add widgets for announcement
        self.announcement_label = tk.Label(self.announcement_frame, text="", fg='black')
        self.announcement_label.pack(side='left')

        self.winner_label = tk.Label(self.announcement_frame, text="", fg='red', font=("Helvetica", 16, "bold"), justify='center')
        self.winner_label.pack(side='left')

        # Input Frame (Southeast)
        self.input_frame = tk.Frame(self, borderwidth=20)
        self.input_frame.grid(row=1, column=1, sticky='nsew')

        # Add widgets for manual input
        x_label = tk.Label(self.input_frame, text="X:")
        x_label.grid(row=0, column=0)
        self.x_entry = tk.Entry(self.input_frame)
        self.x_entry.grid(row=0, column=1)

        y_label = tk.Label(self.input_frame, text="Y:")
        y_label.grid(row=1, column=0)
        self.y_entry = tk.Entry(self.input_frame)
        self.y_entry.grid(row=1, column=1)

        nom_label = tk.Label(self.input_frame, text="NOM:")
        nom_label.grid(row=2, column=0)
        self.nom_entry = tk.Entry(self.input_frame)
        self.nom_entry.grid(row=2, column=1)

        prenom_label = tk.Label(self.input_frame, text="PRENOM:")
        prenom_label.grid(row=3, column=0)
        self.prenom_entry = tk.Entry(self.input_frame)
        self.prenom_entry.grid(row=3, column=1)

        charisme_label = tk.Label(self.input_frame, text="CHARISME:")
        charisme_label.grid(row=4, column=0)
        self.charisme_entry = tk.Entry(self.input_frame)
        self.charisme_entry.grid(row=4, column=1)

        age_label = tk.Label(self.input_frame, text="AGE:")
        age_label.grid(row=5, column=0)
        self.age_entry = tk.Entry(self.input_frame)
        self.age_entry.grid(row=5, column=1)

        # Add button to place point
        place_point_button = tk.Button(self.input_frame, text="Place New Candidate", command=lambda: self.place_candidat(map))
        place_point_button.grid(row=6, columnspan=2)

        # Configure grid weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

    def place_candidat(self,map):
        # Retrieve X and Y coordinates from entry fields
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            nom = str(self.nom_entry.get())
            prenom = str(self.prenom_entry.get())
            charisme = float(self.charisme_entry.get())
            age = float(self.age_entry.get())
        except ValueError:
            # Handle invalid input
            tk.messagebox.showerror("Error", "Invalid input for coordinates")
            return

        # Add point to scatter plot
        label = nom+" "+prenom+" "+str(int(age))
        self.ax.scatter(x, y,c='red',s=200)
        self.ax.text(x-0.6, y+0.3,label, rotation = -45, bbox=dict(boxstyle="rarrow,pad=0.3", alpha = 0.3))
        map.ajoutCandidat(nom,prenom,charisme,age,x,y)
        self.canvas.draw()

# Create the main window
Chessboard().mainloop()
