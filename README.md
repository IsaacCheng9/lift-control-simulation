# lift-control
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