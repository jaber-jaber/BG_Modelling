from neuron import h

class Cell():
    # Cell template. All other cells in this model will inherit from Cell.

    def __init__(self):

        # Cell in 3D space
        self.x = 0
        self.y = 0
        self.z = 0

        # Defining the soma, array of synapses and "Iscale"
        
        self.soma = None
        self.Syn_list = []
        self.Iscale = 0

        # Cell methods (equivalent of procs in HOC)
        self.create_sections()
        self.define_biophysics()
        self.define_geometry()
        self.build_subsets

    def create_sections(self):
        # Sections in the form of:
        # h.Section(name='soma', cell=self)
        # or h.Section(name='dendrite', cell=self)

        
        raise NotImplementedError("Sections have not been created.")

    def define_geometry(self):
        # Set the 3D geometry of the cell.
        raise NotImplementedError("Cell geometries have not been created.")

    def define_biophysics(self):
        # Define biophysics of the cell (assign membrane properties)
        raise NotImplementedError("Biophysics of the cell have not been defined.")

    def self_con(self, threshold=10):
        netcon = h.NetCon(self.soma(0.5)._ref_v, self.soma)
        netcon.threshold = threshold
        return netcon

    