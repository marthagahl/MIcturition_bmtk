import numpy as np

from bmtk.builder.networks import NetworkBuilder
from bmtk.builder.auxi.node_params import positions_columinar, xiter_random

net = NetworkBuilder('hco_net')
inputPUD = NetworkBuilder('inputPUD')

num_cells = 12
cell_prefix = "PUD_"
output_dir='network'

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
     "weight":5.0e-03
    },
    {"source":1,
     "target":3,
     "excitatory":True,
     "weight":5.0e-03
    },
    {"source":1,
     "target":4,
     "excitatory":True,
     "weight":5.0e-03
    },
    {"source":1,
     "target":5,
     "excitatory":True,
     "weight":5.0e-03
    },
    {"source":1,
     "target":8,
     "excitatory":True,
     "weight":5.0e-03
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
     "weight":5.0e-03
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
                    target_sections=["soma"],
                    distance_range=[0.0, 999.0])


def target_ind_equals_source_ind(source, targets, offset=0, min_syn=1, max_syn=1):
    #creates a 1 to 1 mapping between source and destination nodes
    total_targets=len(targets)
    syns=np.zeros(total_targets)
    target_index=source['node_id']
    syns[target_index-offset]=1
    return syns

inputPUD.add_nodes(N=1, model_type='virtual', pop_name='inp')
inputPUD.add_nodes(N=1, model_type='virtual', pop_name='inp')

conn=inputPUD.add_edges(target=net.nodes(model_template='hoc:PUD'),
        source = {'pop_name': 'inp'},
        iterator = 'one_to_all',
        connection_rule = target_ind_equals_source_ind,
        connection_params = {},
        dynamics_params = "AMPA_ExcToExc.json",
        model_template = "Exp2Syn",
        delay = 0,
        syn_weight = 1,
        target_sections=["soma"],
        distance_range=[0.0, 999.0])

print("\nBuilding network and saving to directory \"" + output_dir + "\"")
net.build()
inputPUD.build()
net.save_nodes(output_dir=output_dir)
net.save_edges(output_dir=output_dir)
inputPUD.save_nodes(output_dir=output_dir)
inputPUD.save_edges(output_dir=output_dir)
print("Done")
