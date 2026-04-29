set -e
 
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
 
SCENARIOS=(
    calm
    windy
    firebreak
    firebreak_spot
    urban
    fortmcmurray_nospot
    fortmcmurray_spot
)
 
SIM_TIME=500
SEED=42
 
# ── Step 1: build the simulator if the binary is missing ─────────────────────
if [ ! -x "$ROOT/build/wildfire_sim" ]; then
    echo "build/wildfire_sim not found — building now..."
    bash "$ROOT/build_sim.sh"
    echo ""
fi
 
# ── Step 2: generate scenario JSONs if any are missing ───────────────────────
MISSING=0
for NAME in "${SCENARIOS[@]}"; do
    [ ! -f "$ROOT/scenarios/scenario_${NAME}.json" ] && MISSING=$((MISSING+1))
done
if [ "$MISSING" -gt 0 ]; then
    echo "$MISSING scenario JSON(s) missing — running generate_scenarios.py..."
    python3 "$ROOT/generate_scenarios.py"
    echo ""
fi
 
mkdir -p "$ROOT/results"
 
echo "=============================================="
echo "  Wildfire Cell-DEVS — Running all scenarios"
echo "  sim_time=$SIM_TIME   seed=$SEED"
echo "=============================================="
 
# ── Step 3: simulate each scenario ───────────────────────────────────────────
for NAME in "${SCENARIOS[@]}"; do
    JSON="$ROOT/scenarios/scenario_${NAME}.json"
    LOG="$ROOT/results/grid_log_${NAME}.csv"
 
    if [ ! -f "$JSON" ]; then
        echo "  [SKIP] $NAME — $JSON not found"
        continue
    fi
 
    echo ""
    echo "--- $NAME ---"
    echo "  input  : $JSON"
    echo "  output : $LOG"
 
    "$ROOT/build/wildfire_sim" "$JSON" "$SIM_TIME" "$SEED"
 
    # simulator writes grid_log.csv to the working directory
    if [ -f "$ROOT/grid_log.csv" ]; then
        mv "$ROOT/grid_log.csv" "$LOG"
    elif [ -f "grid_log.csv" ]; then
        mv "grid_log.csv" "$LOG"
    else
        echo "  WARNING: grid_log.csv not found after running $NAME"
    fi
done
 
# ── Step 4: summary ───────────────────────────────────────────────────────────
echo ""
echo "=============================================="
echo "  Done. CSV logs:"
ls -1 "$ROOT/results/"grid_log_*.csv 2>/dev/null | sed 's|^|    |'
echo ""
echo "  To produce GIF / MP4 animations run:"
echo "      python3 visualize_wildfire.py"
echo "=============================================="
