# jc2iy


Methodes de votes et leurs consequences.

On crée un Political Compass avec des électeurs et des candidats. Chaque votant a une liste ordonnée des candidats (préférés au moins préférés), et on teste les différentes méthodes de vote pour voir leurs influences sur le résultat final. On implémente une méthode de Monte-Carlo en fonction des différents types de vote, et des cartes prédéfinies (par exemple une carte représentant la France en fonction des statistiques des différentes élections, etc).

Mini-sprint : Démocratie Liquide

On a créé une fonction délégation qui choisit à qui déléguer en utilisant l'algorithme fournit, dans cette fonction on a calculer les probabilités normalisées (on divise le niveau de compétence de l'electeur par la somme du niveau de compétence de tous les électeurs éligibles à recevoir le vote) et on a utilisé les probabilités cumulatives pour faire le choix.
On a créé une fonction Zone qui calcule la liste des electeurs qui n'ont pas délégué dans la zone d'un individu et on a créé une fonction qui met à jours les poids des electeurs.
Enfin on a mis à jour les fonctions de votes pour prendre en compte les poids d'importance.
Notre fonction STV ne fonctionne pas sur l'interface graphique mais elle fonctionne sur les tests (on est toujours entrain de résoudre ce problème)


----------------------------------------------------------------------------------------------------

Comment utiliser l'interface :


Exécuter le fichier main.py

Pour ajouter manuellement un nouveau candidat à la grille :
 - Dans le champ Nom, vous pouvez entrer une chaîne de caractères
 - Dans le champ Prénom, vous pouvez entrer une chaîne de caractères
 - Dans le champ Charisme, vous pouvez choisir le charisme du candidat entre 0 et 100
 - Dans les champs x et y, vous pouvez choisir une position entre 0 et 500

 - Appuyez sur Soumettre pour valider les informations
   (un récapitulatif sera affiché dans la console sous la forme :
    Nom : <nom_du_candidat>
    Prénom : <prénom_du_candidat>
    Valeurs entières: [<charisme>, <x>, <y>])

Le bouton "Genere un Candidat" permet de générer un nouveau candidat aléatoirement.

Le bouton "Copeland" permet de déterminer le vainqueur selon la méthode de Copeland.

Le bouton "Borda" permet de déterminer le vainqueur selon la méthode de Borda.

Le bouton "Pluralite" permet de déterminer le vainqueur selon la méthode de Pluralité.

Le bouton "STV" permet de déterminer le vainqueur selon la méthode de STV.

Le bouton "Approbation" permet de déterminer le vainqueur selon la méthode de l'Approbation.


Pour sauvegarder le modèle :
 - Entrer le nom du fichier dans le champ au dessus du bouton "save"
 - Appuyer sur le bouton "save" pour sauvegarder le modèle dans le fichier

Pour charger un modèle :
 - Entrer le nom du fichier dans le champ au dessus du bouton "recharge"
 - Appuyer sur le bouton "recharge" pour charger le modèle


----------------------------------------------------------------------------------------------------


Credits:

Zhou Jeremy

Khamis Yara

Nistor Iarina

Kinane-Daouadji Isaac (scrum master)

Benhaddou Chady





