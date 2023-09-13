from neuron import h
from STN import STN

class Network():
    # Network of N STN cells arranged in a row.
    def __init__(self, N):
        self.N = N
        self.NumGPe = 3*N
        self.create_cells(N)
        self.channel_struct()
        self.exc_connections()
        self.inhb_connections()

    def create_cells(self, N):
        self.stn_cells1 = []
        self.stn_cells2 = []

        for i in range(N):
            stn = STN(i, 0, 0, 0, 'stn')
            stn._set_position(i*30, 10, 0)
            self.stn_cells1.append(stn)
        
        for i in range(self.NumGPe):
            stn = STN(i, 0, 0, 0, 'gpe')
            stn._set_position(i*30, -20, 0)
            self.stn_cells2.append(stn)

    def channel_struct(self):
        """ Function to build all functional channels given N number of cells in the network.
        1:3 ratio between STN cells and GPe cells."""

        self.channels = [] # List of all functional channels

        for i, j in enumerate(self.stn_cells1):
            # i = position of cell (0, 1, etc)
            # j = reference to cell object

            numgpe = i * 3 # number of GPe cells

            # Create "channel" which is a list containing 1 STN cell and 3 GPe cells
            channel = [j, self.stn_cells2[(numgpe-1)%self.NumGPe], self.stn_cells2[numgpe], self.stn_cells2[(numgpe+1)%self.NumGPe]]
            self.channels.append(channel)

    def exc_connections(self):
        """Excitatory connections based on Hahn and McIntyre's functional channel paradigm.
        1 STN cell -> 3 GPe cells in its channel."""

        self.synapse_list = [] # List of synapse point processes
        self.exc_cons = [] # List of NetCon objects connecting 1 STN cell to all 3 GPe cells within its channel

        print(self.channels)

        for channel in self.channels:
            for i in channel[1:]:
                # i = GPe cell
                
                nc = h.NetCon(channel[0].soma(0.5)._ref_v, i.Syn_list[0][0], sec=channel[0].soma)
                # source = STN cell
                # target = GPe cell's inserted AMPA pointprocess (see Cell.py)

                self.exc_cons.append(nc) 

            for gpe in channel[1:4]:

                # Append AMPA pointprocess (Synapse)
                self.synapse_list.append(gpe.Syn_list[0])
        
        print(self.exc_cons)
        print(self.synapse_list)

    def inhb_connections(self):
        """Inhibitory connections as based on Hahn and McIntyre's functional channel paradigm.
        Each GPe cell inhibits 2 GPe cells within its own channel.
        Each GPe cell inhibits 4 neighbouring GPe cells.
        Each GPe cell inhibits 2 neighbouring STN cells."""

        self.inhb_cons = []

        for channel in self.channels:
            for gpe in channel[1:]: # For each GPe cell in the channel
                
                if len(self.channels) > 1: # If multiple channels exist (N_STN > 1)
                    for channel_nb in channel[1:]: # For each neighbour to the GPe cell
                        if gpe != channel_nb: # Don't connect cell to itself
                            nc = h.NetCon(gpe.soma(0.5)._ref_v, channel_nb.Syn_list[0][1], sec=gpe.soma)

                            # source = GPe cell
                            # target = Neighbouring GPe cell's GABAa pointprocess (see Cell.py)

        for netcon in self.inhb_cons:
            source, target = netcon.preseg(), netcon.postseg()
            print(source, target)
            # Print a list of each source and its target in the NetCon list to validate
            # connections are correct

        print(self.inhb_cons)
