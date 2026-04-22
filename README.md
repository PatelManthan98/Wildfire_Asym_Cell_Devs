**`Asymmetric Cell‑DEVS Wildfire Spread Simulation
A Terrain‑Aware, Physics‑Driven Wildfire Modeling Framework`**
📖 Project Overview
This project implements an advanced wildfire spread simulator based on the Asymmetric Cell‑DEVS formalism. Unlike traditional symmetric grid models such as Cellular Automata, this simulator assigns each cell its own unique neighborhood, where every neighbor connection carries a directional weight. These weights encode real physical influences, enabling the model to reproduce complex wildfire behavior with high fidelity.

The directional weights are pre‑computed from real geospatial and environmental data. Wind vectors are derived from the May 2016 Fort McMurray Horse River wildfire weather conditions. Slope gradients are extracted from Digital Elevation Models (DEM), and fuel adjacency incorporates land‑cover classification to represent rivers, roads, forests, grasslands, and urban zones. This results in a GIS‑inspired, physics‑informed wildfire simulation capable of modeling asymmetric spread, firebreaks, and long‑range ember spotting.

🚀 Key Features
Asymmetric Topology Engine
The simulator replaces the traditional Moore neighborhood with a weighted, directed graph, where each edge represents a unique physical influence. This allows the model to capture wind‑driven spread, slope‑induced acceleration, and directional fuel transitions.

Fort McMurray 2016 Case Study
The system is validated against the real Horse River wildfire, using historical weather data:
65 km/h south‑west winds, 32°C temperature, and 13% relative humidity.
The model reproduces the documented ember‑driven crossing of the Athabasca River.

GIS‑Inspired Scenario Pipeline
A Python‑based generator mimics a QGIS workflow, producing asymmetric JSON configurations from DEM and land‑cover data. This pipeline automates the creation of realistic wildfire scenarios.

Event‑Driven Simulation Efficiency
Built on Cadmium v2, the simulator leverages discrete‑event execution for high performance, enabling large‑scale wildfire modeling with minimal computational overhead.

🛠️ Installation & Build
1. Prerequisites
Ensure the following tools are installed:

GCC 13+ (C++20 support required)

CMake 3.10+

Cadmium v2 (included as a submodule or cloned manually)

2. Setup Dependencies
Clone the Cadmium v2 framework into the project root:

bash
git clone https://github.com/SimulationEverywhere/cadmium_v2.git cadmium_v2
3. Compilation
Use the provided build script:

bash
chmod +x build_sim.sh
./build_sim.sh
🏃 Running the Simulation
1. Generate Scenarios
Run the Python script to create asymmetric neighborhood files:

bash
python3 generate_scenarios.py
This produces five scenarios in the scenarios/ directory:

calm

windy

firebreak

urban

fortmcmurray

2. Execute All Models
Run the batch simulation script:

bash
chmod +x run_all_scenarios.sh
./run_all_scenarios.sh
All logs are saved automatically.

📊 Results and Visualization
Simulation outputs are stored as CSV logs in the results/ directory.
Visualization scripts interpret the grid states using the following color scheme:

🟩 Green: Unburned fuel

🟥 Red: Actively burning

⬛ Black: Burned out (ash)

⬜ Grey: Non‑combustible terrain (rivers, roads, water bodies)

These visualizations allow you to observe directional spread, firebreak interactions, and ember spotting behavior.

📂 Project Structure
Code
include/
   ├── wildfire_cell.hpp        # Asymmetric Cell-DEVS cell definition
   ├── wildfire_state.hpp       # State structure for each cell

main.cpp                        # AsymmCellDEVSCoupled model entry point
generate_scenarios.py           # GIS-inspired scenario generator
run_all_scenarios.sh            # Batch simulation runner
build_sim.sh                    # Build script
results/                        # Simulation logs and outputs
scenarios/                      # Generated asymmetric JSON scenarios
Wildfire_CellDEVS_Report.pdf    # Full IEEE-style 15–20 page term paper
