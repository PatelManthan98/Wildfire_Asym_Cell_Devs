#!/bin/bash
# build_sim.sh — clean build script for wildfire Cell-DEVS simulation

if [ -d "build" ]; then rm -Rf build; fi
mkdir -p build
cd build || exit
cmake ..
make -j$(nproc)
cd ..
echo ""
echo "Build complete. Executable: build/wildfire_sim"
echo "Usage: ./build/wildfire_sim <scenario.json> <sim_time> [seed]"