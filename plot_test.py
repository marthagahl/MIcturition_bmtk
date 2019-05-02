from bmtk.analyzer.cell_vars import plot_report
from bmtk.analyzer.spike_trains import raster_plot
import pandas as pd
import matplotlib.pyplot as plt
from bmtk.utils.cell_vars import CellVarsFile
import numpy as np
from bmtk.analyzer.cell_vars import _get_cell_report
#plot_report(config_file="simulation_config.json")

config_file = "simulation_config.json"
report_name = None
report_name, report_file = _get_cell_report(config_file, report_name)


var_report = CellVarsFile(report_file)
time_steps = var_report.time_trace

# Plot Inputs: bladder afferent, EUS afferent, and PAG afferent
plt.figure()
lab = ['bladder aff.','EUS aff.', 'PAG aff.']
for i in np.arange(1,4):
    plt.subplot(3,1,i)
    plt.plot(time_steps,var_report.data(gid=i-1,var_name='v'))
    plt.ylim(-80,40)
    plt.ylabel(lab[i-1])

# Plot Outputs: bladder motor neuron and EUS motor neuron
plt.figure()
lab = ['bladder MN','EUS MN']
plt.subplot(2,1,1)
plt.plot(time_steps,var_report.data(gid=12,var_name='v'))
plt.ylim(-80,40)
plt.ylabel(lab[0])

plt.subplot(2,1,2)
plt.plot(time_steps,var_report.data(gid=8,var_name='v'))
plt.ylim(-80,40)
plt.ylabel(lab[1])

# Plot "filter" cells + INd
plt.figure()
lab = ['low pass','high pass','INd']
plt.subplot(3,1,1)
plt.plot(time_steps,var_report.data(gid=3,var_name='v'))
plt.ylim(-80,40)
plt.ylabel(lab[0])

plt.subplot(3,1,2)
plt.plot(time_steps,var_report.data(gid=4,var_name='v'))
plt.ylim(-80,40)
plt.ylabel(lab[1])

plt.subplot(3,1,3)
plt.plot(time_steps,var_report.data(gid=5,var_name='v'))
plt.ylim(-80,40)
plt.ylabel(lab[2])

# Plot the rest
plt.figure()
lab = ['PGN','FB','Hypo','IMG','MPG']
gids = [6,7,9,10,11]
for i in np.arange(0,len(lab)-1):
    plt.subplot(4,1,i+1)
    plt.plot(time_steps,var_report.data(gid=gids[i],var_name='v'))
    plt.ylim(-80,40)
    plt.ylabel(lab[i])


# Plot spike raster
df = pd.read_csv("output/spikes.csv",delimiter=' ')
rast = df.values
plt.figure()
plt.plot(rast[:,0],rast[:,1],'b.')
plt.show()
#raster_plot(cells_file="network/inputPUD_hco_net_edges.h5", cell_models_file="network/inputPUD_hco_net_edge_types.csv", spikes_file="output/spikes.h5")
