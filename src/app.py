"""
A system created to manage lift control, optimised for efficiency in distance
travelled by the lift.

The user is able to configure any number of floors, number of people, lift
capacity, and the delay of intervals in the user interface.

Their simulation can be visually displayed for up to five floors. For more
than five floors, a non-visual display is provided. In both cases, the user
can run their simulation with either the naive, mechanical lift algorithm, or
my improved lift algorithm.

The configured simulation remains the same until the user generates a new
simulation, or changes the configuration settings. This enables the user to
directly compare how the improved algorithm compares to the naive algorithm.

A temporary log of the simulations is also printed in the terminal. It records
the simulation configuration, people generated, movements of the lift, people
pending (if applicable), people in the lift, people delivered, and an overview
of people after the simulation is complete.
"""
import json
import logging
import os
import pathlib
import random
import sys
from time import sleep
from typing import Tuple

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIntValidator, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow

from src.setup.config_sim_setup import Ui_dialog_config_sim
from src.setup.main_menu_setup import Ui_mwindow_main_menu
from src.setup.sim_2_floors_setup import Ui_mwindow_sim_2_floors
from src.setup.sim_3_floors_setup import Ui_mwindow_sim_3_floors
from src.setup.sim_4_floors_setup import Ui_mwindow_sim_4_floors
from src.setup.sim_5_floors_setup import Ui_mwindow_sim_5_floors
from src.setup.sim_6_floors_setup import Ui_mwindow_sim_6_floors


def main() -> None:
    """
    Open the main menu on program startup.
    """
    # Performs scaling to prevent tiny UI on high resolution screens.
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    os.environ["QT_SCALE_FACTOR"] = "2"
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    people_overview_file, logs_file = get_file_names()
    setup_logging(logs_file)
    mwindow_main_menu = MainMenuWindow(people_overview_file)
    mwindow_main_menu.show()
    sys.exit(app.exec())


def get_file_names() -> tuple:
    """
    Get the file names of the people overview and log files.

    Returns:
        The file names of the people overview and log files.
    """
    people_overview_file = "resources/people_overview.json"
    # If people_overview.json doesn't exist, create it /resources.
    if not pathlib.Path(people_overview_file).exists():
        generate_random_people_config(people_overview_file)
    logs_file = "resources/logs.txt"
    return people_overview_file, logs_file


def setup_logging(logs_file: str) -> None:
    """
    Set up the logging system for debugging purposes.

    Args:
        logs_file: The directory of the file to save the logs to.
    """
    logging.basicConfig(
        filename=logs_file,
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logging.debug("Lift Control program started.")


def generate_random_people_config(file_path: str) -> None:
    """
    Randomly create a configuration of ten people with random start and target
    floors in a building of five floors.

    Args:
        file_path: The directory of the file to save the configuration to.
    """
    people = []
    for person in range(10):
        start_floor = random.randint(0, 4)
        while True:
            target_floor = random.randint(0, 4)
            if target_floor != start_floor:
                break
        person_config = {
            "id": person,
            "start_floor": start_floor,
            "target_floor": target_floor,
            "current_floor": start_floor,
            "delivered": False,
            "direction": "up" if target_floor > start_floor else "down",
        }
        people.append(person_config)
        # Save the people configuration to people_overview.json.
        with open(file_path, "w") as file:
            json.dump(people, file, indent=2)


class MainMenuWindow(QMainWindow, Ui_mwindow_main_menu):
    """
    The main window for the lift control simulation.
    """

    def __init__(self, people_overview_file: str):
        """
        Args:
            people_overview_file: The path of the file to get the people in the
                                  simulation from.
        """
        super().__init__()
        self.setupUi(self)

        # Read the JSON file for the list of people.
        with open(people_overview_file, "r") as infile:
            try:
                people_overview = json.load(infile)
            except json.decoder.JSONDecodeError:
                generate_random_people_config(people_overview_file)
                people_overview = json.load(infile)
        self.num_floors = 5
        self.num_people = len(people_overview)
        self.lift_capacity = 5
        # Set the default UI delay to 500 ms.
        self.ui_delay = 0.5

        # Updates labels to show current configuration.
        self.lbl_num_floors.setText("Number of Floors: " + str(self.num_floors))
        self.lbl_num_people.setText("Number of People: " + str(self.num_people))
        self.lbl_lift_capacity.setText("Lift Capacity: " + str(self.lift_capacity))
        self.lbl_ui_delay.setText("UI Delay (ms): " + str(self.ui_delay * 1000))
        # Connects 'Configure Simulation' button to the configure simulation
        # dialog.
        self.btn_config_sim.clicked.connect(
            lambda: self.open_dialog_config_sim(people_overview_file)
        )
        # Connects 'Open Simulation' button to the relevant simulation window.
        self.btn_open_sim.clicked.connect(
            lambda: self.open_mwindow_lift_sim(people_overview_file)
        )
        QApplication.processEvents()

    def open_dialog_config_sim(self, people_overview_file: str) -> None:
        """
        Open the dialog for the user to configure their simulation.

        Args:
            people_overview_file: The path of the file to get the people in the
                                  simulation from.
        """
        self.Dialog = ConfigSimDialog()
        # Restricts inputs to only numbers.
        self.only_int = QIntValidator()
        self.Dialog.line_edit_num_floors.setValidator(self.only_int)
        self.Dialog.line_edit_num_people.setValidator(self.only_int)
        self.Dialog.line_edit_lift_capacity.setValidator(self.only_int)
        self.Dialog.line_edit_ui_delay.setValidator(self.only_int)
        # Connects the 'Save Simulation' button to save the configuration.
        self.Dialog.btn_save_sim.clicked.connect(
            lambda: self.save_sim(people_overview_file)
        )
        self.Dialog.open()

    def open_mwindow_lift_sim(self, people_overview_file: str) -> None:
        """
        Open the main window for the lift simulation.

        Args:
            people_overview_file: The path of the file to get the people in the
                                  simulation from.
        """
        self.lift_floor = 0
        # Opens a different UI depending on the number of floors configured.
        if int(self.num_floors) == 2:
            self.MWindow = LiftSim2FloorsWindow()
        elif int(self.num_floors) == 3:
            self.MWindow = LiftSim3FloorsWindow()
        elif int(self.num_floors) == 4:
            self.MWindow = LiftSim4FloorsWindow()
        elif int(self.num_floors) == 5:
            self.MWindow = LiftSim5FloorsWindow()
        else:
            self.MWindow = LiftSim6FloorsWindow()

        # Reads existing JSON files for list of people.
        with open(people_overview_file, "r") as infile:
            people_overview = json.load(infile)
        # Sets initial values for people waiting on each floor.
        self.update_floors_in_gui(people_overview)
        # Connects 'Generate New Simulation' button to generate a new
        # simulation with the current configuration settings.
        self.MWindow.btn_generate_new_sim.clicked.connect(
            lambda: self.generate_new_sim(people_overview_file)
        )
        # Connects 'Run Simulation (Naive)' button to run the simulation with
        # the naive (mechanical) algorithm.
        self.MWindow.btn_run_sim_naive.clicked.connect(
            lambda: self.run_simulation_with_naive_algorithm(people_overview_file)
        )
        # Connects 'Run Simulation (Improved)' button to run the simulation
        # with the improved algorithm.
        self.MWindow.btn_run_sim_improved.clicked.connect(
            lambda: self.run_simulation_with_improved_algorithm(people_overview_file)
        )
        self.generate_new_sim(people_overview_file)
        self.MWindow.show()

    def save_sim(self, people_overview_file: str) -> None:
        """
        Save the lift simulation settings.

        Args:
            people_overview_file: The path of the file to get the people in the
                                  simulation from.
        """
        self.num_floors_input = self.Dialog.line_edit_num_floors.text()
        self.num_people_input = self.Dialog.line_edit_num_people.text()
        self.lift_capacity_input = self.Dialog.line_edit_lift_capacity.text()
        self.ui_delay_input = self.Dialog.line_edit_ui_delay.text()

        # Validates against inputs which are either too small or null.
        if (
            self.num_floors_input == ""
            or self.num_people_input == ""
            or self.lift_capacity_input == ""
            or self.ui_delay_input == ""
        ):
            self.Dialog.lbl_save_successful.setText(
                "Please fill in all the configuration options!"
            )
        elif int(self.num_floors_input) <= 1:
            self.Dialog.lbl_save_successful.setText(
                "Please configure at least two floors!"
            )
        elif int(self.num_people_input) <= 0:
            self.Dialog.lbl_save_successful.setText(
                "Please configure at least one person!"
            )
        elif int(self.lift_capacity_input) <= 0:
            self.Dialog.lbl_save_successful.setText(
                "Please configure a lift capacity of at least one person!"
            )
        elif int(self.ui_delay_input) <= 0:
            self.Dialog.lbl_save_successful.setText(
                "Please configure a UI delay of at least one millisecond!"
            )
        else:
            # Notifies the user that their configuration was saved
            # successfully.
            self.Dialog.lbl_save_successful.setText("Configuration saved successfully!")
            # Sets the inputs for the new lift simulation.
            self.num_floors = self.Dialog.line_edit_num_floors.text()
            self.num_people = self.Dialog.line_edit_num_people.text()
            self.lift_capacity = self.Dialog.line_edit_lift_capacity.text()
            self.ui_delay = float(self.Dialog.line_edit_ui_delay.text()) / 1000
            # Updates labels to show current configuration.
            self.lbl_num_floors.setText("Number of Floors: " + str(self.num_floors))
            self.lbl_num_people.setText("Number of People: " + str(self.num_people))
            self.lbl_lift_capacity.setText("Lift Capacity: " + str(self.lift_capacity))
            self.lbl_ui_delay.setText("UI Delay (ms): " + str(self.ui_delay * 1000))
            # Updates 'Open Simulation' button to open the relevant
            # simulation window.
            self.btn_open_sim.clicked.connect(
                lambda: self.open_mwindow_lift_sim(people_overview_file)
            )
        QApplication.processEvents()

    def update_floors_in_gui(self, people_overview: list) -> None:
        """
        Update values in GUI for each floor.

        Arguments:
            people_overview (list): A list of generated people.
        """
        # Resets floor statistics to recalculate them.
        self.floor_0_waiting = 0
        self.floor_1_waiting = 0
        self.floor_2_waiting = 0
        self.floor_3_waiting = 0
        self.floor_4_waiting = 0
        self.floor_0_delivered = 0
        self.floor_1_delivered = 0
        self.floor_2_delivered = 0
        self.floor_3_delivered = 0
        self.floor_4_delivered = 0

        # Increments waiting and delivered stats for each floor accordingly.
        for person in people_overview:
            if person["start_floor"] == 0 and person["current_floor"] == 0:
                self.floor_0_waiting += 1
            if person["start_floor"] == 1 and person["current_floor"] == 1:
                self.floor_1_waiting += 1
            if person["start_floor"] == 2 and person["current_floor"] == 2:
                self.floor_2_waiting += 1
            if person["start_floor"] == 3 and person["current_floor"] == 3:
                self.floor_3_waiting += 1
            if person["start_floor"] == 4 and person["current_floor"] == 4:
                self.floor_4_waiting += 1
            if person["target_floor"] == 0 and person["current_floor"] == 0:
                self.floor_0_delivered += 1
            if person["target_floor"] == 1 and person["current_floor"] == 1:
                self.floor_1_delivered += 1
            if person["target_floor"] == 2 and person["current_floor"] == 2:
                self.floor_2_delivered += 1
            if person["target_floor"] == 3 and person["current_floor"] == 3:
                self.floor_3_delivered += 1
            if person["target_floor"] == 4 and person["current_floor"] == 4:
                self.floor_4_delivered += 1

        # Sets grey and red blocks as images to represent floor lift is on.
        grey_block = QPixmap("resources/images/grey_block.png").scaled(150, 15)
        red_block = QPixmap("resources/images/red_block.png").scaled(125, 15)

        # Updates UI with appropriate values depending on number of floors.
        if int(self.num_floors) <= 5:
            self.MWindow.lbl_waiting_0.setText(str(self.floor_0_waiting))
            self.MWindow.lbl_waiting_1.setText(str(self.floor_1_waiting))
            self.MWindow.lbl_delivered_0.setText(str(self.floor_0_delivered))
            self.MWindow.lbl_delivered_1.setText(str(self.floor_1_delivered))
            self.MWindow.lbl_floor_0.setPixmap(grey_block)
            self.MWindow.lbl_floor_1.setPixmap(grey_block)

            if int(self.num_floors) >= 3:
                self.MWindow.lbl_waiting_2.setText(str(self.floor_2_waiting))
                self.MWindow.lbl_delivered_2.setText(str(self.floor_2_delivered))
                self.MWindow.lbl_floor_2.setPixmap(grey_block)
            if int(self.num_floors) >= 4:
                self.MWindow.lbl_waiting_3.setText(str(self.floor_3_waiting))
                self.MWindow.lbl_delivered_3.setText(str(self.floor_3_delivered))
                self.MWindow.lbl_floor_3.setPixmap(grey_block)
            if int(self.num_floors) == 5:
                self.MWindow.lbl_waiting_4.setText(str(self.floor_4_waiting))
                self.MWindow.lbl_delivered_4.setText(str(self.floor_4_delivered))
                self.MWindow.lbl_floor_4.setPixmap(grey_block)

            if self.lift_floor == 0:
                self.MWindow.lbl_floor_0.setPixmap(red_block)
            elif self.lift_floor == 1:
                self.MWindow.lbl_floor_1.setPixmap(red_block)
            elif self.lift_floor == 2:
                self.MWindow.lbl_floor_2.setPixmap(red_block)
            elif self.lift_floor == 3:
                self.MWindow.lbl_floor_3.setPixmap(red_block)
            elif self.lift_floor == 4:
                self.MWindow.lbl_floor_4.setPixmap(red_block)
        QApplication.processEvents()
        sleep(self.ui_delay)

    def generate_new_sim(self, people_overview_file: str) -> None:
        """
        Generate a new simulation with the current configuration settings.

        Args:
            people_overview_file: The path of the file to get the people in the
                                  simulation from.
        """
        # Empties the list of people generated to overwrite previous sim.
        people_overview = []

        # Generates people and their lift statuses as a list of
        # dictionaries.
        for i in range(int(self.num_people)):
            # Creates a random starting floor.
            start_floor = random.randrange(0, int(self.num_floors))
            # Creates a target floor which is different to starting floor.
            while True:
                target_floor = random.randrange(0, int(self.num_floors))
                if start_floor != target_floor:
                    break
            # Calculates the direction the person will be going.
            if target_floor - start_floor > 0:
                direction = "Up"
            else:
                direction = "Down"
            # Adds the person dictionary to the list.
            person = {
                "id": i,
                "start_floor": start_floor,
                "target_floor": target_floor,
                "current_floor": start_floor,
                "delivered": False,
                "direction": direction,
            }
            people_overview.append(person)

        # Saves the list of people to a JSON file.
        with open(people_overview_file, "w") as outfile:
            json.dump(people_overview, outfile, ensure_ascii=False, indent=4)
        # Sets initial values for people waiting on each floor.
        self.update_floors_in_gui(people_overview)
        # Resets tracking stats to 0.
        self.MWindow.lbl_num_delivered.setText("Number of People Delivered: 0")
        self.MWindow.lbl_distance_travelled.setText("Total Distance Travelled: 0")
        # Provides confirmation that generation was successful.
        self.MWindow.lbl_update.setText("New simulation generated successfully.")
        QApplication.processEvents()

    def display_simulation_info(self, people_overview: list) -> None:
        """
        Display the information about the simulation that has started.

        Args:
            people_overview: A list of the people in the simulation.
        """
        # Resets tracking stats to 0.
        self.MWindow.lbl_num_delivered.setText("Number of People Delivered: 0")
        self.MWindow.lbl_distance_travelled.setText("Total Distance Travelled: 0")
        self.MWindow.lbl_update.setText("")
        # Sets initial values for people waiting on each floor.
        self.update_floors_in_gui(people_overview)
        # Displays configuration, generated people, and starting lift floor.
        print(
            "\n-------------------------------------------------------------"
            f"\nNumber of Floors: {self.num_floors}"
            f"\nNumber of People: {self.num_people}"
            f"\nLift Capacity: {self.lift_capacity}"
            f"\nUI Delay (ms): {self.ui_delay * 1000}"
        )
        print("\nPeople Overview (Simulation Starting):")
        for person in people_overview:
            print(person)
        print(f"\nLift Floor: {self.lift_floor} (Starting)")

    def mark_passenger_as_delivered(
        self,
        num_people_delivered: int,
        num_in_lift: int,
        passenger: dict,
        people_lift: list,
        people_overview: list,
    ) -> Tuple[int, int]:
        """
        Mark a passenger as delivered and remove them from the lift.

        Args:
            num_people_delivered: The number of people delivered so far.
            num_in_lift: The number of people currently in the lift.
            passenger: The passenger to be marked as delivered.
            people_lift: The list of people currently in the lift.
            people_overview: The list of people in the simulation.

        Returns:
            The updated number of people delivered and number of people in the
            lift.
        """
        num_in_lift -= 1
        num_people_delivered += 1
        self.MWindow.lbl_num_in_lift.setText(
            "Number of People in Lift: " + str(num_in_lift)
        )
        self.MWindow.lbl_num_delivered.setText(
            "Number of People Delivered: " + str(num_people_delivered)
        )
        delivered_msg = (
            f"Delivered person ID {passenger['id']} "
            f"from floor {passenger['start_floor']} to {passenger['target_floor']}"
        )
        print(f"    {delivered_msg}")
        self.MWindow.lbl_update.setText(delivered_msg)
        QApplication.processEvents()
        sleep(self.ui_delay)
        # Find the person and mark them as delivered.
        for person1 in people_overview:
            if person1["id"] == passenger["id"]:
                person1["delivered"] = True
        # Remove the person from the lift.
        people_lift.remove(passenger)
        return num_people_delivered, num_in_lift

    def update_current_floor_of_passengers(
        self, distance_travelled: int, people_lift: list, people_overview: list
    ) -> int:
        """
        Update the current floor of passengers in the lift.

        Args:
            distance_travelled: The total distance travelled by the lift.
            people_lift: The list of people in the lift.
            people_overview: The list of people in the simulation.

        Returns:
            The updated total distance travelled by the lift.
        """
        for passenger in people_lift:
            for person in people_overview:
                if person["id"] == passenger["id"]:
                    passenger["current_floor"] = self.lift_floor
                    person["current_floor"] = self.lift_floor
        self.update_floors_in_gui(people_overview)
        distance_travelled += 1
        self.MWindow.lbl_distance_travelled.setText(
            "Total Distance Travelled: " + str(distance_travelled)
        )
        QApplication.processEvents()
        return distance_travelled

    def switch_lift_direction_if_at_top_or_bottom_floor(
        self, lift_direction: str
    ) -> str:
        """
        Switch the lift's direction if it has reached the top or bottom floor.

        Args:
            lift_direction: The current direction of the lift.
        """
        if self.lift_floor == 0 and lift_direction == "Down":
            lift_direction = "Up"
        if self.lift_floor == int(self.num_floors) - 1 and lift_direction == "Up":
            lift_direction = "Down"
        return lift_direction

    def collect_person_with_naive_algorithm(
        self,
        distance_travelled: int,
        lift_direction: str,
        num_in_lift: int,
        people_lift: list,
        people_overview: list,
        person: dict,
    ) -> Tuple[int, str, int]:
        """
        Collect a person from their start floor using the naive algorithm.

        Args:
            distance_travelled: The total distance travelled by the lift.
            lift_direction: Whether the lift is going up or down.
            num_in_lift: The number of people in the lift.
            people_lift: The list of people in the lift.
            people_overview: The list of people in the simulation.
            person: The person to collect.

        Returns:
            The updated distance travelled, lift direction and number of people
            in the lift.
        """
        while self.lift_floor != person["start_floor"]:
            # Moves the lift up or down based on the person's
            # start floor relative to the lift's current floor,
            # and whether the lift needs to change direction,
            # then displays the floor moved to.
            if lift_direction == "Up":
                self.lift_floor += 1
            else:
                self.lift_floor -= 1
            self.update_floors_in_gui(people_overview)
            distance_travelled += 1
            self.MWindow.lbl_distance_travelled.setText(
                "Total Distance Travelled: " + str(distance_travelled)
            )
            QApplication.processEvents()
            print(f"Lift Floor: {self.lift_floor} (Collecting)")
            lift_direction = self.switch_lift_direction_if_at_top_or_bottom_floor(
                lift_direction
            )
        # Collect the person and update the GUI.
        people_lift.append(person)
        num_in_lift += 1
        self.MWindow.lbl_num_in_lift.setText(
            "Number of People in Lift: " + str(num_in_lift)
        )
        QApplication.processEvents()
        return distance_travelled, lift_direction, num_in_lift

    def deliver_person_with_naive_algorithm(
        self,
        distance_travelled: int,
        lift_direction: str,
        num_people_delivered: int,
        num_in_lift: int,
        people_lift: list,
        people_overview: list,
        person: dict,
    ) -> Tuple[int, int, str, int]:
        """
        Deliver the person to their target floor and any additional people
        en-route.

        Args:
            distance_travelled: The total distance travelled by the lift.
            lift_direction: Whether the lift is going up or down.
            num_people_delivered: The number of people delivered in the
                                  simulation.
            num_in_lift: The number of people in the lift.
            people_lift: The list of people in the lift.
            people_overview: The list of people in the simulation.
            person: The person to collect.

        Returns:
            The updated distance travelled, updated number of people delivered,
            lift direction, and number of people in the lift.
        """
        while people_lift:
            # Checks if there's a person on the floor going the
            # same direction and collects them if they are.
            for en_route in people_overview:
                if (
                    en_route not in people_lift
                    and en_route["start_floor"] == self.lift_floor
                    and en_route["delivered"] is False
                    and en_route["direction"] == person["direction"]
                ):
                    people_lift.append(en_route)
                    num_in_lift += 1
                    collected_msg = (
                        f"Collected person ID {en_route['id']} en route, "
                        "as they are also going "
                        f"{en_route['direction'].lower()}."
                    )
                    print(f"    {collected_msg}")
                    self.MWindow.lbl_update.setText(collected_msg)
                    self.MWindow.lbl_num_in_lift.setText(
                        "Number of People in Lift: " + str(num_in_lift)
                    )
                    QApplication.processEvents()
                    sleep(self.ui_delay)

            # Continue moving the lift up or down until we reach
            # the top or bottom of the building.
            if lift_direction == "Up":
                self.lift_floor += 1
            else:
                self.lift_floor -= 1
            distance_travelled = self.update_current_floor_of_passengers(
                distance_travelled, people_lift, people_overview
            )
            print(f"Lift Floor: {self.lift_floor} (Delivering)")
            lift_direction = self.switch_lift_direction_if_at_top_or_bottom_floor(
                lift_direction
            )

            # Drop off passengers if we've reached their target.
            for passenger in people_lift[:]:
                if passenger["target_floor"] == self.lift_floor:
                    (
                        num_people_delivered,
                        num_in_lift,
                    ) = self.mark_passenger_as_delivered(
                        num_people_delivered,
                        num_in_lift,
                        passenger,
                        people_lift,
                        people_overview,
                    )
        return distance_travelled, num_people_delivered, lift_direction, num_in_lift

    def run_simulation_with_naive_algorithm(self, people_overview_file: str) -> None:
        """
        Run the simulation using the naive (mechanical) algorithm.

        This algorithm implements a traditional lift control system where the
        person requesting the lift will press a button to either go up or
        down once the lift arrives.

        The algorithm picks up people in order of who requested the lift first.
        It saves time en route of delivery of that person by delivering
        additional people if the lift has space and these people are travelling
        in the same direction. This strikes a balance between fairness and
        time saving, as people who request the lift first will still have
        greater priority.

        However, for the lift to change direction from going upwards to
        downwards, or from going downwards to upwards, it must travel to either
        the top or the bottom floor respectively.

        Args:
            people_overview_file: The path of the file to get the people in the
                                  simulation from.
        """
        num_people_delivered = 0
        distance_travelled = 0
        num_in_lift = 0
        people_lift = []
        self.lift_floor = 0
        lift_direction = "Up"

        # Reads existing JSON files for list of people.
        with open(people_overview_file, "r") as infile:
            people_overview = json.load(infile)
        self.display_simulation_info(people_overview)

        # Continues simulation until all target floors are reached.
        while (
            next((d for d in people_overview if not d["delivered"]), None) is not None
        ):
            # Iterates in order of the people generated (represents a queue).
            for person in people_overview:
                if person["delivered"] is False:
                    # Continue moving floors until we can collect the person.
                    (
                        distance_travelled,
                        lift_direction,
                        num_in_lift,
                    ) = self.collect_person_with_naive_algorithm(
                        distance_travelled,
                        lift_direction,
                        num_in_lift,
                        people_lift,
                        people_overview,
                        person,
                    )
                    # Deliver the person and any additional people in the lift.
                    (
                        distance_travelled,
                        num_people_delivered,
                        lift_direction,
                        num_in_lift,
                    ) = self.deliver_person_with_naive_algorithm(
                        distance_travelled,
                        lift_direction,
                        num_people_delivered,
                        num_in_lift,
                        people_lift,
                        people_overview,
                        person,
                    )

        self.display_simulation_summary(people_overview, distance_travelled)

    def collect_person_with_improved_algorithm(
        self,
        distance_travelled: int,
        num_in_lift: int,
        people_lift: list,
        people_overview: list,
        people_pending: list,
    ) -> Tuple[int, int]:
        """
        Collect a person from their start floor using the improved algorithm,
        delivering people who can be delivered en-route of collecting the
        person.

        Args:
            distance_travelled: The total distance travelled by the lift.
            num_in_lift: The number of people in the lift.
            people_lift: A list of people in the lift.
            people_overview: A list of people in the simulation.
            people_pending: A list of people who can be delivered en-route of
                            collecting the person.

        Returns:
            The total distance travelled by the lift and the number of people
            in the lift.
        """
        # Calculate if the lift needs to go up or down to collect the next
        # person.
        if people_pending[0]["start_floor"] - self.lift_floor > 0:
            lift_direction = "Up"
        elif people_pending[0]["start_floor"] - self.lift_floor < 0:
            lift_direction = "Down"
        else:
            lift_direction = "None"

        num_floors_away_from_collection = abs(
            int(people_pending[0]["start_floor"]) - self.lift_floor
        )
        # Add people as pending if they can be delivered en route of collecting
        # the person.
        if lift_direction in ("Up", "Down"):
            for en_route in people_overview:
                num_floors_away_en_route = abs(
                    int(en_route["target_floor"]) - self.lift_floor
                )
                if (
                    en_route not in people_pending
                    and len(people_lift) < int(self.lift_capacity) - 1
                    and en_route["delivered"] is False
                    and en_route["direction"] == lift_direction
                    and num_floors_away_en_route <= num_floors_away_from_collection
                ):
                    people_pending.append(en_route)

        # Check if it needs to pick any pending person up.
        for waiting in people_pending[:]:
            if waiting["start_floor"] == self.lift_floor:
                people_lift.append(waiting)
                people_pending.remove(waiting)
                num_in_lift += 1
                collected_msg = (
                    f"Collected person ID {waiting['id']} en route, as they "
                    f"are also going {waiting['direction'].lower()} and can be "
                    "dropped off en route."
                )
                print(f"    {collected_msg}")
                self.MWindow.lbl_update.setText(collected_msg)
                self.MWindow.lbl_num_in_lift.setText(
                    "Number of People in Lift: " + str(num_in_lift)
                )
                QApplication.processEvents()
                sleep(self.ui_delay)

        if people_pending:
            if lift_direction == "Up":
                self.lift_floor += 1
            else:
                self.lift_floor -= 1
            distance_travelled = self.update_current_floor_of_passengers(
                distance_travelled, people_lift, people_overview
            )
            print(f"Lift Floor: {self.lift_floor} (Collecting)")

        return distance_travelled, num_in_lift

    def deliver_person_with_improved_algorithm(
        self,
        distance_travelled: int,
        num_people_delivered: int,
        num_in_lift: int,
        people_lift: list,
        people_overview: list,
        people_pending: list,
    ) -> Tuple[int, int, int]:
        """
        Deliver a person from their start floor using the improved algorithm,
        delivering people who can be delivered en-route of delivering the
        person.

        Args:
            distance_travelled: The total distance travelled by the lift.
            num_people_delivered: The number of people delivered in the
                                  simulation.
            num_in_lift: The number of people in the lift.
            people_lift: A list of people in the lift.
            people_overview: A list of people in the simulation.
            people_pending: A list of people who can be delivered en-route of
                            collecting the person.

        Returns:
            The updated distance travelled by the lift, number of people
            delivered, and the number of people in the lift.
        """
        while people_lift:
            # Check if the lift has arrived at the target floor of anyone in
            # the lift, and drop them off if it has.
            for passenger in people_lift[:]:
                if passenger["target_floor"] == self.lift_floor:
                    (
                        num_people_delivered,
                        num_in_lift,
                    ) = self.mark_passenger_as_delivered(
                        num_people_delivered,
                        num_in_lift,
                        passenger,
                        people_lift,
                        people_overview,
                    )
                    if passenger in people_pending:
                        people_pending.remove(passenger)

            if people_lift:
                # Check if there's a person on the floor going the same
                # direction and collects them if they are.
                for en_route in people_overview:
                    if (
                        en_route not in people_lift
                        and len(people_lift) < int(self.lift_capacity)
                        and en_route["start_floor"] == self.lift_floor
                        and en_route["delivered"] is False
                        and en_route["direction"] == people_lift[0]["direction"]
                    ):
                        people_lift.append(en_route)
                        num_in_lift += 1

                # Move the lift up/down towards the target floor.
                if people_lift[0]["direction"] == "Up":
                    self.lift_floor += 1
                else:
                    self.lift_floor -= 1
                distance_travelled = self.update_current_floor_of_passengers(
                    distance_travelled, people_lift, people_overview
                )
                print(f"Lift Floor: {self.lift_floor} (Delivering)")
        return distance_travelled, num_people_delivered, num_in_lift

    def run_simulation_with_improved_algorithm(self, people_overview_file: str) -> None:
        """
        Run the simulation using the improved algorithm.

        This algorithm implements an improved lift control system where the
        person requesting the lift will enter the floor they want to travel to,
        as opposed to traditional lift systems where the person only presses
        a button saying they want to go up or down.

        The algorithm picks up people in order of who requested the lift first.
        It saves time en route of delivery of that person by delivering
        additional people if the lift has space and these people are travelling
        in the same direction. This strikes a balance between fairness and
        time saving, as people who request the lift first will still have
        greater priority.

        It also optimises moves by delivering people who can be delivered en
        route of the collection of people.

        Args:
            people_overview_file: The path of the file to get the people in the
                                  simulation from.
        """
        num_people_delivered = 0
        distance_travelled = 0
        num_in_lift = 0
        people_pending = []
        people_lift = []
        self.lift_floor = 0

        # Reads existing JSON files for list of people.
        with open(people_overview_file, "r") as infile:
            people_overview = json.load(infile)
        self.display_simulation_info(people_overview)

        # Continues simulation until all target floors are reached.
        while (
            next((d for d in people_overview if not d["delivered"]), None) is not None
        ):
            # Processes in order of requests generated (represents a queue
            # in chronological order).
            if not people_pending:
                for person in people_overview:
                    if person["delivered"] is False:
                        people_pending.append(person)
                        break
            else:
                # Collect the next person and deliver any people who can be
                # delivered en-route of collecting the person.
                (
                    distance_travelled,
                    num_in_lift,
                ) = self.collect_person_with_improved_algorithm(
                    distance_travelled,
                    num_in_lift,
                    people_lift,
                    people_overview,
                    people_pending,
                )
                # Deliver the person and any additional people who can be
                # delivered en-route of delivering the person.
                (
                    distance_travelled,
                    num_people_delivered,
                    num_in_lift,
                ) = self.deliver_person_with_improved_algorithm(
                    distance_travelled,
                    num_people_delivered,
                    num_in_lift,
                    people_lift,
                    people_overview,
                    people_pending,
                )

        self.display_simulation_summary(people_overview, distance_travelled)

    def display_simulation_summary(
        self, people_overview: list, distance_travelled: int
    ) -> None:
        """
        Display a summary of the simulation after it has finished.

        Args:
            people_overview: A list of people in the simulation.
            distance_travelled: The total distance travelled by the lift.
        """
        print("\nPeople Overview (Simulation Complete):")
        for person in people_overview:
            print(person)
        print(f"Total Distance Travelled: {distance_travelled}")
        self.MWindow.lbl_update.setText("Simulation complete.")
        QApplication.processEvents()


class ConfigSimDialog(QDialog, QIntValidator, Ui_dialog_config_sim):
    """
    The dialog window for creating a new lift simulation.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class LiftSim2FloorsWindow(QMainWindow, Ui_mwindow_sim_2_floors):
    """
    The main window when simulating two floors.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class LiftSim3FloorsWindow(QMainWindow, Ui_mwindow_sim_3_floors):
    """
    The main window when simulating three floors.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class LiftSim4FloorsWindow(QMainWindow, Ui_mwindow_sim_4_floors):
    """
    The main window when simulating four floors.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class LiftSim5FloorsWindow(QMainWindow, Ui_mwindow_sim_5_floors):
    """
    The main window when simulating five floors.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class LiftSim6FloorsWindow(QMainWindow, Ui_mwindow_sim_6_floors):
    """
    The main window when simulating six or more floors.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    main()
