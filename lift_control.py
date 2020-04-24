"""A system created to manage lift control, optimised for efficiency of use."""
import json
import logging
import random
import sys
from time import sleep
from typing import Tuple

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
    """Sets up the logging system to automatically log actions to log file."""
    logging.basicConfig(filename="logs.txt", level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    logging.debug("Lift Control program started.")


class LiftControlWindow(QMainWindow, Ui_mwindow_lift_control):
    """Contains the dialog window for inventory management."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.num_floors = 5
        self.num_people = 5
        self.lift_capacity = 5
        self.ui_delay = 250

        # Connects 'New Simulation' button to the new simulation dialog.
        self.btn_config_sim.clicked.connect(self.open_dialog_config_sim)
        # Connects 'Run Simulation (Naive)' button to run the simulation with
        # the naive (mechanical) algorithm.
        self.btn_run_sim_naive.clicked.connect(
            lambda: self.run_simulation_naive())
        # Connects 'Run Simulation (Improved)' button to run the simulation
        # with the improved algorithm.
        self.btn_run_sim_improved.clicked.connect(
            lambda: self.run_simulation_improved())

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
        # Empties the list of people generated to overwrite previous config.
        people_overview = []

        # Gets the inputs for the new sale.
        self.num_floors = self.Dialog.line_edit_num_floors.text()
        self.num_people = self.Dialog.line_edit_num_people.text()
        self.lift_capacity = self.Dialog.line_edit_lift_capacity.text()
        self.ui_delay = self.Dialog.line_edit_ui_delay.text()

        # Validates against inputs of null and zero.
        if (self.num_floors != "" and self.num_people != "" and
                self.lift_capacity != "" and self.ui_delay != "" and
                int(self.num_floors) > 0 and int(self.num_people) > 0 and
                int(self.lift_capacity) > 0 and int(self.ui_delay) > 0):
            # Notifies the user that their configuration was saved
            # successfully.
            self.Dialog.lbl_save_successful.setText(
                "Configuration saved successfully!")

            # Generates people and their lift statuses as a list of
            # dictionaries.
            for i in range(int(self.num_people)):
                # Creates a random starting floor.
                starting_floor = random.randrange(0, int(self.num_floors))

                # Creates a target floor which is different to starting floor.
                while True:
                    target_floor = random.randrange(0, int(self.num_floors))
                    if starting_floor != target_floor:
                        break

                # Calculates the direction the person will be going.
                if target_floor - starting_floor > 0:
                    direction = "Up"
                else:
                    direction = "Down"

                # Adds the person dictionary to the list.
                person = {
                    "id": i,
                    "starting_floor": starting_floor,
                    "target_floor": target_floor,
                    "current_floor": 0,
                    "status": False,
                    "direction": direction}
                people_overview.append(person)

            # Saves the list of people to a JSON file.
            with open("people_overview.json", "w") as outfile:
                json.dump(people_overview, outfile,
                          ensure_ascii=False, indent=4)
        else:
            # Notifies the user that their configuration was not saved
            # successfully.
            self.Dialog.lbl_save_successful.setText(
                "Please fill all input fields to save your configuration.")

    def run_simulation_naive(self) -> None:
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
        num_moves = 0
        num_in_lift = 0
        people_lift = []
        lift_floor = 0
        lift_direction = "Up"

        # Reads existing JSON files for list of people.
        with open("people_overview.json", "r") as infile:
            people_overview = json.load(infile)

        # Displays configuration, generated people, and starting lift floor.
        print("\n-------------------------------------------------------------"
              "\nNumber of Floors:", self.num_floors, "\nNumber of People:",
              self.num_people, "\nLift Capacity:", self.lift_capacity,
              "\nUI Delay (ms):", self.ui_delay)
        print("\nPeople Generated")
        for person in people_overview:
            print(person)
        print("\nLift Floor (Starting):", lift_floor)

        # Continues simulation until all target floors are reached.
        while (next((d for d in people_overview if not d["status"]), None) is
               not None):
            # Iterates in order of the people generated (represents a queue).
            for person in people_overview:
                if person["status"] is False:
                    # Calculates the number of moves needed to reach the next
                    # person's starting floor.
                    collect_moves = (int(person["starting_floor"]) -
                                     lift_floor)
                    print("\nFloor Differential (Collecting):",
                          abs(collect_moves))

                    # Updates the number of people in the lift.
                    num_in_lift += 1
                    self.lbl_num_in_lift.setText("Number of People in Lift: " +
                                                 str(num_in_lift))

                    # Moves the lift floor by floor to collect the person, and
                    # adds them to the list of people in the lift.
                    while True:
                        # Doesn't move the lift if on correct floor.
                        if lift_floor == person["starting_floor"]:
                            break
                        else:
                            sleep(int(self.ui_delay) / 1000)
                            # Moves the lift up or down based on the person's
                            # start floor relative to the lift's current floor,
                            # and whether the lift needs to change direction,
                            # then displays the floor moved to.
                            if lift_direction == "Up":
                                lift_floor += 1
                            else:
                                lift_floor -= 1
                            num_moves += 1
                            self.lbl_num_moves.setText("Number of Moves: " +
                                                       str(num_moves))
                            print("    Lift Floor (Collecting):", lift_floor)

                        # Changes the lift's direction if they have reached
                        # the end.
                        if lift_floor == 0 and lift_direction == "Down":
                            lift_direction = "Up"
                        if (lift_floor == int(self.num_floors) and
                                lift_direction == "Up"):
                            lift_direction = "Down"
                    people_lift.append(person)

                    # Iterates whilst there are people in the lift.
                    while people_lift:
                        sleep(int(self.ui_delay) / 1000)

                        # Checks if there's a person on the floor going the
                        # same direction and collects them if they are.
                        for extra in people_overview:
                            if (extra not in people_lift and
                                extra["starting_floor"] == lift_floor and
                                extra["status"] is False and
                                    extra["direction"] == person["direction"]):
                                people_lift.append(extra)
                                num_in_lift += 1
                                self.lbl_num_in_lift.setText("Number of "
                                                             "People in "
                                                             "Lift: " +
                                                             str(num_in_lift))
                                print("\nThere are now", num_in_lift, "people "
                                      "in the lift, as person", extra["id"],
                                      "has been added to the lift.")

                        # Displays an updated version of the list of people in
                        # the lift.
                        print("\nPeople in Lift:")
                        for passenger in people_lift:
                            print(passenger)

                        # Displays the number of moves needed to deliver the
                        # next closest person in the lift.
                        deliver_moves = min(
                            [abs(int(passenger["target_floor"]) - lift_floor)
                             for passenger in people_lift])
                        print("\nFloor Differential (Delivering):",
                              deliver_moves)

                        # Moves the lift up or down based on the person's
                        # target floor relative to the lift's current floor,
                        # and whether the lift needs to change direction, then
                        # displays the floor moved to.
                        if lift_direction == "Up":
                            lift_floor += 1
                        else:
                            lift_floor -= 1
                        num_moves += 1
                        self.lbl_num_moves.setText("Number of Moves: "
                                                   + str(num_moves))
                        print("    Lift Floor (Delivering):", lift_floor)

                        # Changes the lift's direction if they have reached
                        # the end.
                        if lift_floor == 0 and lift_direction == "Down":
                            lift_direction = "Up"
                        if (lift_floor == int(self.num_floors) and
                                lift_direction == "Up"):
                            lift_direction = "Down"

                        # Checks if the lift has arrived at the target floor of
                        # anyone in the lift, and drops them off if it has.
                        for passenger in people_lift[:]:
                            if passenger["target_floor"] == lift_floor:
                                # Marks the person as delivered, and increments
                                # count.
                                num_in_lift -= 1
                                num_delivered += 1
                                self.lbl_num_in_lift.setText("Number of "
                                                             "People in "
                                                             "Lift: " +
                                                             str(num_in_lift))
                                self.lbl_num_delivered.setText(
                                    "Number of People Delivered: " +
                                    str(num_delivered))
                                print("\nDelivered person ID", passenger["id"],
                                      "from floor",
                                      passenger["starting_floor"], "to",
                                      passenger["target_floor"])

                                # Marks the person as delivered.
                                print("\nPeople Overview:")
                                for person in people_overview:
                                    if person["id"] == passenger["id"]:
                                        person["status"] = True

                                # Removes the person from the lift.
                                people_lift.remove(passenger)
                        
                        # Displays the updated version of the list of
                        # people.
                        print("\nPeople Overview:")
                        for person in people_overview:
                            print(person)

    def run_simulation_improved(self) -> None:
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
        num_moves = 0
        num_in_lift = 0
        people_pending = []
        people_lift = []
        lift_floor = 0

        # Reads existing JSON files for list of people.
        with open("people_overview.json", "r") as infile:
            people_overview = json.load(infile)

        # Displays configuration, generated people, and starting lift floor.
        print("\n-------------------------------------------------------------"
              "\nNumber of Floors:", self.num_floors, "\nNumber of People:",
              self.num_people, "\nLift Capacity:", self.lift_capacity,
              "\nUI Delay (ms):", self.ui_delay)
        print("\nPeople Generated:")
        for person in people_overview:
            print(person)
        print("\nLift Floor (Starting):", lift_floor)

        # Continues simulation until all target floors are reached.
        while (next((d for d in people_overview if not d["status"]), None) is
               not None):
            # Processes in order of requests generated (represents a queue
            # in chronological order).
            if not people_pending:
                for person in people_overview:
                    if person["status"] is False:
                        people_pending.append(person)
                        break
            else:
                sleep(int(self.ui_delay) / 1000)

                # Calculates if the lift needs to go up or down to collect the
                # next person.
                if people_pending[0]["starting_floor"] - lift_floor > 0:
                    lift_direction = "Up"
                elif people_pending[0]["starting_floor"] - lift_floor < 0:
                    lift_direction = "Down"

                # Number of floors the lift is away from collecting someone.
                floors_away = (abs(int(people_pending[0]["starting_floor"])
                                   - lift_floor))

                # Adds people as pending if they can be delivered en route.
                for extra in people_overview:
                    floors_away_extra = (abs(
                        int(extra["target_floor"]) - lift_floor))
                    if (extra not in people_pending and
                        len(people_lift) < int(self.lift_capacity) - 1
                        and extra["status"] is False and
                        extra["direction"] == lift_direction and
                            floors_away_extra <= floors_away):
                        people_pending.append(extra)

                # Displays an updated version of the list of people pending.
                print("\nPeople Pending:")
                for waiting in people_pending:
                    print(waiting)

                # Checks if it needs to pick a pending person up.
                for waiting in people_pending[:]:
                    if waiting["starting_floor"] == lift_floor:
                        people_lift.append(waiting)
                        people_pending.remove(waiting)
                        num_in_lift += 1
                        self.lbl_num_in_lift.setText("Number of People in "
                                                     "Lift: " +
                                                     str(num_in_lift))
                        print("\nThere are now", num_in_lift, "people in the "
                              "lift, as person ID", waiting["id"],
                              "has been added to the lift.")

                # Displays an updated version of the list of people waiting for
                # the lift.
                if people_lift:
                    print("\nPeople in Lift:")
                    for passenger in people_lift:
                        print(passenger)

                if people_pending:
                    # Displays the number of moves needed to collect the next
                    # person.
                    collect_moves = abs(
                        int(people_pending[0]["starting_floor"]) -
                        lift_floor)
                    print("\nFloor Differential (Collecting):",
                          collect_moves)

                    # Moves the lift up or down depending on the direction,
                    # and specifies the floor moved to.
                    if lift_direction == "Up":
                        lift_floor += 1
                    else:
                        lift_floor -= 1
                    num_moves += 1
                    self.lbl_num_moves.setText("Number of Moves: "
                                               + str(num_moves))
                    print("    Lift Floor (Collecting):", lift_floor)

                # Iterates whilst there are people in the lift.
                while people_lift:
                    sleep(int(self.ui_delay) / 1000)

                    # Checks if the lift has arrived at the target floor of
                    # anyone in the lift, and drops them off if it has.
                    for passenger in people_lift[:]:
                        if passenger["target_floor"] == lift_floor:
                            # Marks the person as delivered, and increments
                            # count.
                            num_in_lift -= 1
                            num_delivered += 1
                            self.lbl_num_in_lift.setText("Number of People in "
                                                         "Lift: " +
                                                         str(num_in_lift))
                            self.lbl_num_delivered.setText(
                                "Number of People Delivered: " +
                                str(num_delivered))
                            print("\nDelivered person ID", passenger["id"],
                                  "from floor", passenger["starting_floor"],
                                  "to", passenger["target_floor"])

                            # Marks the person as delivered.
                            for person in people_overview:
                                if person["id"] == passenger["id"]:
                                    person["status"] = True

                            # Ensures person is removed from lift and pending.
                            people_lift.remove(passenger)
                            if passenger in people_pending:
                                people_pending.remove(passenger)

                    # Displays the updated version of the list of
                    # people.
                    print("\nPeople Overview:")
                    for person in people_overview:
                        print(person)

                    # Calculates the number of moves needed to reach the
                    # floor of the next closest person in the lift.
                    if people_lift:
                        # Checks if there's a person on the floor going the
                        # same direction and collects them if they are.
                        for extra in people_overview:
                            if (extra not in people_lift and
                                len(people_lift) < int(self.lift_capacity)
                                and extra["starting_floor"] == lift_floor
                                and extra["status"] is False and
                                extra["direction"] ==
                                    people_lift[0]["direction"]):
                                people_lift.append(extra)
                                num_in_lift += 1
                                print("\nThere are now", num_in_lift,
                                      "people in the lift, as person ID",
                                      extra["id"],
                                      "has been added to the lift.")

                        # Displays an updated version of the list of people
                        # in the lift.
                        print("\nPeople in Lift:")
                        for passenger in people_lift:
                            print(passenger)

                        # Displays the next closest floor to deliver a person.
                        deliver_moves = min(
                            [abs(int(passenger["target_floor"]) -
                                 lift_floor) for passenger in people_lift])
                        print("\nFloor Differential (Delivering):",
                              deliver_moves)

                        # Moves the lift up or down depending on the
                        # direction, and specifies the floor moved to.
                        if people_lift[0]["direction"] == "Up":
                            lift_floor += 1
                            lift_direction = "Up"
                        else:
                            lift_floor -= 1
                            lift_direction = "Down"
                        num_moves += 1
                        self.lbl_num_moves.setText("Number of Moves: "
                                                   + str(num_moves))
                        print("    Lift Floor (Delivering):", lift_floor)


class ConfigSimDialog(QDialog, QIntValidator, Ui_dialog_config_sim):
    """Contains the dialog window for creating a new lift simulation."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    main()
