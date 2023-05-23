from neuron import h
from Cell import Cell

class STN(Cell):
    def __init__(self, amp=0, dur=1e9, loc=0.5, delay=0):
        super(STN, self).__init__() # Functions are inherited from class Cell. If undefined here, 
        # will act as functions that are defined in Cell.

        self.ident = 'stn'
        self.delay = delay # Time delay of stimulation
        self.dur = dur # Duration of current
        self.loc = loc # Location of current onset
        self.amp = amp # Magnitude of current

    def create_sections(self):
        self.soma = h.Section(name='soma', cell=self)

    def define_geometry(self):
        self.soma.L = self.soma.diam = 12.6157
        self.shape_3D()

    def define_biophysics(self):
        for sec in self.all:
            sec.Ra = 100
            sec.cm = 100

        # Insert membrane currents
        
        