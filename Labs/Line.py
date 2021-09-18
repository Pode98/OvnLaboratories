import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c
from Labs.Node import *
from Labs.Signal_information import *


class Line(object):

    def __init__(self,line_dict):
        self._label=line_dict['label']
        self._lenght=line_dict['lenght']
        self._state='free'
        self._successive={} #Node

    @property
    def label(self):
        return self._label

    @property
    def lenght(self):
        return self._lenght

    @property       #Lab4
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        state = state.lower().strip()
        if state in ['free', 'occupied']:
            self._state = state
        else:
            print('ERROR: line state not recognized.Value:', state)

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self,successive):
        self._successive=successive

    def latency_generation(self):
        latency=self._lenght/(c*2/3)
        return latency

    def noise_generation(self,signal_power):
        noise=signal_power/(2*self._lenght)
        return noise

    def propagate(self,signal_information,occupation=False):
        #latency
        latency=self.latency_generation()
        signal_information.add_latency(latency)

        #noise
        signal_power= signal_information.signal_power
        noise=self.noise_generation(signal_power)
        signal_information.add_noise(noise)

        #state
        if occupation:
            self.state = 'occupied'

        node=self.successive[signal_information.path[0]]
        signal_information=node.propagate(signal_information,occupation)
        return signal_information
