from neuron import h
from STN import STN

class Network():
    # Network of N cells arranged in a row.
    def __init__(self, N):
        # create_cells(self, N)
        # connect cells(self)
        self.create_cells(N)

    def create_cells(self, N):
        self.stn_cells1 = []
        self.stn_cells2 = [] # Replace with GPe cells
        for i in range(N):
            stn = STN(i, 0, 0, 0)
            stn._set_position(i*30, 10, 0)
            self.stn_cells1.append(stn)
        
        for i in range(N):
            stn = STN(i, 0, 0, 0)
            stn._set_position(i*30, -20, 0)
            self.stn_cells2.append(stn)