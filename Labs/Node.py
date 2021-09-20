import json
import numpy as np
import matplotlib.pyplot as plt

from Labs.Signal_information import *
from Labs.Line import *

class Node(object):
    def __init__(self,node_dict):
        self._label=node_dict['label']
        self._position=node_dict['position']
        self._connected_nodes=node_dict['connected_nodes']
        self._successive={}
        self._switching_matrix=None #Lab6 added attribute property and setter

    @property
    def label(self):
        return self._label

    @property
    def position(self):
        return self._position

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self,successive):
        self._successive=successive

    @property
    def switching_matrix(self):
        return self._switching_matrix

    @successive.setter
    def successive(self, value):
        self._switching_matrix = value

    def propagate(self,lightpath,occupation=False):
        path=lightpath.path
        if len(path)>1:
            line_label=path[:2]
            line=self.successive[line_label]
            lightpath.next()
            lightpath=line.propagate(lightpath, occupation) #Lab5 aggiornato lightpath al posto di signalinformation

        return lightpath





