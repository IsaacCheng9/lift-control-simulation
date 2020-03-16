"""A system created to manage lift control, optimised for efficiency of use."""

import json
import logging
import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog, QMainWindow

from config_sim_setup import Ui_dialog_config_sim
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
        self.btn_config_sim.clicked.connect(self.open_dialog_config_sim)
        # Connects 'Run Simulation' button to run the simulation.
        self.btn_run_sim.clicked.connect(self.run_simulation)

    def open_dialog_config_sim(self) -> None:
        """Opens the dialog for the user to configure their simulation."""
        self.Dialog = ConfigSimDialog()

        # Restricts inputs to only numbers.
        self.only_int = QIntValidator()
        self.Dialog.line_edit_num_floors.setValidator(self.only_int)
        self.Dialog.line_edit_num_people.setValidator(self.only_int)
        self.Dialog.line_edit_lift_capacity.setValidator(self.only_int)
        self.Dialog.line_edit_ui_delay.setValidator(self.only_int)

        # Connects the 'Save Simulation' button to save the configuration.
        self.Dialog.btn_save_sim.clicked.connect(self.save_sim)

        self.Dialog.open()

    def save_sim(self):
        """Saves the lift simulation settings."""
        # Gets the inputs for the new sale.
        num_floors = self.Dialog.line_edit_num_floors.text()
        num_people = self.Dialog.line_edit_num_people.text()
        lift_capacity = self.Dialog.line_edit_lift_capacity.text()
        ui_delay = self.Dialog.line_edit_ui_delay.text()

        # Validates against null inputs.
        if (num_floors != "" and num_people != "" and lift_capacity != "" and
                ui_delay != ""):
            # Notifies the user that their configuration was saved
            # successfully.
            self.Dialog.lbl_save_successful.setText(
                "Configuration saved successfully!")
        else:
            # Notifies the user that their configuration was not saved
            # successfully.
            self.Dialog.lbl_save_successful.setText(
                "Please fill all input fields to save your configuration.")

    def run_simulation(self) -> None:
        """Runs the simulation based on the given configuration."""
        total_delivered = 0
        num_moves = 0
        num_in_lift = 0
        floor = []
        people = []

        print(lift_capacity)

        # Checks whether the user has made a configuration.

        # Creates a random combination of starting positions and target
        # positions.


class ConfigSimDialog(QDialog, QIntValidator, Ui_dialog_config_sim):
    """Contains the dialog window for creating a new lift simulation."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    main()
