import socket

def connexion_internet():
    try:
        #Tentative de connexion
        socket.gethostbyname("www.google.com")
        return True
    except socket.error:
        return False


#Code ISO du pays où faire la mesure offline
iso_code = "FRA"

#Vérification de la connexion internet
internet = connexion_internet()
if internet:
    print("L'appareil est connecté à internet.")
else:
    print("L'appareil n'est pas connecté à internet.")