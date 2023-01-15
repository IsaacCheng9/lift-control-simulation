# Lift Control Simulation

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A desktop application developed in Python with PyQt6 to manage and simulate lift
control under various configurations.

I optimised a custom algorithm for efficiency in distance travelled by the lift.
This algorithm achieves up to 82.5% reduction in distance travelled compared to
the naive algorithm benchmark, outperforming the 25% reduction claimed by the
destination dispatch technique.

For more information about this, see the design
document at [docs/Lift Control - Design Document.pdf](<docs/Lift Control - Design Document.pdf>).
It contains an explanation of the algorithm and performance analysis.

## Visuals

![Running the simulation](https://i.imgur.com/K6YzssY.gif)

## Installation

### Operating System

Compatible with:

- Windows
- MacOS
- Linux

### Python Version

Python 3.7.0 or later is required for this software to run. It can be downloaded
from [Python's website here.](https://www.python.org/getit/)

### Running the Application

To run the application, you should follow the following steps:

1. Clone this GitHub repository.
2. Ensure that you're in the root directory: `lift-control-simulation`
3. Install the required Python libraries: `pip install -r requirements.txt`
4. Run the application with the command: `python -m src.app`

## Usage

### Configuration

The user is able to configure any number of floors, number of people, lift
capacity, and the delay of intervals in the user interface.

### Simulation

Their simulation can be visually displayed for up to five floors. For more than
five floors, the application provides a non-visual display. In both cases, the
user can run their simulation with either the naive mechanical lift (the
benchmark) algorithm, or my improved lift algorithm.

The configured simulation remains the same until the user generates a new
simulation, or changes the configuration settings. This enables the user to
directly compare how the improved algorithm compares to the naive algorithm.

### Logging

The application prints a temporary log of the simulations in the terminal. It
records the simulation configuration, people generated, movements of the lift,
people pending (if applicable), people in the lift, people delivered, and an
overview of people after the simulation is complete.
