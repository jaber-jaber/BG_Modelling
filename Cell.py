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

        # Cell methods (equivalent of procs in HOC)
        self.create_sections()
        self.define_biophysics()
        self.define_geometry()

    def create_sections(self):
        # Sections in the form of:
        # h.Section(name='soma', cell=self)
        # or h.Section(name='dendrite', cell=self)

        
        raise NotImplementedError("Sections were not created.")

    def define_geometry(self):
        # Set the 3D geometry of the cell.
        raise NotImplementedError("Cell geometries have not been created.")

    def define_biophysics(self):
        # Define biophysics of the cell (assign membrane properties)
        raise NotImplementedError("Biophysics of the cell have not been defined.")

    def get_spikes(self):
        spiketrain = []
        return spiketrain.netconvecs_to_listoflists(self.t_vec, self.id_vec)

    def current_clamp(self):
        stim = h.IClamp(self.soma(self.loc))
        stim.delay = self.delay
        stim.dur = self.dur
        stim.amp = self.amp
        
        return stim