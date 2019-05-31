import os
import numpy as np

def constant_rate_input(filename,input_dir,hz,start,duration,cells):
    
    stims = {}   
    interval = 1000.0/hz
    for cell in cells:
        spk = start
        spike_ints = np.random.poisson(interval,100)
        for spike_int in spike_ints:
            if not stims.get(cell):
                stims[cell] = []
            if spk <= duration:
                spk = spk + spike_int
                stims[cell].append(spk)
    
    with open(os.path.join(input_dir,filename),'w') as file:
        file.write('gid spike-times\n')
        for key, value in stims.items():
            file.write(str(key)+' '+','.join(str(x) for x in value)+'\n')   
    return


def abrupt_changing_rates(filename,input_dir,hz,start,end,cells):
    print('len(hz)=',len(hz))
    stims = {}   
    for i in np.arange(0,len(hz)):
        interval = 1000.0/hz[i]
        for cell in cells:
            spk = start[i]
            spike_ints = np.random.poisson(interval,100)
            for spike_int in spike_ints:
                if not stims.get(cell):
                    stims[cell] = []
                spk = spk + spike_int
                if spk <= end[i]:
                    stims[cell].append(spk)
    
    with open(os.path.join(input_dir,filename),'w') as file:
        file.write('gid spike-times\n')
        for key, value in stims.items():
            file.write(str(key)+' '+','.join(str(x) for x in value)+'\n')   
    return

def ramp_rate_input(filename,input_dir,hz,start,duration,cells,slope):
    
    stims = {}
    # Every 1 second, raise rate by factor of slope
    for cell in cells:
        spk = start
        for i in np.arange(1,duration):
            interval = 1000.0/(i*hz/slope)
            print("interval: {}".format(interval))
            spike_int = np.random.poisson(interval)
            if not stims.get(cell):
                stims[cell] = []
            if spk <= duration:
                spk = spk + spike_int
                stims[cell].append(spk)
    
    with open(os.path.join(input_dir,filename),'w') as file:
        file.write('gid spike-times\n')
        for key, value in stims.items():
            file.write(str(key)+' '+','.join(str(x) for x in value)+'\n')   
        return

if __name__ == '__main__':
    
    #Change these for your needs
    start = 0 #ms
    duration = 6000 #ms

    output_file = 'EUS_spikes.csv'
    input_dir = './'
    #hz = 3.0

    slope = 4
    cells = [0,1,2,3,4,5,6,7,8,9]
    hz = [15.0,3.0]
    start = [0.0,5000.0]
    end= [5000.0,6000.0]
    abrupt_changing_rates(output_file,input_dir, hz, start,end, cells)
    #ramp_rate_input(output_file,input_dir, hz, start, duration, cells, slope)
