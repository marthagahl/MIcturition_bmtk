import os
import numpy as np

def generate_input(filename,input_dir,hz,start,duration,cells,noise):
    
    step = int(1000/hz)
   

    stims = {}
    
    for cell in cells:
        intvl = np.random.poisson(step,size=1000)
        spike_time = start
        for i in np.arange(start,start+duration,step):
            spike_time = spike_time + intvl[i]
            if not stims.get(cell):
                stims[cell] = []
            stims[cell].append(spike_time)
    
    with open(os.path.join(input_dir,filename),'w') as file:
        file.write('gid spike-times\n')
        for key, value in stims.items():
            file.write(str(key)+' '+','.join(str(x) for x in value)+'\n')   
    return

if __name__ == '__main__':
    
    #Change these for your needs
    start = 0 #ms
    duration = 1000 #ms
    hz = 80
    output_file = 'spikes_{}.csv'.format(hz)
    input_dir = 'input'
    
    cells = [0]
    noise = 1
    
    generate_input(output_file,input_dir, hz, start, duration, cells, noise)
