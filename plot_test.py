from bmtk.analyzer.cell_vars import plot_report
from bmtk.analyzer.spike_trains import raster_plot


plot_report(config_file="simulation_config.json")
raster_plot(cells_file="network/inputPUD_hco_net_edges.h5", cell_models_file="network/inputPUD_hco_net_edge_types.csv", spikes_file="output/spikes.h5")
