from fuzzywuzzy import fuzz
import speech_recognition as sr

# Définition des commandes avec leur valeur
data_set_commands  = { # data set pour le numero de commandes 
    "lance borda": 1,
    "lance copeland": 2,
    "lance pluralité": 3,
    "lance STV": 4,
    "lance approbation": 5,
    "génère un candidats": 6,
    "Jenner" :6,
    
}

data_set_preProcessing = { # data set pour pouvoir regroup les commande par classe 
    "lance": 1,
    "génère": 2,
    "Jenner":2
}
class SLCV():
    """
    Classe permettant d'interpréter les commandes vocales et d'exécuter les actions correspondantes. Elle gère la reconnaissance vocale,
    l'analyse des commandes, et l'exécution des opérations spécifiées par l'utilisateur.

    Attributes:
        data_preProcessing (dict): Dictionnaire des mots clés pour le prétraitement des commandes.
        data_commands (dict): Dictionnaire des commandes avec leurs valeurs numériques associées.

    Méthodes:
        __init__: Initialise une nouvelle instance de la classe SLCV. Elle configure les jeux de données nécessaires pour le prétraitement et la reconnaissance des commandes.
        ecouter: Écoute l'entrée vocale de l'utilisateur et tente de la transcrire en texte en utilisant l'API Google Speech.
        get_command_values: Identifie et extrait les valeurs des commandes à partir d'une phrase donnée, en utilisant le dictionnaire de commandes.
        detection_mots: Détecte les mots dans une phrase qui correspondent à des mots clés pré-définis, en utilisant le ratio de similarité de FuzzyWuzzy.
        pre_analyse: Segment et pré-analyse la phrase d'entrée pour regrouper les mots selon les mots clés identifiés, préparant l'analyse plus détaillée.
        traitement: Analyse les segments de phrases pré-analysés pour déterminer et exécuter les commandes correspondantes.
        use: Méthode principale utilisée pour exécuter le processus complet d'écoute, d'analyse et d'exécution des commandes vocales.
    """
    def __init__(self,data_set_preProcessing=data_set_preProcessing,data_set_commands = data_set_commands ) :
        self.data_preProcessing = data_set_preProcessing #data set pour le numero de commandes 
        self.data_commands = data_set_commands # data set pour pouvoir regroup les commande par classe 
        
    def ecouter(self):
        """
        Fonction qui retourne la phrase prononcée par l'utilisateur en utilisant l'API Google Speech.
        
        Returns:
            str: La phrase transcrise ou None si l'audio n'est pas compréhensible.
        """
        recognizer = sr.Recognizer() # Initialiser le recognizer
        with sr.Microphone() as source: # Utiliser le microphone comme source audio
            print("Dites quelque chose...")
            audio = recognizer.listen(source)

            try:
                # Reconnaissance vocale avec Google Web Speech API
                text = recognizer.recognize_google(audio, language="fr-FR")
                print("Vous avez dit :", text)
                return text
            except sr.UnknownValueError:
                print("Google Web Speech API n'a pas pu comprendre l'audio.")
                return None
            except sr.RequestError as e:
                print(f"Erreur lors de la requête à l'API Google Web Speech : {e}")

    def get_command_values(self,input_phrase,data_set_commands ):
        """
        Identifie les commandes dans la phrase d'entrée basée sur le jeu de données de commandes.
        
        Args:
            input_phrase (str): La phrase à analyser.
            data_set_commands (dict): Le dictionnaire des commandes avec leurs valeurs.
            
        Returns:
            list: Liste des valeurs des commandes identifiées.
        """
        commands = data_set_commands 
        command_values = []

        for phrase in commands:
            # Trouver le nombre d'occurrences de la phrase dans l'input_phrase
            count = input_phrase.count(phrase)
            if count > 0:
                command_values.extend([commands[phrase]] * count)
        return command_values

    def detection_mots(self,input_phrase, data_set):
        """
        Détecte et retourne le numéro de commande basé sur la similarité de mots clés trouvés dans la phrase.
        
        Args:
            input_phrase (str): La phrase à analyser.
            data_set (dict): Le dictionnaire des mots clés et leurs valeurs.
        
        Returns:
            list or None: Liste des valeurs de commandes détectées ou None si aucune correspondance.
        """

        command_values = []

        for phrase in data_set:
            # Utilisation de fuzz.ratio pour trouver la similitude entre les phrases
            similarity_score = fuzz.ratio(input_phrase, phrase)
            # Si le score de similitude dépasse un seuil donné, considérez-le comme une correspondance
            if similarity_score > 70:  # Vous pouvez ajuster ce seuil selon vos besoins
                command_values.append(data_set[phrase])

        return command_values if command_values else None  # Retourne None si aucune correspondance significative n'est trouvée

    def pre_analse(self,input_phrase, data_set):
        """
        Pré-analyse la phrase en segmentant et regroupant les morceaux basés sur les mots clés du jeu de données.
        
        Args:
            input_phrase (str): La phrase à analyser.
            data_set (dict): Le dictionnaire pour le prétraitement.
        
        Returns:
            dict: Dictionnaire des segments de phrase avec leurs valeurs de commandes associées.
        """
        phrases = input_phrase.split()
        resultat = {}
        cmdActuel = None
        cpt = 0
        for mot in phrases:
            NbDataSet = self.detection_mots(mot, data_set)
            if NbDataSet != None:
                cmdActuel = cpt
                cpt += 1
                if NbDataSet == [2] :resultat[cmdActuel-100] = mot + " "
                else : resultat[cmdActuel] = mot + " "
            elif cmdActuel is not None:
                if cmdActuel in resultat:
                    resultat[cmdActuel] += mot + " " # Ajouter la nouvelle clé au dictionnaire
        return resultat

    def traitement(self,dico, data_set):
        """
        Analyse le dictionnaire de segments de phrases et retourne les commandes à exécuter.
        
        Args:
            dico (dict): Dictionnaire des segments de phrases.
            data_set (dict): Le dictionnaire des commandes.
        
        Returns:
            list: Liste des numéros des commandes à exécuter.
        """
        tas = []
        for clée in dico.keys():
            phrase = dico[clée]
            Ncmd = self.detection_mots(phrase.strip(), data_set)
            if Ncmd: tas.append(Ncmd[0])
        return tas

    def use(self):
        """
        Analyse complète de la phrase prononcée et retourne les commandes à lancer.
        
        Returns:
            list: Liste des numéros des commandes à exécuter.
        """

        return self.traitement(self.pre_analse(self.ecouter(),self.data_preProcessing),self.data_commands)

