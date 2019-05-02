import numpy as np

from bmtk.builder.networks import NetworkBuilder
from bmtk.builder.auxi.node_params import positions_columinar, xiter_random

# Build the networks
net = NetworkBuilder('hco_net')
Blad_afferent = NetworkBuilder('Blad_aff') # Virtual cells delivering input to Bladder
EUS_afferent = NetworkBuilder('EUS_aff') # Virtual cells delivering input to EUS


num_cells = 13
cell_prefix = "PUD_"
output_dir='network'

# IDs
# 0 - Bladder afferent
# 1 - EUS afferent
# 2 - PAG/PMC
# 3 - INm+
# 4 - INm-
# 5 - INd
# 6 - PGN
# 7 - FB
# 8 - EUS MN
# 9 - Hypo
# 10 - IMG
# 11 - MPG
connection_mappings = [
    {"source":0,
     "target":2,
     "excitatory":True,
     "weight":5.0e-03
    },
    {"source":0,
     "target":5,
     "excitatory":True,
     "weight":5.0e-03
    },
    {"source":0,
     "target":9,
     "excitatory":True,
     "weight":8.0e-03
    },
    {"source":1,
     "target":3,
     "excitatory":True,
     "weight":10.0e-03
    },
    {"source":1,
     "target":4,
     "excitatory":True,
     "weight":14.0e-03
    },
    {"source":1,
     "target":5,
     "excitatory":True,
     "weight":5.0e-03
    },
    {"source":1,
     "target":8,
     "excitatory":True,
     "weight":10.0e-03
    },
    {"source":2,
     "target":5,
     "excitatory":True,
     "weight":5.0e-03
    },
    {"source":2,
     "target":8,
     "excitatory":False,
     "weight":5.0e-03
    },
    {"source":3,
     "target":4,
     "excitatory":False,
     "weight":2.0e-03
    },
    {"source":3,
     "target":6,
     "excitatory":False,
     "weight":5.0e-03
    },
    {"source":4,
     "target":3,
     "excitatory":False,
     "weight":5.0e-03
    },
    {"source":4,
     "target":6,
     "excitatory":True,
     "weight":5.0e-03
    },
    {"source":5,
     "target":6,
     "excitatory":True,
     "weight":5.0e-03
    },
    {"source":6,
     "target":7,
     "excitatory":True,
     "weight":5.0e-03
    },
    {"source":6,
     "target":11,
     "excitatory":True,
     "weight":5.0e-03
    },
    {"source":7,
     "target":5,
     "excitatory":False,
     "weight":5.0e-03
    },
    {"source":9,
     "target":10,
     "excitatory":True,
     "weight":5.0e-03
    },
    {"source":10,
     "target":12,
     "excitatory":False,
     "weight":5.0e-03
    },
    {"source":11,
     "target":12,
     "excitatory":True,
     "weight":5.0e-03
    }
]

# Create the desired number of cells, each named "PUD_n" where "n" is the cell number
print("\nCreating Cells")
for i in range(num_cells):
    print("Building cell " + cell_prefix+str(i))
    template = 'hoc:PUD'
    if i == 4:
        template = 'hoc:PUD2'
    
    net.add_nodes(N = 1, cell_name=cell_prefix+str(i), model_type='biophysical', model_template=template, morphology='blank.swc')


# For each of the connections create a mapping
print("\nConnecting Cells")
for conn in connection_mappings:
    dynamic = 'GABA_InhToExc.json' # See files in biophys_components/synaptic_models
    if conn["excitatory"]:
        dynamic = 'AMPA_ExcToExc.json'
    
    print("Connecting cell " + cell_prefix+str(conn["source"]) + " to " + cell_prefix+str(conn["target"]) + " via " + dynamic)
    
    net.add_edges(source={'cell_name':cell_prefix+str(conn["source"])},
                    target={'cell_name':cell_prefix+str(conn["target"])},
                    syn_weight = conn["weight"],
                    model_template='Exp2Syn',
                    dynamics_params=dynamic,
                    delay=0.0,
                    threshold = 0,
                    target_sections=["soma"],
                    distance_range=[0.0, 999.0])


def target_ind_equals_source_ind(source, targets, offset=0, min_syn=1, max_syn=1):
    #creates a 1 to 1 mapping between source and destination nodes
    total_targets=len(targets)
    syns=np.zeros(total_targets)
    target_index=source['node_id']
    syns[target_index-offset]=1
    return syns

# Connect virtual cells to EUS and Bladder

Blad_afferent.add_nodes(N=1, model_type='virtual', potential='exc')
EUS_afferent.add_nodes(N=1, model_type='virtual', potential='exc')

EUS_afferent.add_edges(source = EUS_afferent.nodes(),
         target = net.nodes(cell_name='PUD_1'),
         connection_params = {},
         dynamics_params = "AMPA_ExcToExc.json",
         model_template = "Exp2Syn",
         delay = 0,
         threshold = 0,
         syn_weight = 10e-3,
         target_sections=["soma"],
         distance_range=[0.0, 999.0])


Blad_afferent.add_edges(source = Blad_afferent.nodes(),
         target = net.nodes(cell_name='PUD_0'),
         connection_params = {},
         dynamics_params = "AMPA_ExcToExc.json",
         model_template = "Exp2Syn",
         delay = 0,
         threshold = 0,
         syn_weight = 10e-3,
         target_sections=["soma"],
         distance_range=[0.0, 999.0])

print("\nBuilding network and saving to directory \"" + output_dir + "\"")
net.build()
Blad_afferent.build()
EUS_afferent.build()

net.save_nodes(output_dir=output_dir)
net.save_edges(output_dir=output_dir)

Blad_afferent.save_nodes(output_dir=output_dir)
Blad_afferent.save_edges(output_dir=output_dir)

EUS_afferent.save_nodes(output_dir=output_dir)
EUS_afferent.save_edges(output_dir=output_dir)
print("Done")
