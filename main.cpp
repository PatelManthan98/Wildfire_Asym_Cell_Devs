#include <cadmium/celldevs/asymm/coupled.hpp>
#include <cadmium/core/logger/csv.hpp>
#include <cadmium/core/simulation/root_coordinator.hpp>
#include "wildfire_cell.hpp"
#include "wildfire_state.hpp"
#include <cstdlib>
#include <ctime>
#include <iostream>

using namespace cadmium::celldevs;

std::shared_ptr<AsymmCell<WildfireCellState, double>> addCell(
    const std::string& cellId,
    const std::shared_ptr<const AsymmCellConfig<WildfireCellState, double>>& cfg
) {
    return std::make_shared<WildfireAsymmCell>(cellId, cfg);
}

int main(int argc, char** argv) {
    std::string config = (argc > 1) ? argv[1] : "scenario.json";
    double sim_time    = (argc > 2) ? std::stod(argv[2]) : 500.0;
    unsigned int seed  = (argc > 3) ? static_cast<unsigned>(std::stoul(argv[3]))
                                    : static_cast<unsigned>(time(nullptr));
    srand(seed);

    std::cout << "Scenario : " << config   << "\n"
              << "Sim time : " << sim_time << "\n"
              << "RNG seed : " << seed     << "\n";

    auto model = std::make_shared<AsymmCellDEVSCoupled<WildfireCellState, double>>(
        "wildfire", addCell, config);
    model->buildModel();

    auto root   = cadmium::RootCoordinator(model);
    auto logger = std::make_shared<cadmium::CSVLogger>("grid_log.csv", ";");
    root.setLogger(logger);
    root.start();
    root.simulate(sim_time);
    root.stop();

    std::cout << "Done. Log: grid_log.csv\n";
    return 0;
}
