"""
"""

from datetime import datetime

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog

from new_sim_setup import Ui_dialog_new_sim


class NewSimDialog(QDialog, Ui_dialog_new_sim):
    """Contains the dialog window for creating a new lift simulation."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Restricts inputs to only numbers.
        self.line_edit_num_floors.setValidator(self.only_int)
        self.line_edit_num_people.setValidator(self.only_int)
        self.line_edit_lift_capacity.setValidator(self.only_int)
        self.line_edit_ui_speed.setValidator(self.only_int)

        # Connects the 'Start New Simulation' button to start the simulation.
        self.btn_start_sim.connect(self.start_sim)

    def start_sim(self):
        """Starts the lift simulation in the main window."""
        # Gets the inputs for the new sale.
        num_floors = self.line_edit_num_floors.text()
        num_people = self.line_edit_num_people.text()
        lift_capacity = self.line_edit_lift_capacity.text()
        ui_speed = self.line_edit_ui_speed.text()

        # Validates against null inputs.
        if (num_floors != "" and num_people != "" and lift_capacity != "" and
                ui_speed != ""):
            pass

            # Notifies the user that their simulation was started successfully.
            self.lbl_start_successful.setText(
                "Simulation started successfully!")
        else:
            # Notifies the user that their simulation was not started
            # successfully.
            self.lbl_start_successful.setText(
                "Please fill all input fields to start your simulation.")
