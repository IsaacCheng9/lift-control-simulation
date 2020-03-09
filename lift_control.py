"""
"""

import json
import logging
import sys
from typing import Tuple

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

from lift_control_setup import Ui_mwindow_lift_control


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
        self.btn_new_sim.clicked.connect(self.open_dialog_new_sim)

    def open_dialog_new_sim(self) -> None:
        """Opens the dialog for the user to start a new simulation."""
        self.Dialog = NewSimDialog()
        self.Dialog.open()


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    main()
