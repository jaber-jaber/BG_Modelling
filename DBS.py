from neuron import h, gui
from math import sqrt, pi

class DBS:
    def __init__(self, network, x, y, z):
        self.elec_x = x
        self.elec_y = y
        self.elec_z = z

        self.network = network

    def ext_voltage(self):
        self.v_ext = []
        sigma = 0.3

        x3d = h.x3d
        y3d = h.y3d
        z3d = h.z3d

        elec_x = self.elec_x
        elec_y = self.elec_y
        elec_z = self.elec_z

        for cell in self.network:
            dbs_Stim = h.Ipulse2(cell.soma(0.5))
            
            x = (x3d(0, sec=cell.soma) + x3d(1, sec=cell.soma)) / 2
            y = (y3d(0, sec=cell.soma) + y3d(1, sec=cell.soma)) / 2
            z = (z3d(0, sec=cell.soma) + z3d(1, sec=cell.soma)) / 2

            dis = sqrt(
                (elec_x - x) ** 2 +
                (elec_y - y) ** 2 + 
                (elec_z - z) ** 2
            )

            vext =  1 / (4 * pi * dis * sigma)
            self.v_ext.append(vext)
