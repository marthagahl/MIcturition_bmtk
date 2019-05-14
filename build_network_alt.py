from bmtk.builder import NetworkBuilder
import numpy as np
from bmtk.builder.auxi.node_params import positions_cuboid, positions_list

np.random.seed(12366)

# Initialize our network
net = NetworkBuilder("SPWR_biophysical")

# Create the possible x,y,z coordinates
xside_length = 1400; yside_length = 1400; height = 200; min_dist = 20;
x_grid = np.arange(0,xside_length+min_dist,min_dist)
y_grid = np.arange(0,yside_length+min_dist,min_dist)
z_grid = np.arange(0,height+min_dist,min_dist)
xx, yy, zz = np.meshgrid(x_grid, y_grid, z_grid)
pos_list = np.vstack([xx.ravel(), yy.ravel(), zz.ravel()]).T

# Number of cells in each population
numPN_A = 4115
numPN_C = 4115
numPV = 1646
numAAC = 411

###################################################################################
####################################Pyr Type A#####################################

# Pick coordinates
inds = np.random.choice(np.arange(0,np.size(pos_list,0)),numPN_A,replace=False)
pos = pos_list[inds,:]

# Add a population of numPN_A nodes (all of which share model_type, dynamics_params, etc.)
net.add_nodes(N=numPN_A, pop_name='PyrA',
              positions=positions_list(positions=pos),
              mem_potential='e',
              model_type='biophysical',
              model_template='ctdb:Biophys1.hoc',
              model_processing='aibs_perisomatic',
              dynamics_params='472363762_fit.json',
              morphology='Scnn1a_473845048_m.swc')

##################################################################################
###################################Pyr Type C#####################################

# Get rid of coordinates already used
pos_list = np.delete(pos_list,inds,0)

# Pick new coordinates
inds = np.random.choice(np.arange(0,np.size(pos_list,0)),numPN_C,replace=False)
pos = pos_list[inds,:]

# Add a population of numPN_C nodes (all of which share model_type, dynamics_params, etc.)
net.add_nodes(N=numPN_C, pop_name='PyrC',
              positions=positions_list(positions=pos),
              mem_potential='e',
              model_type='biophysical',
              model_template='ctdb:Biophys1.hoc',
              model_processing='aibs_perisomatic',
              dynamics_params='472363762_fit.json',
              morphology='Scnn1a_473845048_m.swc')

#################################################################################
###########################Fast - spiking PV ints################################

# Get rid of coordinates already used
pos_list = np.delete(pos_list,inds,0)

# Pick new coordinates
inds = np.random.choice(np.arange(0,np.size(pos_list,0)),numPV,replace=False)
pos = pos_list[inds,:]

# Add a population of numPV nodes
net.add_nodes(N=numPV, pop_name='PV',
              positions=positions_list(positions=pos),
              mem_potential='e',
              model_type='biophysical',
              model_template='ctdb:Biophys1.hoc',
              model_processing='aibs_perisomatic',
              dynamics_params='472363762_fit.json',
              morphology='Scnn1a_473845048_m.swc')

#################################################################################
############################# Chandelier ########################################

# Get rid of coordinates already used
pos_list = np.delete(pos_list,inds,0)

# Pick new coordinates
inds = np.random.choice(np.arange(0,np.size(pos_list,0)),numAAC,replace=False)
pos = pos_list[inds,:]

# Add a population of numPV nodes
net.add_nodes(N=numAAC, pop_name='AAC',
              positions=positions_list(positions=pos),
              mem_potential='e',
              model_type='biophysical',
              model_template='ctdb:Biophys1.hoc',
              model_processing='aibs_perisomatic',
              dynamics_params='472363762_fit.json',
              morphology='Scnn1a_473845048_m.swc')

################################################################################
############################# BACKGROUND INPUTS ################################

# External inputs
thalamus = NetworkBuilder('mthalamus')
thalamus.add_nodes(N=numPN_A+numPN_C,
                   pop_name='tON',
                   potential='exc',
                   model_type='virtual')

##############################################################################
############################## CONNECT CELLS #################################
from bmtk.builder.auxi.edge_connectors import distance_connector, connect_random

def dist_perc_conn(src,trg,min_dist,max_dist,min_syns=1,max_syns=2,perc=0.2):
    if src.node_id==trg.node_id:
        return None
    else:
        src_pos = src['positions']
        trg_pos = trg['positions']

        dist = np.sqrt((src_pos[0]-trg_pos[0])**2+(src_pos[1]-trg_pos[1])**2+(src_pos[2]-trg_pos[2])**2)

        if dist<max_dist and dist>min_dist and np.random.uniform()<perc:
            print('connecting cell {} to {}'.format(src.node_id,trg.node_id))
            print('positions: ',src_pos, trg_pos)
            print('distance: ',dist)
            tmp_syn = np.random.randint(min_syns,max_syns)
        else:
            tmp_syn = 0
        return tmp_syn

# Create connections between Pyr --> PV cells
net.add_edges(source={'pop_name': ['PyrA','PyrC']}, target={'pop_name': 'PV'},
              connection_rule=dist_perc_conn,
              connection_params={'min_dist':0,'max_dist':300,'min_syns':1,'max_syns':2,'perc':0.2},
              syn_weight=5.0e-03,
              dynamics_params='AMPA_ExcToExc.json',
              model_template='Exp2Syn',
              distance_range=[0.0, 300.0],
              target_sections=['somatic'],
              delay=2.0)


net.build()
net.save_nodes(output_dir='network')
net.save_edges(output_dir='network')


# Create connections between "thalamus" and Pyramidals
# First define the connection rule
def one_to_one(source, target):
    
    sid = source.node_id
    tid = target.node_id
    if sid == tid:
	print("connecting cell {} to {}".format(sid,tid))
        tmp_nsyn = 1
    else:
        return None

    return tmp_nsyn

thalamus.add_edges(source=thalamus.nodes(), target=net.nodes(pop_name='PyrA'),
                   connection_rule=one_to_one,
                   syn_weight=5.0e-03,
                   target_sections=['somatic'],
                   delay=2.0,
                   distance_range=[0.0, 300.0],
                   dynamics_params='AMPA_ExcToExc.json',
                   model_template='Exp2Syn')

thalamus.add_edges(source=thalamus.nodes(), target=net.nodes(pop_name='PyrC'),
                   connection_rule=one_to_one,
                   syn_weight=5.0e-03,
                   target_sections=['somatic'],
                   delay=2.0,
                   distance_range=[0.0, 300.0],
                   dynamics_params='AMPA_ExcToExc.json',
                   model_template='Exp2Syn')

# Build and save our network

thalamus.build()
thalamus.save_nodes(output_dir='network')
thalamus.save_edges(output_dir='network')


from bmtk.utils.spike_trains import SpikesGenerator

sg = SpikesGenerator(nodes='network/mthalamus_nodes.h5', t_max=60.0)
sg.set_rate(15.0)
sg.save_csv('thalamus_spikes.csv', in_ms=True)
