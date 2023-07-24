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
        self.shape_3D()

    def define_biophysics(self):
        self.soma.Ra = 200
        self.soma.nseg = 1
        self.soma.cm = 1

        # Area = 10000 um2
    
        # Defining electrophysiological properties
        self.soma.insert('stn')

        # Otsuka gAHP = 0.001

        # Rhythmic Spontaneous activity is primarily driven by
        self.soma.gnabar_stn = 49e-3 # Fast sodium channel
        self.soma.gkdrbar_stn = 57e-3 # Delayed rectifier K channel (repolarization)
        self.soma.gkabar_stn = 5e-3 # A-type potassium channel for delaying depolarization

        # Freq of spontaneous activity depends on
        self.soma.gkcabar_stn = 1e-3 # AHP Ca2+-dependent K channel
        self.soma.gcalbar_stn = 15e-3 # Long-lasting calcium Ca2+ currents
        self.soma.gcatbar_stn = 5e-3 # Low threshold T-type Ca2+ currents

        # Ca dynamics and leak current
        self.soma.kca_stn = 2 # Ca removal rate
        self.soma.gl_stn = 0.29e-3 # Leak current
        