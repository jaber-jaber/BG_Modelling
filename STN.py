from neuron import h
from Cell import Cell
import textwrap

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
        self.soma.L = self.soma.diam = 60
        self.soma.nseg = 1
        self.shape_3D()

    def define_biophysics(self):
        self.soma.Ra = 200
        self.soma.cm = 1
        print('Biophysics defined.')

        # Area = 10000 um2
    
        # Defining current properties
        self.soma.insert('stn')

        # self.soma.gnabar_stn = 49e-3 # S/cm2
        # self.soma.gkdrbar_stn = 57e-3
        # self.soma.gkcabar_stn = 1e-3 * 10
        # # self.soma.gkabar_stn = 5e-3
        # self.soma.gcalbar_stn = 15e-3 * 10
        # self.soma.gcatbar_stn = 5e-3 * 10
        # self.soma.kca_stn = 2
        # self.soma.gl_stn = 0.35e-3