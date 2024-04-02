import csv

## Fonctions de calcul des emissions carbone

#Fonction qui somme toutes les emissions d'un fichier csv à partir de debut jusqu'a fin (optionnel)
def emission_totale(csv_file, debut=0, fin=None):
    '''
        Fonction qui prend un fichier csv et retourne le nom de la fonction mesuree, l'emission totale de tous les appels et la moyenne d'un appel

        Parameters:
            csv_file (str): Nom du fichier 
            debut (int): Numero de la premiere ligne a lire (par defaut : 0 qui equivaut au debut du fichier)
            fin (int): Numero de la derniere ligne a lire (par defaut : None qui equivaut a la fin du fichier)

        Returns:
            nom_fonction, total_emission, moyenne (str, float, float): Tuple contenant le nom de la fonction mesuree, l'emission totale de tous les appels et l'emission moyenne d'un appel
    '''
    total_emissions = 0.0

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        num_ligne = 0
        nom_fonction = ""

        for colonne in reader:
            if num_ligne < debut:
                num_ligne += 1
                continue
            if (fin is not None) and (num_ligne > fin):
                break
            total_emissions += float(colonne['emissions'])
            num_ligne += 1
            if nom_fonction == "":
                nom_fonction = str(colonne['project_name'])

    moyenne = total_emissions/num_ligne
    return nom_fonction, total_emissions, moyenne


## Affichage des calculs

#Emission totale de Individus init
nom_fonction, total_emission_individus, moyenne_emission_individus = emission_totale('Resultats/emissions_carbone_individus.csv', debut=6, fin=5750)
print("Emission totale de ", nom_fonction, " : ", total_emission_individus)
print("Moyenne d'emission de ", nom_fonction, " : ", moyenne_emission_individus)
print("\n")

#Emission totale de Planete
nom_fonction, total_emission_planete, moyenne_emission_planete = emission_totale('Resultats/emissions_planete.csv', debut=12, fin=408)
print("Emission totale de ", nom_fonction, " : ", total_emission_planete)
print("Moyenne d'emission de ", nom_fonction, " : ", moyenne_emission_planete)
print("\n")

#Emission totale du lancement
nom_fonction, total_emission_lancement, moyenne_emission_lancement = emission_totale('Resultats/emissions_lancement.csv', debut=0, fin=None)
print("Emission totale du lancement : ", total_emission_lancement)
print("\n")

#Emission totale de l'ouverture du MenuLateral
nom_fonction, total_emission_ouverture_menu_lat, moyenne_emission_fermeture_menu_lat = emission_totale('Resultats/emissions_MenuLateral_ouverture.csv', debut=0, fin=None)
print("Emission totale de l'ouverture du MenuLateral : ", total_emission_ouverture_menu_lat)
print("Moyenne d'emission de l'ouverture du MenuLateral : ", total_emission_ouverture_menu_lat/10)
print("\n")

#Emission totale de la fermeture du MenuLateral
nom_fonction, total_emission_fermeture_menu_lat, moyenne_emission_fermeture_menu_lat = emission_totale('Resultats/emissions_MenuLateral_fermeture.csv', debut=0, fin=None)
print("Emission totale de la fermeture du MenuLateral : ", total_emission_fermeture_menu_lat)
print("Moyenne d'emission de la fermeture du MenuLateral : ", total_emission_fermeture_menu_lat/10)
print("\n")

#Emission totale de la soumission d'une candidat
nom_fonction, total_emission_soumission_candidat, moyenne_emissions_soumission_candidat = emission_totale('Resultats/emissions_soumission_candidat.csv', debut=0, fin=None)
print("Emission totale de la soumission : ", total_emission_soumission_candidat)
print("\n")

#Emission totale de la generation d'un candidat
nom_fonction, total_emission_generation_candidat, moyenne_emissions_soumission_candidat = emission_totale('Resultats/emissions_soumission_candidat.csv', debut=0, fin=None)
print("Emission totale de le generation : ", total_emission_generation_candidat)
print("\n")

#Emission totale de l'ouverture du MenuLateral
nom_fonction, total_emission_ouverture_menu_lat2, moyenne_emission_ouverture_menu_lat2 = emission_totale('Resultats/emissions_MenuLateral2_ouverture.csv', debut=0, fin=None)
print("Emission totale de l'ouverture du MenuLateral2 : ", total_emission_ouverture_menu_lat2)
print("Moyenne d'emission de l'ouverture du MenuLateral2 : ", total_emission_ouverture_menu_lat2/10)
print("\n")

#Emission totale de la fermeture du MenuLateral
nom_fonction, total_emission_fermeture_menu_lat2, moyenne_emission_fermeture_menu_lat2 = emission_totale('Resultats/emissions_MenuLateral2_fermeture.csv', debut=0, fin=None)
print("Emission totale de la fermeture du MenuLateral2 : ", total_emission_fermeture_menu_lat2)
print("Moyenne d'emission de la fermeture du MenuLateral2 : ", total_emission_fermeture_menu_lat2/10)
print("\n")

#Emission totale du bouton des règles de vote (ouverture)
nom_fonction, total_emission_ouverture_bouton_vote, moyenne_emission_ouverture_bouton_vote = emission_totale('Resultats/emissions_Bouton_vote_ouverture.csv', debut=0, fin=None)
print("Emission totale de l'ouverture avec le bouton Regle de vote : ", total_emission_ouverture_bouton_vote)
print("Moyenne d'emission de l'ouverture avec le bouton Regle de vote : ", total_emission_ouverture_bouton_vote/10)
print("\n")

#Emission totale du bouton des règles de vote (fermeture)
nom_fonction, total_emission_fermeture_bouton_vote, moyenne_emission_fermeture_bouton_vote = emission_totale('Resultats/emissions_Bouton_vote_fermeture.csv', debut=0, fin=None)
print("Emission totale de la fermeture avec le bouton Regle de vote : ", total_emission_fermeture_bouton_vote)
print("Moyenne d'emission de la fermeture avec le bouton Regle de vote : ", total_emission_fermeture_bouton_vote/10)
print("\n")

#Emission totale du bouton Democratie liquide (ouverture)
nom_fonction, total_emission_ouverture_democratie_liquide, moyenne_emission_ouverture_democratie_liquide = emission_totale('Resultats/emissions_Democratie_liquide_ouverture.csv', debut=0, fin=None)
print("Emission totale de la fermeture avec le bouton Regle de vote : ", total_emission_ouverture_democratie_liquide)
print("Moyenne d'emission de la fermeture avec le bouton Regle de vote : ", total_emission_ouverture_democratie_liquide/10)
print("\n")

#Emission totale du bouton Democratie liquide  (fermeture)
nom_fonction, total_emission_fermeture_democratie_liquide, moyenne_emission_fermeture_democratie_liquide = emission_totale('Resultats/emissions_Democratie_liquide_fermeture.csv', debut=0, fin=None)
print("Emission totale de l'ouverture avec le bouton Democratie liquide : ", total_emission_fermeture_democratie_liquide)
print("Moyenne d'emission de la fermeture avec le bouton Democratie liquide : ", total_emission_fermeture_democratie_liquide/10)
print("\n")

#Emission totale de Copeland liquide
nom_fonction, total_emission_copeland_liquide, moyenne_emission_copeland_liquide = emission_totale('Resultats/emissions_Copeland_liquide.csv', debut=0, fin=None)
print("Emission totale de Copeland liquide : ", total_emission_copeland_liquide)
print("Moyenne d'emission de Copeland liquide : ", total_emission_copeland_liquide/10)
print("\n")

#Emission totale de Borda liquide
nom_fonction, total_emission_borda_liquide, moyenne_emission_borda_liquide = emission_totale('Resultats/emissions_Borda_liquide.csv', debut=0, fin=None)
print("Emission totale de Borda liquide : ", total_emission_borda_liquide)
print("Moyenne d'emission de Borda liquide : ", total_emission_borda_liquide/5)
print("\n")

#Emission totale de Pluralite liquide
nom_fonction, total_emission_pluralite_liquide, moyenne_emission_pluralite_liquide = emission_totale('Resultats/emissions_Pluralite_liquide.csv', debut=0, fin=None)
print("Emission totale de Pluralite liquide : ", total_emission_pluralite_liquide)
print("Moyenne d'emission de Pluralite liquide : ", total_emission_pluralite_liquide/5)
print("\n")

#Emission totale de STV liquide
nom_fonction, total_emission_stv_liquide, moyenne_emission_stv_liquide = emission_totale('Resultats/emissions_STV_liquide.csv', debut=0, fin=None)
print("Emission totale de STV liquide : ", total_emission_stv_liquide)
print("Moyenne d'emission de STV liquide : ", total_emission_stv_liquide/5)
print("\n")

#Emission totale de Approbation liquide
nom_fonction, total_emission_approbation_liquide, moyenne_emission_approbation_liquide = emission_totale('Resultats/emissions_Approbation_liquide.csv', debut=0, fin=None)
print("Emission totale de Approbation liquide : ", total_emission_approbation_liquide)
print("Moyenne d'emission de Approbation liquide : ", total_emission_approbation_liquide/5)
print("\n")

#Emission totale de Copeland
nom_fonction, total_emission_copeland, moyenne_emission_copeland = emission_totale('Resultats/emissions_Copeland.csv', debut=0, fin=None)
print("Emission totale de Copeland : ", total_emission_copeland)
print("Moyenne d'emission de Copeland : ", total_emission_copeland/10)
print("\n")

#Emission totale de Borda
nom_fonction, total_emission_borda, moyenne_emission_borda = emission_totale('Resultats/emissions_Borda.csv', debut=0, fin=None)
print("Emission totale de Borda liquide : ", total_emission_borda)
print("Moyenne d'emission de Borda liquide : ", total_emission_borda/5)
print("\n")

#Emission totale de Pluralite
nom_fonction, total_emission_pluralite, moyenne_emission_pluralite = emission_totale('Resultats/emissions_Pluralite.csv', debut=0, fin=None)
print("Emission totale de Pluralite liquide : ", total_emission_pluralite)
print("Moyenne d'emission de Pluralite liquide : ", total_emission_pluralite/5)
print("\n")

#Emission totale de STV
nom_fonction, total_emission_stv, moyenne_emission_stv = emission_totale('Resultats/emissions_STV.csv', debut=0, fin=None)
print("Emission totale de STV liquide : ", total_emission_stv)
print("Moyenne d'emission de STV liquide : ", total_emission_stv/5)
print("\n")

#Emission totale de Approbation
nom_fonction, total_emission_approbation, moyenne_emission_approbation = emission_totale('Resultats/emissions_Approbation.csv', debut=0, fin=None)
print("Emission totale de Approbation liquide : ", total_emission_approbation)
print("Moyenne d'emission de Approbation liquide : ", total_emission_approbation/5)
print("\n")

## Variables contenant les moyennes

emission_moyen_individus = moyenne_emission_individus
emission_moyen_planete = moyenne_emission_planete
emission_moyen_lancement = total_emission_lancement/10

emission_moyen_ouverture_menu_lat = total_emission_ouverture_menu_lat/10
emission_moyen_fermeture_menu_lat = total_emission_fermeture_menu_lat/10

emission_moyen_soumission_candidat = total_emission_soumission_candidat/19

emission_moyen_generation_candidat = total_emission_generation_candidat/10

emission_moyen_ouverture_menu_lat2 = total_emission_ouverture_menu_lat2/10
emission_moyen_fermeture_menu_lat2 = total_emission_fermeture_menu_lat2/10

emission_moyen_bouton_vote_ouverture = total_emission_ouverture_bouton_vote/10
emission_moyen_bouton_vote_fermeture = total_emission_fermeture_bouton_vote/10

emission_moyen_democratie_liquide_ouverture = total_emission_ouverture_democratie_liquide/10
emission_moyen_democratie_liquide_fermeture = total_emission_fermeture_democratie_liquide/10

emission_moyen_copeland_liquide = total_emission_copeland_liquide/10
emission_moyen_borda_liquide = total_emission_borda_liquide/5
emission_moyen_pluralite_liquide = total_emission_pluralite_liquide/5
emission_moyen_stv_liquide = total_emission_stv_liquide/5
emission_moyen_approbation_liquide = total_emission_approbation_liquide/5

emission_moyen_copeland = total_emission_copeland/10
emission_moyen_borda = total_emission_borda/5
emission_moyen_pluralite = total_emission_pluralite/5
emission_moyen_stv = total_emission_stv/5
emission_moyen_approbation = total_emission_approbation/5