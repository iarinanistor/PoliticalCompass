from fuzzywuzzy import fuzz
import speech_recognition as sr

# Définition des commandes avec leur valeur
data_set_commands  = { # data set pour le numero de commandes 
    "lance borda": 1,
    "lance copeland": 2,
    "lance pluralité": 3,
    "lance STV": 4,
    "génère un candidats": 5,
    "Jenner" :5
}

data_set_preProcessing = { # data set pour pouvoir regroup les commande par classe 
    "lance": 1,
    "génère": 2,
    "Jenner":2
}
class SLCV():
    def __init__(self,data_set_preProcessing=data_set_preProcessing,data_set_commands = data_set_commands ) :
        self.data_preProcessing = data_set_preProcessing #data set pour le numero de commandes 
        self.data_commands = data_set_commands # data set pour pouvoir regroup les commande par classe 
        
    def ecouter(self):
        """
        fonction qui retourn la phrase dite en vocal grace a l'api google 
        args :
        return un str 
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
        input str phrase , dic data_set_commands
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
        input str phrase , dic data_set
        renvoie le numero de la commande si on dectete le mot dans la phrase None sinon
        
        retrun int or None 
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
        faite un pre_analyse de la phrase en coupant et recolant les morceaux de phrase en fonction des mots clée dans le data_set
        
        args dico
        
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
        fait l'analyse complet du dico et renvoie une liste de itn qui reprenste les commande a lancer
        int []
        """
        tas = []
        for clée in dico.keys():
            phrase = dico[clée]
            Ncmd = self.detection_mots(phrase.strip(), data_set)
            if Ncmd: tas.append(Ncmd[0])
        return tas

    def use(self):
        """
        fait l'analyse complet de la phrase dit en vocal et renvoie une liste de itn qui reprenste les commande a lancer
        int []
        """
        return self.traitement(self.pre_analse(self.ecouter(),self.data_preProcessing),self.data_commands)

