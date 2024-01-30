import tkinter as tk
from Candidat import *
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

figure = Figure(figsize=(10, 10), dpi=100)
ax = figure.add_subplot(111)
ax.axhline(y=50,color='red')
ax.axvline(x=50,color='red')
ax.set_xlim([0,100])
ax.set_ylim([0,100])
candidats = generate_candidats(10)

def plot():
    xp = np.array([candidat.x() for candidat in candidats])
    yp = np.array([candidat.y() for candidat in candidats])
    ax.scatter(xp, yp)
    canvas.draw()






root = tk.Tk()
canvas = FigureCanvasTkAgg(figure, root)
canvas.draw()
canvas.get_tk_widget().pack(pady=10)
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack()
button = tk.Button(root, text="Graph It", command=plot)
button.pack()
root.mainloop()