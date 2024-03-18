from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler

csv_handler = CSVHandler('result.csv')

global i
i = 0

@measure_energy(handler=csv_handler)
def foo():
# Instructions to be evaluated.
    global i
    i += 1

for _ in range(100):
    foo()

csv_handler.save_data()