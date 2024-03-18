#Importation des bibliothèques pour calculer la consommation d'énergie et l'empreinte carbone
from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
from pyJoules.device import DeviceFactory
from pyJoules.energy_meter import EnergyMeter

devices = DeviceFactory.create_devices()
meter = EnergyMeter(devices)

csv_handler = CSVHandler("Conso_energie.csv")