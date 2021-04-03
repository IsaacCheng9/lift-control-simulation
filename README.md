# lift-control-simulation

A system developed in Python to manage and simulate lift control in various
scenarios.

It uses a priority queue and a custom-made algorithm, optimised for efficiency
in distance travelled by the lift. This algorithm achieves up to 82.5%
reduction in distance travelled by the lift compared to the naive algorithm,
dwarfing the 25% reduction claimed by the destination dispatch technique.

## Visuals

![Running the simulation](https://i.imgur.com/K6YzssY.gif)

## Installation

### Python Version

This application has been developed and tested to work on Python 3.7 and
onwards.

### Python Libraries

The simulation relies on PyQt5 for the user interface and simulation, so you
must `pip install pyqt5` if you do not already have it installed.

## Usage

### Configuration

The user is able to configure any number of floors, number of people, lift
capacity, and the delay of intervals in the user interface.

### Simulation

Their simulation can be visually displayed for up to five floors. For more than
five floors, a non-visual display is provided. In both cases, the user can run
their simulation with either the naive, mechanical lift algorithm, or my
improved lift algorithm.

The configured simulation remains the same until the user generates a new
simulation, or changes the configuration settings. This enables the user to
directly compare how the improved algorithm compares to the naive algorithm.

### Logging

A temporary log of the simulations is also printed in the terminal. It records
the simulation configuration, people generated, movements of the lift, people
pending (if applicable), people in the lift, people delivered, and an overview
of people after the simulation is complete.