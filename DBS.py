from neuron import h, gui
from math import sqrt, pi
import numpy as np
from scipy import signal

def generate_DBS_signal(start_time, stop_time, dt
                        , amplitude, freq, pulse_width, offset, r
                        ):
    
    times  = np.round(np.arange(start_time, stop_time, dt), 2)
    tmp = np.arange(0, stop_time - start_time, dt)/1000.0

    T = (1.0/freq)*1000.0
    duty = (pulse_width/T)
            
    dbs_signal = offset + r * (1.0+signal.square(2.0 * pi * freq * tmp, duty=duty))/2.0
    dbs_signal[-1] = 0.0
    
    dbs_signal *= amplitude

    return dbs_signal, times
# class DBS:
#     def __init__(self, network, x, y, z):
#         self.elec_x = x
#         self.elec_y = y
#         self.elec_z = z

#         self.network = network

    # def ext_voltage(self):
    #     self.v_ext = []
    #     sigma = 0.3

    #     x3d = h.x3d
    #     y3d = h.y3d
    #     z3d = h.z3d

    #     elec_x = self.elec_x
    #     elec_y = self.elec_y
    #     elec_z = self.elec_z

    #     for cell in self.network:
    #         dbs_Stim = h.Ipulse2(cell.soma(0.5))
    #         dbs_Stim.amp = 1
    #         dbs_Stim.dur = 200
    #         dbs_Stim.per = 100
    #         dbs_Stim.delay = 50

    #         x = (x3d(0, sec=cell.soma) + x3d(1, sec=cell.soma)) / 2
    #         y = (y3d(0, sec=cell.soma) + y3d(1, sec=cell.soma)) / 2
    #         z = (z3d(0, sec=cell.soma) + z3d(1, sec=cell.soma)) / 2

    #         dis = sqrt(
    #             (elec_x - x) ** 2 +
    #             (elec_y - y) ** 2 + 
    #             (elec_z - z) ** 2
    #         )
