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
    """Opens the main menu on program startup."""
    # Performs scaling to prevent tiny UI on high resolution screens.
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    os.environ["QT_SCALE_FACTOR"] = "2"
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    people_overview_file, logs_file = file_names()
    setup_logging(logs_file)
    mwindow_main_menu = MainMenuWindow(people_overview_file)
    mwindow_main_menu.show()
    sys.exit(app.exec())


def file_names() -> tuple:
    people_overview_file = "resources/people_overview.json"
    # If people_overview.json doesn't exist, create it /resources.
    if not pathlib.Path(people_overview_file).exists():
        generate_random_people_config(people_overview_file)
    logs_file = "resources/logs.txt"
    return people_overview_file, logs_file


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


class MainMenuWindow(QMainWindow, Ui_mwindow_main_menu):
    """Contains the main window for the lift control simulation."""

    def __init__(self, people_overview_file: str):
        super().__init__()
        self.setupUi(self)

        # Reads existing JSON files for list of people.
        with open(people_overview_file, "r") as infile:
            try:
                people_overview = json.load(infile)
            except json.decoder.JSONDecodeError:
                generate_random_people_config(people_overview_file)
                people_overview = json.load(infile)
        self.num_floors = 5
        self.num_people = len(people_overview)
        self.lift_capacity = 5
        self.ui_delay = 500

        # Updates labels to show current configuration.
        self.lbl_num_floors.setText("Number of Floors: " + str(self.num_floors))
        self.lbl_num_people.setText("Number of People: " + str(self.num_people))
        self.lbl_lift_capacity.setText("Lift Capacity: " + str(self.lift_capacity))
        self.lbl_ui_delay.setText("UI Delay (Milliseconds): " + str(self.ui_delay))
        # Connects 'Configure Simulation' button to the configure simulation
        # dialog.
        self.btn_config_sim.clicked.connect(self.open_dialog_config_sim)
        # Connects 'Open Simulation' button to the relevant simulation window.
        self.btn_open_sim.clicked.connect(
            lambda: self.open_mwindow_lift_sim(people_overview_file)
        )
        QApplication.processEvents()

    def open_dialog_config_sim(self, people_overview_file: str) -> None:
        """Opens the dialog for the user to configure their simulation."""
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
        """Opens the main window for the lift simulation."""
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
        self.update_floors(people_overview)
        # Connects 'Generate New Simulation' button to generate a new
        # simulation with the current configuration settings.
        self.MWindow.btn_generate_new_sim.clicked.connect(
            lambda: self.generate_new_sim(people_overview_file)
        )
        # Connects 'Run Simulation (Naive)' button to run the simulation with
        # the naive (mechanical) algorithm.
        self.MWindow.btn_run_sim_naive.clicked.connect(
            lambda: self.run_simulation_naive(people_overview_file)
        )
        # Connects 'Run Simulation (Improved)' button to run the simulation
        # with the improved algorithm.
        self.MWindow.btn_run_sim_improved.clicked.connect(
            lambda: self.run_simulation_improved(people_overview_file)
        )
        self.generate_new_sim(people_overview_file)
        self.MWindow.show()

    def save_sim(self, people_overview_file: str):
        """Saves the lift simulation settings."""
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
            self.ui_delay = self.Dialog.line_edit_ui_delay.text()
            # Updates labels to show current configuration.
            self.lbl_num_floors.setText("Number of Floors: " + str(self.num_floors))
            self.lbl_num_people.setText("Number of People: " + str(self.num_people))
            self.lbl_lift_capacity.setText("Lift Capacity: " + str(self.lift_capacity))
            self.lbl_ui_delay.setText("UI Delay: " + str(self.ui_delay))
            # Updates 'Open Simulation' button to open the relevant
            # simulation window.
            self.btn_open_sim.clicked.connect(
                lambda: self.open_mwindow_lift_sim(people_overview_file)
            )
        QApplication.processEvents()

    def update_floors(self, people_overview: list):
        """
        Updates values in UI for each floor.

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

    def generate_new_sim(self, people_overview_file: str) -> None:
        """Generates a new simulation with current configuration settings."""
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
        self.update_floors(people_overview)
        # Resets tracking stats to 0.
        self.MWindow.lbl_num_delivered.setText("Number of People Delivered: 0")
        self.MWindow.lbl_distance_travelled.setText("Total Distance Travelled: 0")
        # Provides confirmation that generation was successful.
        self.MWindow.lbl_update.setText("New simulation generated successfully.")
        QApplication.processEvents()

    def run_simulation_naive(self, people_overview_file: str) -> None:
        """
        Runs the simulation using the naive (mechanical) algorithm.

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
        """
        num_delivered = 0
        distance_travelled = 0
        num_in_lift = 0
        people_lift = []
        self.lift_floor = 0
        lift_direction = "Up"

        # Reads existing JSON files for list of people.
        with open(people_overview_file, "r") as infile:
            people_overview = json.load(infile)
        self.display_config_info(people_overview)

        # Continues simulation until all target floors are reached.
        while (
            next((d for d in people_overview if not d["delivered"]), None) is not None
        ):
            # Iterates in order of the people generated (represents a queue).
            for person in people_overview:
                if person["delivered"] is False:
                    # Calculates the number of moves needed to reach the next
                    # person's starting floor.
                    collect_moves = int(person["start_floor"]) - self.lift_floor
                    print("\nFloor Differential (Collecting):", abs(collect_moves))

                    # Moves the lift floor by floor to collect the person, and
                    # adds them to the list of people in the lift.
                    while True:
                        # Doesn't move the lift if on correct floor.
                        if self.lift_floor == person["start_floor"]:
                            # Updates the number of people in the lift.
                            num_in_lift += 1
                            self.MWindow.lbl_num_in_lift.setText(
                                "Number of People in Lift: " + str(num_in_lift)
                            )
                            QApplication.processEvents()
                            break
                        else:
                            sleep(int(self.ui_delay) / 1000)
                            # Moves the lift up or down based on the person's
                            # start floor relative to the lift's current floor,
                            # and whether the lift needs to change direction,
                            # then displays the floor moved to.
                            if lift_direction == "Up":
                                self.lift_floor += 1
                            else:
                                self.lift_floor -= 1
                            self.update_floors(people_overview)
                            distance_travelled += 1
                            self.MWindow.lbl_distance_travelled.setText(
                                "Total Distance Travelled: " + str(distance_travelled)
                            )
                            QApplication.processEvents()
                            print("    Lift Floor (Collecting):", self.lift_floor)

                        # Changes the lift's direction if they have reached
                        # the end.
                        if self.lift_floor == 0 and lift_direction == "Down":
                            lift_direction = "Up"
                        if (
                            self.lift_floor == int(self.num_floors) - 1
                            and lift_direction == "Up"
                        ):
                            lift_direction = "Down"
                    people_lift.append(person)

                    # Iterates whilst there are people in the lift.
                    while people_lift:
                        # Checks if there's a person on the floor going the
                        # same direction and collects them if they are.
                        for extra in people_overview:
                            if (
                                extra not in people_lift
                                and extra["start_floor"] == self.lift_floor
                                and extra["delivered"] is False
                                and extra["direction"] == person["direction"]
                            ):
                                people_lift.append(extra)
                                num_in_lift += 1
                                self.MWindow.lbl_num_in_lift.setText(
                                    "Number of People in Lift: " + str(num_in_lift)
                                )
                                QApplication.processEvents()
                                print(
                                    "\nThere are now",
                                    num_in_lift,
                                    "people in the lift, as person",
                                    extra["id"],
                                    "has been added to the lift.",
                                )

                        # Displays an updated version of the list of people in
                        # the lift.
                        print("\nPeople in Lift:")
                        for passenger in people_lift:
                            print(passenger)

                        # Displays the number of moves needed to deliver the
                        # next closest person in the lift.
                        deliver_moves = min(
                            [
                                abs(int(passenger["target_floor"]) - self.lift_floor)
                                for passenger in people_lift
                            ]
                        )
                        print("\nFloor Differential (Delivering):", deliver_moves)
                        sleep(int(self.ui_delay) / 1000)

                        # Moves the lift up or down based on the person's
                        # target floor relative to the lift's current floor,
                        # and whether the lift needs to change direction, then
                        # displays the floor moved to.
                        if lift_direction == "Up":
                            self.lift_floor += 1
                        else:
                            self.lift_floor -= 1

                        distance_travelled = self.update_current_floor_of_passengers(
                            distance_travelled, people_lift, people_overview
                        )
                        print("    Lift Floor (Delivering):", self.lift_floor)

                        # Changes the lift's direction if they have reached
                        # the end.
                        if self.lift_floor == 0 and lift_direction == "Down":
                            lift_direction = "Up"
                        if (
                            self.lift_floor == int(self.num_floors) - 1
                            and lift_direction == "Up"
                        ):
                            lift_direction = "Down"

                        # Checks if the lift has arrived at the target floor of
                        # anyone in the lift, and drops them off if it has.
                        for passenger in people_lift[:]:
                            if passenger["target_floor"] == self.lift_floor:
                                num_in_lift = self.mark_passenger_as_delivered(
                                    num_delivered,
                                    num_in_lift,
                                    passenger,
                                    people_lift,
                                    people_overview,
                                )

        # Displays the updated version of the list of
        # people.
        print("\nPeople Overview (Simulation Complete):")
        for person in people_overview:
            print(person)
        sleep(int(self.ui_delay) / 1000)
        self.MWindow.lbl_update.setText("Simulation complete.")
        QApplication.processEvents()

    def mark_passenger_as_delivered(
        self,
        num_delivered: int,
        num_in_lift: int,
        passenger: dict,
        people_lift: list,
        people_overview: list,
    ) -> int:
        """
        Marks a passenger as delivered, and removes them from the lift.

        Args:
            num_delivered: The number of people delivered so far.
            num_in_lift: The number of people currently in the lift.
            passenger: The passenger to be marked as delivered.
            people_lift: The list of people currently in the lift.
            people_overview: The list of people in the simulation.

        Returns:
            The updated number of people in the lift.
        """
        sleep(int(self.ui_delay) / 1000)
        num_in_lift -= 1
        num_delivered += 1
        self.MWindow.lbl_num_in_lift.setText(
            "Number of People in Lift: " + str(num_in_lift)
        )
        self.MWindow.lbl_num_delivered.setText(
            "Number of People Delivered: " + str(num_delivered)
        )
        print(
            "\nDelivered person ID",
            passenger["id"],
            "from floor",
            passenger["start_floor"],
            "to",
            passenger["target_floor"],
        )
        self.MWindow.lbl_update.setText(
            "Delivered person ID "
            + str(passenger["id"])
            + " from floor "
            + str(passenger["start_floor"])
            + " to "
            + str(passenger["target_floor"])
        )
        QApplication.processEvents()
        # Marks the person as delivered.
        for person1 in people_overview:
            if person1["id"] == passenger["id"]:
                person1["delivered"] = True
        # Removes the person from the lift.
        people_lift.remove(passenger)
        return num_in_lift

    def display_config_info(self, people_overview: list) -> None:
        # Resets tracking stats to 0.
        self.MWindow.lbl_num_delivered.setText("Number of People Delivered: 0")
        self.MWindow.lbl_distance_travelled.setText("Total Distance Travelled: 0")
        self.MWindow.lbl_update.setText("")
        # Sets initial values for people waiting on each floor.
        self.update_floors(people_overview)
        # Displays configuration, generated people, and starting lift floor.
        print(
            "\n-------------------------------------------------------------"
            "\nNumber of Floors:",
            self.num_floors,
            "\nNumber of People:",
            self.num_people,
            "\nLift Capacity:",
            self.lift_capacity,
            "\nUI Delay (ms):",
            self.ui_delay,
        )
        print("\nPeople Generated:")
        for person in people_overview:
            print(person)
        print("\nLift Floor (Starting):", self.lift_floor)

    def run_simulation_improved(self, people_overview_file: str) -> None:
        """
        Runs the simulation using the improved algorithm.

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
        """
        num_delivered = 0
        distance_travelled = 0
        num_in_lift = 0
        people_pending = []
        people_lift = []
        self.lift_floor = 0

        # Reads existing JSON files for list of people.
        with open(people_overview_file, "r") as infile:
            people_overview = json.load(infile)
        self.display_config_info(people_overview)

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
                # Calculates if the lift needs to go up or down to collect the
                # next person.
                if people_pending[0]["start_floor"] - self.lift_floor > 0:
                    lift_direction = "Up"
                elif people_pending[0]["start_floor"] - self.lift_floor < 0:
                    lift_direction = "Down"
                else:
                    lift_direction = "None"

                # Number of floors the lift is away from collecting someone.
                floors_away = abs(
                    int(people_pending[0]["start_floor"]) - self.lift_floor
                )

                # Adds people as pending if they can be delivered en route.
                if lift_direction in ("Up", "Down"):
                    for extra in people_overview:
                        floors_away_extra = abs(
                            int(extra["target_floor"]) - self.lift_floor
                        )
                        if (
                            extra not in people_pending
                            and len(people_lift) < int(self.lift_capacity) - 1
                            and extra["delivered"] is False
                            and extra["direction"] == lift_direction
                            and floors_away_extra <= floors_away
                        ):
                            people_pending.append(extra)

                # Displays an updated version of the list of people pending.
                print("\nPeople Pending:")
                for waiting in people_pending:
                    print(waiting)

                # Checks if it needs to pick a pending person up.
                for waiting in people_pending[:]:
                    if waiting["start_floor"] == self.lift_floor:
                        people_lift.append(waiting)
                        people_pending.remove(waiting)
                        num_in_lift += 1
                        self.MWindow.lbl_num_in_lift.setText(
                            "Number of People in Lift: " + str(num_in_lift)
                        )
                        QApplication.processEvents()
                        print(
                            "\nThere are now",
                            num_in_lift,
                            "people in the lift, as person ID",
                            waiting["id"],
                            "has been added to the lift.",
                        )

                if people_pending:
                    # Displays the number of moves needed to collect the next
                    # person.
                    collect_moves = abs(
                        int(people_pending[0]["start_floor"]) - self.lift_floor
                    )
                    print("\nFloor Differential (Collecting):", collect_moves)
                    sleep(int(self.ui_delay) / 1000)

                    # Moves the lift up or down depending on the direction,
                    # and specifies the floor moved to.
                    if lift_direction == "Up":
                        self.lift_floor += 1
                    else:
                        self.lift_floor -= 1

                    distance_travelled = self.update_current_floor_of_passengers(
                        distance_travelled, people_lift, people_overview
                    )
                    print("    Lift Floor (Collecting):", self.lift_floor)

                # Iterates whilst there are people in the lift.
                while people_lift:
                    # Checks if the lift has arrived at the target floor of
                    # anyone in the lift, and drops them off if it has.
                    for passenger in people_lift[:]:
                        if passenger["target_floor"] == self.lift_floor:
                            num_in_lift = self.mark_passenger_as_delivered(
                                num_delivered,
                                num_in_lift,
                                passenger,
                                people_lift,
                                people_overview,
                            )
                            if passenger in people_pending:
                                people_pending.remove(passenger)

                    # Calculates the number of moves needed to reach the
                    # floor of the next closest person in the lift.
                    if people_lift:
                        # Checks if there's a person on the floor going the
                        # same direction and collects them if they are.
                        for extra in people_overview:
                            if (
                                extra not in people_lift
                                and len(people_lift) < int(self.lift_capacity)
                                and extra["start_floor"] == self.lift_floor
                                and extra["delivered"] is False
                                and extra["direction"] == people_lift[0]["direction"]
                            ):
                                people_lift.append(extra)
                                num_in_lift += 1
                                print(
                                    "\nThere are now",
                                    num_in_lift,
                                    "people in the lift, as person ID",
                                    extra["id"],
                                    "has been added to the lift.",
                                )

                        # Displays an updated version of the list of people
                        # in the lift.
                        print("\nPeople in Lift:")
                        for passenger in people_lift:
                            print(passenger)
                        # Displays the next closest floor to deliver a person.
                        deliver_moves = min(
                            [
                                abs(int(passenger["target_floor"]) - self.lift_floor)
                                for passenger in people_lift
                            ]
                        )
                        print("\nFloor Differential (Delivering):", deliver_moves)
                        sleep(int(self.ui_delay) / 1000)

                        # Moves the lift up or down depending on the
                        # direction, and specifies the floor moved to.
                        if people_lift[0]["direction"] == "Up":
                            self.lift_floor += 1
                        else:
                            self.lift_floor -= 1

                        distance_travelled = self.update_current_floor_of_passengers(
                            distance_travelled, people_lift, people_overview
                        )
                        print("    Lift Floor (Delivering):", self.lift_floor)

        # Displays the updated version of the list of people.
        print("\nPeople Overview (Simulation Complete):")
        for person in people_overview:
            print(person)
        sleep(int(self.ui_delay) / 1000)
        self.MWindow.lbl_update.setText("Simulation complete.")
        QApplication.processEvents()

    def update_current_floor_of_passengers(
        self, distance_travelled, people_lift, people_overview
    ):
        # Updates the current floor of people in lift.
        for passenger in people_lift:
            for person in people_overview:
                if person["id"] == passenger["id"]:
                    passenger["current_floor"] = self.lift_floor
                    person["current_floor"] = self.lift_floor
        self.update_floors(people_overview)
        distance_travelled += 1
        self.MWindow.lbl_distance_travelled.setText(
            "Total Distance Travelled: " + str(distance_travelled)
        )
        QApplication.processEvents()
        return distance_travelled


class ConfigSimDialog(QDialog, QIntValidator, Ui_dialog_config_sim):
    """Contains the dialog window for creating a new lift simulation."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class LiftSim2FloorsWindow(QMainWindow, Ui_mwindow_sim_2_floors):
    """Contains the main window for simulating two floors."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class LiftSim3FloorsWindow(QMainWindow, Ui_mwindow_sim_3_floors):
    """Contains the main window for simulating three floors."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class LiftSim4FloorsWindow(QMainWindow, Ui_mwindow_sim_4_floors):
    """Contains the main window for simulating four floors."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class LiftSim5FloorsWindow(QMainWindow, Ui_mwindow_sim_5_floors):
    """Contains the main window for simulating five floors."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class LiftSim6FloorsWindow(QMainWindow, Ui_mwindow_sim_6_floors):
    """Contains the main window for simulating six or more floors."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    main()
