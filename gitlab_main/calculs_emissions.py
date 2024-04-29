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
    return total_emissions, moyenne


## Affichage des calculs


#Emission totale du lancement
total_emission_lancement, moyenne_emission_lancement = emission_totale('Mesures_emissions/emissions_lancement.csv', debut=0, fin=None)

#Emission totale de Individus init
total_emission_individus, moyenne_emission_individus = emission_totale('Mesures_emissions/emissions_individus.csv', debut=0, fin=None)

#Emission totale de l'ouverture du MenuLateral
total_emission_ouverture_menu_lat, moyenne_emission_fermeture_menu_lat = emission_totale('Mesures_emissions/emissions_MenuLateral_ouverture.csv', debut=0, fin=None)

#Emission totale de la fermeture du MenuLateral
total_emission_fermeture_menu_lat, moyenne_emission_fermeture_menu_lat = emission_totale('Mesures_emissions/emissions_MenuLateral_fermeture.csv', debut=0, fin=None)

#Emission totale de la soumission d'une candidat
total_emission_soumission_candidat, moyenne_emissions_soumission_candidat = emission_totale('Mesures_emissions/emissions_soumission_candidat.csv', debut=0, fin=None)

#Emission totale de la generation d'un candidat
total_emission_generation_candidat, moyenne_emissions_soumission_candidat = emission_totale('Mesures_emissions/emissions_soumission_candidat.csv', debut=0, fin=None)

#Emission totale de l'ouverture du MenuLateral
total_emission_ouverture_menu_lat2, moyenne_emission_ouverture_menu_lat2 = emission_totale('Mesures_emissions/emissions_MenuLateral2_ouverture.csv', debut=0, fin=None)

#Emission totale de la fermeture du MenuLateral
total_emission_fermeture_menu_lat2, moyenne_emission_fermeture_menu_lat2 = emission_totale('Mesures_emissions/emissions_MenuLateral2_fermeture.csv', debut=0, fin=None)

#Emission totale du bouton des règles de vote (ouverture)
total_emission_ouverture_bouton_vote, moyenne_emission_ouverture_bouton_vote = emission_totale('Mesures_emissions/emissions_Bouton_vote_ouverture.csv', debut=0, fin=None)

#Emission totale du bouton des règles de vote (fermeture)
total_emission_fermeture_bouton_vote, moyenne_emission_fermeture_bouton_vote = emission_totale('Mesures_emissions/emissions_Bouton_vote_fermeture.csv', debut=0, fin=None)

#Emission totale de Copeland
total_emission_copeland, moyenne_emission_copeland = emission_totale('Mesures_emissions/emissions_Copeland.csv', debut=0, fin=None)

#Emission totale de Borda
total_emission_borda, moyenne_emission_borda = emission_totale('Mesures_emissions/emissions_Borda.csv', debut=0, fin=None)

#Emission totale de Pluralite
total_emission_pluralite, moyenne_emission_pluralite = emission_totale('Mesures_emissions/emissions_Pluralite.csv', debut=0, fin=None)

#Emission totale de STV
total_emission_stv, moyenne_emission_stv = emission_totale('Mesures_emissions/emissions_STV.csv', debut=0, fin=None)

#Emission totale de Approbation
total_emission_approbation, moyenne_emission_approbation = emission_totale('Mesures_emissions/emissions_Approbation.csv', debut=0, fin=None)


#Emission totale de Map 3D
total_emission_Map_3D, moyenne_emission_Map_3D = emission_totale('Mesures_emissions/emissions_Map_3D.csv', debut=0, fin=None)

#Emission totale de Map 2D
total_emission_Map_2D, moyenne_emission_Map_2D = emission_totale('Mesures_emissions/emissions_Map_2D.csv', debut=0, fin=None)


#Emission totale de Activer CV
total_emission_Activer_CV, moyenne_emission_Activer_CV = emission_totale('Mesures_emissions/emissions_Activer_CV.csv', debut=0, fin=None)

#Emission totale de ajoute 0.1
total_emission_ajoute, moyenne_emission_ajoute = emission_totale('Mesures_emissions/emissions_ajoute_0.1.csv', debut=0, fin=None)

#Emission totale de ajoute -0.1
total_emission_ajoute_moins, moyenne_emission_ajoute_moins = emission_totale('Mesures_emissions/emissions_ajoute_-0.1.csv', debut=0, fin=None)

#Emission totale de click map
total_emission_click_map, moyenne_emission_click_map = emission_totale('Mesures_emissions/emissions_click_map.csv', debut=0, fin=None)

#Emission totale de Supprimer
total_emission_Supprimer, moyenne_emission_Supprimer = emission_totale('Mesures_emissions/emissions_Supprimer.csv', debut=0, fin=None)

#Emission totale de Type Generation
total_emission_type_Generation, moyenne_emission_type_Generation = emission_totale('Mesures_emissions/emissions_type_Generation.csv', debut=0, fin=None)

#Emission totale de Creer Map
total_emission_Creer_Map, moyenne_emission_Creer_Map = emission_totale('Mesures_emissions/emissions_Creer_Map.csv', debut=0, fin=None)

#Emission totale de ecrire
total_emission_ecrire, moyenne_emission_ecrire = emission_totale('Mesures_emissions/emissions_ecrire.csv', debut=0, fin=None)

#Emission totale de lire
total_emission_lire, moyenne_emission_lire = emission_totale('Mesures_emissions/emissions_lire.csv', debut=0, fin=None)

#Emission totale de Arbre tournoi
total_emission_Arbre_tournoi, moyenne_emission_Arbre_tournoi = emission_totale('Mesures_emissions/emissions_Arbre_tournoi.csv', debut=0, fin=None)

#Emission totale de LWindow
total_emission_LWindow, moyenne_emission_LWindow = emission_totale('Mesures_emissions/emissions_LWindow.csv', debut=0, fin=None)



### Variables contenant les moyennes

emission_moyen_individus = moyenne_emission_individus
emission_moyen_lancement = total_emission_lancement/10

emission_moyen_ouverture_menu_lat = total_emission_ouverture_menu_lat/10
emission_moyen_fermeture_menu_lat = total_emission_fermeture_menu_lat/10

emission_moyen_soumission_candidat = total_emission_soumission_candidat/19

emission_moyen_generation_candidat = total_emission_generation_candidat/10

emission_moyen_ouverture_menu_lat2 = total_emission_ouverture_menu_lat2/10
emission_moyen_fermeture_menu_lat2 = total_emission_fermeture_menu_lat2/10

emission_moyen_bouton_vote_ouverture = total_emission_ouverture_bouton_vote/10
emission_moyen_bouton_vote_fermeture = total_emission_fermeture_bouton_vote/10

emission_moyen_copeland = total_emission_copeland/10
emission_moyen_borda = total_emission_borda/5
emission_moyen_pluralite = total_emission_pluralite/5
emission_moyen_stv = total_emission_stv/5
emission_moyen_approbation = total_emission_approbation/5


emission_moyen_Map_3D = total_emission_Map_3D/10
emission_moyen_Map_2D = total_emission_Map_2D/10

emission_moyen_Activer_CV = total_emission_Activer_CV/10
emission_moyen_ajoute = total_emission_ajoute/10
emission_moyen_ajoute_moins = total_emission_ajoute_moins/10
emission_moyen_click_map = total_emission_click_map/10
emission_moyen_Supprimer = total_emission_Supprimer/10
emission_moyen_type_Generation = total_emission_type_Generation/10
emission_moyen_Creer_Map = total_emission_Creer_Map/10

emission_moyen_ecrire = total_emission_ecrire/10
emission_moyen_lire = total_emission_lire/10
emission_moyen_Arbre_tournoi = total_emission_Arbre_tournoi/10