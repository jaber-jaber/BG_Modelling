from neuron import h
from STN import STN

class Network():
    # Network of N cells arranged in a row.
    def __init__(self, N):
        self.N = N
        self.NumGPe = 3*N
        self.create_cells(N)
        self.channel_struct()
        self.exc_connections()

    def create_cells(self, N):
        self.stn_cells1 = []
        self.stn_cells2 = [] # Replace with GPe cells
        for i in range(N):
            stn = STN(i, 0, 0, 0, 'stn')
            stn._set_position(i*30, 10, 0)
            self.stn_cells1.append(stn)
        
        for i in range(self.NumGPe):
            stn = STN(i, 0, 0, 0, 'gpe')
            stn._set_position(i*30, -20, 0)
            self.stn_cells2.append(stn)

    def channel_struct(self):
        N = self.N
        self.channels = []

        for i, j in enumerate(self.stn_cells1):
            numgpe = i * 3
            channel = [j, self.stn_cells2[(numgpe-1)%self.NumGPe], self.stn_cells2[numgpe], self.stn_cells2[(numgpe+1)%self.NumGPe]]
            self.channels.append(channel)

    def exc_connections(self):
        N = self.N
        self.synapse_list = []
        self.exc_cons = []

        print(self.channels)

        for channel in self.channels:
            for i in channel[1:]:
                nc = h.NetCon(channel[0].soma(0.5)._ref_v, i.Syn_list[0], sec=channel[0].soma)
                nc.weight[0] = 0.01
                nc.delay = 500
                self.exc_cons.append(nc)

            for gpe in channel[1:4]:
                self.synapse_list.append([gpe.Syn_list[0]])

        
        print(self.exc_cons)
        print(self.synapse_list)

        