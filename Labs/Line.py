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
        self._successive={} #Node

    @property
    def label(self):
        return self._label

    @property
    def lenght(self):
        return self._lenght

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

    def propagate(self,signal_information):
        #latency
        latency=self.latency_generation()
        signal_information.add_latency(latency)

        #noise
        signal_power= signal_information.signal_power
        noise=self.noise_generation(signal_power)
        signal_information.add_noise(noise)

        node=self.successive[signal_information.path[0]]
        signal_information=node.propagate(signal_information)
        return signal_information