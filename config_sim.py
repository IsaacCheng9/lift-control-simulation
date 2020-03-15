"""
"""

from datetime import datetime

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog

from config_sim_setup import Ui_dialog_config_sim


class ConfigSimDialog(QDialog, QIntValidator, Ui_dialog_config_sim):
    """Contains the dialog window for creating a new lift simulation."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Restricts inputs to only numbers.
        self.only_int = QIntValidator()
        self.line_edit_num_floors.setValidator(self.only_int)
        self.line_edit_num_people.setValidator(self.only_int)
        self.line_edit_lift_capacity.setValidator(self.only_int)
        self.line_edit_ui_delay.setValidator(self.only_int)

        # Connects the 'Save Simulation' button to save the configuration.
        self.btn_save_sim.clicked.connect(self.save_sim)

    def save_sim(self):
        """Saves the lift simulation settings."""
        # Gets the inputs for the new sale.
        num_floors = self.line_edit_num_floors.text()
        num_people = self.line_edit_num_people.text()
        lift_capacity = self.line_edit_lift_capacity.text()
        ui_delay = self.line_edit_ui_delay.text()

        # Validates against null inputs.
        if (num_floors != "" and num_people != "" and lift_capacity != "" and
                ui_delay != ""):
            # Notifies the user that their configuration was saved
            # successfully.
            self.lbl_save_successful.setText(
                "Configuration saved successfully!")
        else:
            # Notifies the user that their configuration was not saved
            # successfully.
            self.lbl_save_successful.setText(
                "Please fill all input fields to save your configuration.")
