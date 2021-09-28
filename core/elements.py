import itertools
import json
import matplotlib
import math
import random

import numpy as np
import pandas as pd
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from scipy.constants import c, h, pi
from random import shuffle

BER_t = 1e-3
Bn=12.5e9 #banda rumore


class Lightpath(object):  #Lab5 definita nuova classe
    def __init__(self, power, path, channel):
        self._sig_power = power
        self._path = path
        self._channel = channel
        self._noise_power = 0
        self._latency = 0
        self.Rs = 32.0e9
        self.df = 50.0e9

    @property
    def signal_power(self):
        return self._sig_power

    def set_signal_power(self, value):
        self._sig_power = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def channel(self):
        return self._channel

    @property
    def noise_power(self):
        return self._noise_power

    @noise_power.setter
    def noise_power(self, value):
        self._noise_power = value

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self, value):
        self._latency = value

    def add_noise(self, value):
        self.noise_power += value

    def add_latency(self, value):
        self.latency += value

    def next(self):
        self.path = self.path[1:]

class SignalInformation(Lightpath):
    def __init__(self,power,path):
        self._signal_power=power
        self._path=path
        self._noise_power=0
        self._latency=0

    @property
    def signal_power(self):
        return self._signal_power

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self,path):
        self._path=path

    @property
    def noise_power(self):
        return self._noise_power

    @noise_power.setter
    def noise_power(self,noise):
        self._noise_power=noise

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self,latency):
        self._latency=latency

    def add_noise(self,noise):
        self._noise_power+=noise

    def add_latency(self,latency):
        self._latency+=latency

    def next(self):
        self.path=self.path[1:]

################################### CLASS LINE ###########################################

class Line(object):

    def __init__(self, line_dict):
        self._label = line_dict['label']
        self._lenght = line_dict['lenght']
        self._state = ['free'] * 10  # Lab5 trasformato il campo in vettore
        self._successive = {}  # Node

    @property
    def label(self):
        return self._label

    @property
    def lenght(self):
        return self._lenght

    @property  # Lab4
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        # state = state.lower().strip()
        state = [s.lower().strip() for s in state]  # aggiunta in Lab5
        # if state in ['free', 'occupied']:vecchia condizione
        if set(state).issubset(set(['free', 'occupied'])):  # Modifica Lab5, dovuto da aggiornamento a vettore
            self._state = state
        else:
            print('ERROR: line state not recognized.Value:', set(state) - set(['free', 'occupied']))  # aggiunta a Lab5
            # print('ERROR: line state not recognized.Value:', state) vecchia condizione

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    def latency_generation(self):
        latency = self._lenght / (c * 2 / 3)
        return latency

    def noise_generation(self, signal_power):
        noise = signal_power / (2 * self._lenght)
        return noise

    def propagate(self, lightpath, occupation=False):  # sostituito SignalInformation con Lightpath Lab5
        # latency
        latency = self.latency_generation()
        lightpath.add_latency(latency)

        # noise
        signal_power = lightpath.signal_power
        noise = self.noise_generation(signal_power)
        lightpath.add_noise(noise)

        # state
        if occupation:  # Condizione aggiornata da Lab5
            channel = lightpath.channel
            new_state = list(self.state)
            new_state[channel] = 'occupied'
            self.state = new_state

        node = self.successive[lightpath.path[0]]
        lightpath = node.propagate(lightpath, occupation)
        return lightpath


#################################### CLASS NODE ###############################################

class Node(object):
    def __init__(self,node_dict):
        self._label=node_dict['label']
        self._position=node_dict['position']
        self._connected_nodes=node_dict['connected_nodes']
        self._successive={}
        self._switching_matrix=None #Lab6 added attribute property and setter
        self._transceiver='' #Lab7 es 2

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

    @switching_matrix.setter
    def switching_matrix(self, value):
        self._switching_matrix = value

    @property
    def transceiver(self):
        return self._transceiver

    @transceiver.setter
    def transceiver(self,transceiver):
        self._transceiver=transceiver

    def propagate(self,lightpath,occupation=False):
        path=lightpath.path
        if len(path)>1:
            line_label=path[:2]
            line=self.successive[line_label]
            lightpath.next()
            lightpath=line.propagate(lightpath, occupation) #Lab5 aggiornato lightpath al posto di signalinformation

        return lightpath


######################## CLASS NETWORK ###########################################

class Network(object):
    def __init__(self,json_path,transceiver='fixed_rate'):
        self._nodes={}
        self._lines={}
        self._connected = False #Lab4
        self._weighted_paths = None #Lab4
        self._route_space = None #Lab5

        node_json=json.load(open(json_path,'r'))
        for node_label in node_json:
            #create nodes
            node_dict=node_json[node_label]
            node_dict['label']=node_label
            node=Node(node_dict)
            self._nodes[node_label]=node

            #Lab 7
            if 'transceiver' not in node_json[node_label]['transceiver']:
                node.transceiver=transceiver
            else:
                node.transceiver=node_json[node_label]['transceiver']

            #create lines
            for connected_node_label in node_dict['connected_nodes']:
                line_dict={}
                line_label= node_label+connected_node_label
                line_dict['label']=line_label
                node_position=np.array(node_json[node_label]['position'])
                connected_node_position=np.array(node_json[connected_node_label]['position'])
                line_dict['lenght']=np.sqrt(np.sum(node_position-connected_node_position)**2)
                line=Line(line_dict)
                self._lines[line_label]=line



    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    @property
    def connected(self):
        return self._connected


    def draw(self):
        nodes=self.nodes
        for node_label in nodes:
            n0=nodes[node_label]
            x0=n0.position[0]
            y0=n0.position[1]
            plt.plot(x0,y0,'go',markersize=10)
            plt.text(x0+20,y0+20,node_label)
            for connected_node_label in n0.connected_nodes:
                n1=nodes[connected_node_label]
                x1=n1.position[0]
                y1=n1.position[1]
                plt.plot([x0,x1],[y0,y1],'b')
        plt.xlabel('Km')
        plt.title('Network')
        plt.show()

    def find_paths(self,label1,label2):
        cross_nodes=[key for key in self.nodes.keys() if ((key!=label1)&(key!=label2))]
        cross_lines=self.lines.keys()
        inner_paths={}
        inner_paths['0']=label1
        for i in range(len(cross_nodes)+1):
            inner_paths[str(i+1)]=[]
            for inner_path in inner_paths[str(i)]:
                inner_paths[str(i+1)]+=[
                    inner_path + cross_node
                    for cross_node in cross_nodes
                    if ((inner_path[-1]+cross_node in cross_lines)&
                        (cross_node not in inner_path))]

        paths=[]
        for i in range(len(cross_nodes)+1):
            for path in inner_paths[str(i)]:
                if path[-1] + label2 in cross_lines:
                    paths.append(path+label2)
        return  paths

    def connect(self):#Added switching matrix reference Lab6
        nodes_dict=self.nodes
        lines_dict=self.lines
        switching_matrix={}
        for node_label in nodes_dict:
            node=nodes_dict[node_label]
            for connected_node in node.connected_nodes:
                inner_dict={connected_node:np.zeros(10)}
                for connected_node2 in node.connected_nodes:
                    if connected_node2!=connected_node:
                        dict_tmp={connected_node2:np.ones(10)}
                        inner_dict.update(dict_tmp)

                switching_matrix.update({connected_node:inner_dict})

                line_label=node.label+connected_node
                line=lines_dict[line_label]
                line.successive[connected_node]=nodes_dict[connected_node]
                node.successive[line_label]=lines_dict[line_label]
            node.switching_matrix=switching_matrix
            switching_matrix={}
        self._connected = True


    # def propagate(self,signal_information):  #funzione prima di Lab5
    #     path=signal_information.path
    #     start_node=self.nodes[path[0]]
    #     propagated_signal_information=start_node.propagate(signal_information)
    #     return  propagated_signal_information

    def propagate(self,lightpath, occupation=False): #Aggiornata a Lab5
        path=lightpath.path
        start_node=self.nodes[path[0]]
        propagated_lightpath=start_node.propagate(lightpath,occupation)
        return  propagated_lightpath


    #Lab4
    @property
    def weighted_paths(self):
        return self._weighted_paths

    def set_weighted_paths(self, signal_power):#Modifica Lab5 con implementazione route space
        if not self.connected:
            self.connect()
        node_labels = self.nodes.keys()
        pairs = []
        for label1 in node_labels:
            for label2 in node_labels:
                if label1 != label2:
                    pairs.append(label1 + label2)
        df = pd.DataFrame()
        paths = []
        latencies = []
        noises = []
        snrs = []

        for pair in pairs:
            for path in self.find_paths(pair[0], pair[1]):
                path_string = ''
                for node in path:
                    path_string += node + '->'
                paths.append(path_string[:-2])

                # Propagation
                signal_information = SignalInformation(signal_power, path)
                signal_information = self.propagate(signal_information,occupation=False)
                latencies.append(signal_information.latency)
                noises.append(signal_information.noise_power)
                snrs.append(10 * np.log10(signal_information.signal_power / signal_information.noise_power) )

        df['path'] = paths
        df['latency'] = latencies
        df['noise'] = noises
        df['snr'] = snrs
        self._weighted_paths = df
        #Aggiunta da Lab5
        route_space = pd.DataFrame()
        route_space['path'] = paths
        for i in range(10):
            route_space[str(i)] = ['free']*len(paths)
            self._route_space = route_space

    #Lab3 --ridefinita in Lab4 sotto
    #def find_best_latency(self, input_node, output_node):
    #   all_paths = self.weighted_paths.path.values
    #  inout_paths = [path for path in all_paths if ((path[0] == input_node) and (path[-1] == output_node))]
    #    inout_df = self.weighted_paths.loc[
    #        self.weighted_paths.path.isin(inout_paths)]
    #    best_latency = np.min(inout_df.latency.values)
    #    best_path = inout_df.loc[
    #        inout_df.latency == best_latency].path.values[0].replace('->', '')
    #    return best_path

    def stream(self, connections, best='latency'): #Aggiornato a Lab7
        streamed_connections = []
        for connection in connections:
            input_node = connection.input_node
            output_node = connection.output_node
            signal_power = connection.signal_power
            #self.set_weighted_paths(signal_power) Lab3
            self.set_weighted_paths(1)  #Lab4
            if best == 'latency':
                path = self.find_best_latency(input_node, output_node)
            elif best == 'snr':
                path = self.find_best_snr(input_node, output_node)
            else:
                print('ERROR: best input not recognized.Value:', best)
                continue
            # if path: #added condition for Lab4 on the path
            #     in_signal_information = SignalInformation(signal_power, path)
            #     out_signal_information = self.propagate(in_signal_information)
            #     connection.latency = out_signal_information.latency
            #     noise = out_signal_information.noise_power
            #     connection.snr = 10 * np.log10(signal_power / noise)
            if path: #Condiione aggiornata a Lab5
                path_occupancy = self.route_space.loc[self.route_space.path == path].T.values[1:]
                channel = [i for i in range(len(path_occupancy)) if path_occupancy[i] =='free'][0]
                #Lab 7 es 3
                lightpath=Lightpath(signal_power,path,channel)
                rb=self.calculate_bit_rate(lightpath,self.nodes[input_node].transceiver)
                if rb==0:
                    continue
                else:
                    connection.bit_rate=rb
                #end
                path_occupancy = self.route_space.loc[
                                     self.route_space.path == path].T.values[1:]
                channel = [i for i in range(len(path_occupancy))
                           if path_occupancy[i] == 'free'][0]
                path = path.replace('->', '')
                in_lightpath = Lightpath(signal_power, path, channel)
                out_lightpath = self.propagate(in_lightpath, True)
                connection.latency = out_lightpath.latency
                noise_power = out_lightpath.noise_power
                connection.snr = 10 * np.log10(signal_power / noise_power)
                self.update_route_space(path, channel)
            else:
                connection.snr=0
                connection.latency='None'
            streamed_connections.append(connection)
        return streamed_connections

    #due metodi aggiunti (lab5)
    @staticmethod
    def path_to_line_set(path):
        path = path.replace('->', '')
        return set([path[i] + path[i + 1] for i in range(len(path) - 1)])

    def update_route_space(self, path, channel): #Modifica da Lab6 per aggiornare la routing space con la switching matrix
        all_paths = [self.path_to_line_set(p) for p in self.route_space.path.values]
        states = self.route_space[str(channel)]
        lines = self.path_to_line_set(path)
        for i in range(len(all_paths)):
            line_set = all_paths[i]
            if lines.intersection(line_set):
                states[i] = 'occupied'

                path_to_update=self.line_set_to_path(line_set)

                for j in range(len(path_to_update)):     #strange
                    if j not in (0, len(path_to_update) - 1):
                        if ((path_to_update[j - 1] in self.nodes[path_to_update[j]].connected_nodes) & (
                                path_to_update[j + 1] in self.nodes[path_to_update[j]].connected_nodes)):
                            self.nodes[path_to_update[j]].switching_matrix[path_to_update[j - 1]][
                                path_to_update[j + 1]][
                                channel] = 0
        self.route_space[str(channel)] = states

    #metodo per ottenere tutte le liste di stati dalle linee
    @staticmethod #how tf is this working i've really have no idea
    def line_set_to_path(line_set):
        path=""
        elements=list(itertools.permutations(list(line_set), len(list(line_set))))
        for i in range(len(elements)):
            flag=1
            for j in range(len(elements)-1):
                if elements[i][j][1] != elements[i][j+1][0]:
                    flag=0
                j+=2
            if flag==1:
                for j in range(len(elements[i])):
                    path+=elements[i][j][0]
                return path


    #es7 Lab4
    #Modifica Lab5 es4 in modo da gestire la channel occupancy (tutti e tre i metodi)

    # def available_paths(self, input_node, output_node):    #Funzione da Lab4
    #     if self.weighted_paths is None:
    #         self.set_weighted_paths(1)
    #     all_paths = [path for path in self.weighted_paths.path.values
    #         if ((path[0] == input_node) and (path[-1] == output_node))]
    #     unavailable_lines = [line for line in self.lines
    #         if self.lines[line].state =='occupied']
    #     available_paths = []
    #     for path in all_paths:
    #         available = True
    #         for line in unavailable_lines:
    #             if line[0] + '->' + line[1] in path:
    #                 available = False
    #                 break
    #         if available:
    #             available_paths.append(path)
    #     return available_paths

    def available_paths(self, input_node, output_node): #Funione ridefinita in contesto a Lab5
        if self.weighted_paths is None:
            self.set_weighted_paths(1)
        all_paths = [path for path in self.weighted_paths.path.values
                 if ((path[0] == input_node) and (path[-1] == output_node))]
        available_paths = []
        for path in all_paths:
            path_occupancy = self.route_space.loc[self.route_space.path == path].T.values[1:]
            if 'free' in path_occupancy:
                available_paths.append(path)
        return available_paths

    def find_best_snr(self, input_node, output_node):
        available_paths = self.available_paths(input_node, output_node)
        if available_paths:
            inout_df = self.weighted_paths.loc[self.weighted_paths.path.isin(available_paths)]
            best_snr = np.max(inout_df.snr.values)
            #best_path = inout_df.loc[inout_df.snr == best_snr].path.values[0].replace('->', '')
            best_path = inout_df.loc[inout_df.snr == best_snr].path.values[0] #da Lab5
        else:
            best_path = None
        return best_path

    def find_best_latency(self, input_node, output_node):
        available_paths = self.available_paths(input_node, output_node)
        if available_paths:
            inout_df = self.weighted_paths.loc[self.weighted_paths.path.isin(available_paths)]
            best_latency = np.min(inout_df.latency.values)
            #best_path = inout_df.loc[inout_df.latency == best_latency].path.values[0].replace('->', '')
            best_path = inout_df.loc[inout_df.latency == best_latency].path.values[0]#da Lab5
        else:
            best_path = None
        return best_path

    #Lab5
    @property
    def route_space(self):
        return self._route_space

    #Lab7
    def calculate_bit_rate(self, lightpath, strategy):
        global BER_t
        Rs=lightpath.Rs
        global Bn
        path=lightpath.path
        Rb=0
        GSNR_db=pd.array(self.weighted_paths.loc[self.weighted_paths['path'] == path]['snr'])[0]
        GSNR=10**(GSNR_db/10)

        if strategy=='fixed_rate':
            if GSNR > 2 * math.erfcinv(2 * BER_t) ** 2 * (Rs/Bn):
                Rb=100
            else:
                Rb=0

        if strategy == 'flex_rate':
            if GSNR < 2 * math.erfcinv(2 * BER_t) ** 2 * (Rs / Bn):
                Rb = 0
            elif (GSNR > 2 * math.erfcinv(2 * BER_t) ** 2 * (Rs / Bn)) & (GSNR < (14 / 3) * math.erfcinv(
                    (3 / 2) * BER_t) ** 2 * (Rs / Bn)):
                Rb = 100
            elif (GSNR > (14 / 3) * math.erfcinv((3 / 2) * BER_t) ** 2 * (Rs / Bn)) & (GSNR < 10 * math.erfcinv(
                    (8 / 3) * BER_t) ** 2 * (Rs / Bn)):
                Rb = 200
            elif GSNR > 10 * math.erfcinv((8 / 3) * BER_t) ** 2 * (Rs / Bn):
                Rb = 400

        if strategy == 'shannon':
            Rb = 2 * Rs * np.log2(1 + Bn / Rs * GSNR) / 1e9

        return Rb



############################# CLASS CONNECTIONS ######################################

class Connection(object):
    def __init__(self,input_node,output_node,signal_power):
        self._input_node = input_node
        self._output_node = output_node
        self._signal_power = signal_power
        self._latency = 0
        self._snr = 0
        self._bit_rate = 0

    @property
    def input_node(self):
        return self._input_node

    @property
    def output_node(self):
        return self._output_node

    @property
    def signal_power(self):
        return self._signal_power

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self,latency):
        self._latency = latency

    @property
    def snr(self):
        return self._snr

    @snr.setter
    def snr(self,snr):
        self._snr = snr

    @property
    def bit_rate(self):
        return self._bit_rate

    @bit_rate.setter
    def snr(self, bit_rate):
        self._bit_rate = bit_rate
