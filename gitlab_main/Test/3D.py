import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Génération de coordonnées aléatoires pour les points
num_points = 1000  # Nombre de points à générer aléatoirement
x = np.random.randint(0, 250, num_points)
y = np.random.randint(0, 250, num_points)
z = np.random.randint(0, 30, num_points)

# Création de la figure et de l'axe 3D pour la visualisation
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Utilisation de plot_trisurf pour créer une surface à partir des points aléatoires
ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')

# Personnalisation du graphique
ax.set_xlabel('Axe X')
ax.set_ylabel('Axe Y')
ax.set_zlabel('Axe Z')
plt.title('Surface interpolée à partir de points aléatoires')

# Affichage du graphique
plt.show()
