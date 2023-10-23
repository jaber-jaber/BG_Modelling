from neuron import h, gui
from math import sqrt, pi
import numpy as np
from scipy import signal

""" Function to generate DBS square waveform. 
DBS signal is fed into STIM point process in STN.py

"""

def generate_DBS_signal(start_time, stop_time, dt
                        , amplitude, freq, pulse_width, offset, r
                        ):
    
    times  = np.round(np.arange(start_time, stop_time, dt), 2)
    tmp = np.arange(0, stop_time - start_time, dt)/1000.0

    T = (1.0/freq)*1000.0
    duty = (pulse_width/T)
            
    dbs_signal = offset + r * (1.0+signal.square(2.0 * pi * freq * tmp, duty=duty))/2.0
    # r is amplitude scaling by distance from stimulation electrode.
    dbs_signal[-1] = 0.0
    
    dbs_signal *= amplitude

    return dbs_signal, times