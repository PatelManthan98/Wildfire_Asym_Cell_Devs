Asymmetric Cell-DEVS Wildfire Simulation

A physics-informed wildfire spread model built using the Asymmetric Cell-DEVS formalism and executed on the Cadmium v2 discrete-event simulation engine.
The model integrates heterogeneous terrain, wind forcing, fuel structure, and probabilistic ember spotting to reproduce real wildfire behavior.

--------------------------------------------------

KEY FEATURES

- Asymmetric Topology:
  Wind and slope effects embedded directly into directional vicinity weights.

- Ember Spotting:
  Sparse long-range edges simulate river-crossing and extreme-wind ignition.

- Real Geospatial Data:
  NRCan CDEM — elevation & slope
  NLCMS-2015 — land-cover & fuel classification

- High-Performance Execution:
  Built on Cadmium v2 for asynchronous, event-driven simulation.

--------------------------------------------------

PREREQUISITES & ENVIRONMENT SETUP

This project was developed on the devsim server.
A Python virtual environment is used to avoid system-level dependency issues.

1. Python Environment

Create virtual environment:
python3 -m venv .venv

Activate environment:
source .venv/bin/activate

Install visualization dependencies:
pip install numpy matplotlib pandas

--------------------------------------------------

RUNNING THE SIMULATION

From the project root:

Usage:
./build/wildfire_sim <scenario_file> <time_steps> <seed>

Example:
./build/wildfire_sim scenario.json 500 42

Parameters:
scenario.json — grid, fuel, weather, and topology configuration
500 — total simulation steps
42 — random seed for reproducibility

--------------------------------------------------

VISUALIZATION & ANALYSIS

After simulation, a grid_log.csv file is generated in /build.

To generate outputs:

Ensure virtual environment is active:
source .venv/bin/activate

Run visualization:
python3 visualize_wildfire.py

Outputs include:
- wildfire_spread.gif — animated fire progression
- PNG charts:
  • rate of spread
  • active burning cells
  • cumulative burn area

--------------------------------------------------

VALIDATED SCENARIOS

Scenario 1 — Calm:
Isotropic spread under no-wind conditions

Scenario 3 — Firebreak:
Complete containment by a river (no spotting)

Scenario 4 — Moderate Wind:
Spotting occurs but cannot sustain a breach

Scenario 7 — Fort McMurray:
Reproduces the 2016 Horse River breach under 65 km/h winds

--------------------------------------------------

AUTHOR

Manthan Patel
Department of Systems and Computer Engineering
Carleton University
