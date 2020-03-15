"""A system created to manage lift control, optimised for efficiency of use."""

import json
import logging
import sys
from typing import Tuple

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

from lift_control_setup import Ui_mwindow_lift_control
from config_sim import ConfigSimDialog


def main() -> None:
    """Opens the program window, and exits program when window is closed."""
    app = QtWidgets.QApplication(sys.argv)
    setup_logging()
    mwindow_lift_control = LiftControlWindow()
    mwindow_lift_control.show()
    sys.exit(app.exec())


def setup_logging():
    """
    Sets up the logging system to automatically log actions to log file.
    """
    logging.basicConfig(filename="logs.txt", level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    logging.debug("Lift Control program started.")


class LiftControlWindow(QMainWindow, Ui_mwindow_lift_control):
    """Contains the dialog window for inventory management."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connects 'New Simulation' button to the new simulation dialog.
        self.btn_config_sim.clicked.connect(self.open_dialog_config_sim)
        # Connects 'Run Simulation' button to run the simulation.
        self.btn_run_sim.clicked.connect(self.run_simulation)

    def open_dialog_config_sim(self) -> None:
        """Opens the dialog for the user to configure their simulation."""
        self.Dialog = ConfigSimDialog()
        self.Dialog.open()

    def run_simulation(self) -> None:
        """Runs the simulation based on the given configuration."""
        total_delivered = 0
        num_moves = 0
        num_in_lift = 0
        floor = []
        people = []

        # Checks whether the user has made a configuration.

        # Creates a random combination of starting positions and target
        # positions.


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    main()
