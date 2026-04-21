#!/bin/bash
# run_all_scenarios.sh — Build, run all 5 scenarios, and visualize
set -e
echo "=== Building ==="
bash build_sim.sh
mkdir -p results

for NAME in calm windy firebreak urban fortmcmurray; do
    echo ""; echo "=== Running: $NAME ==="
    cd build
    ./wildfire_sim "../scenarios/scenario_${NAME}.json" 500 42
    mv grid_log.csv "../results/grid_log_${NAME}.csv"
    cd ..
done

echo ""; echo "=== Visualizing ==="
for NAME in calm windy firebreak urban fortmcmurray; do
    LOG_FILE="results/grid_log_${NAME}.csv" SCENARIO="$NAME" python3 visualize_wildfire.py
done
echo ""; echo "=== Done. Results in results/ ==="
ls results/*.gif results/*.png