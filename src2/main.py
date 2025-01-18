import time

from simulation.drawer import Coordinates
from simulation.gui import Gui

if __name__ == "__main__":
    time.sleep(0.1)
    gui = Gui(Coordinates())
    while True:
        gui.sprite()
