import pandas as pd
from core.elements import *
from random import shuffle
import copy


# used for the traffic matrix
def main():
    sat_percent = 95
    # fixed rate_____________________________________________________________________________
    network = Network('248253.json')
    n_node = len(network.nodes.keys())
    saturationFix = []
    MsFix = []
    M = 1
    while 1:
        t_mtx = np.ones((n_node, n_node)) * 100 * M
        for i in range(n_node):
            t_mtx[i][i] = 0
        elements = list(itertools.permutations(network.nodes.keys(), 2))
        n_elem = len(elements)
        for e in elements:  # remove the diagonal
            if e[0] == e[1]:
                elements.remove(e)
        for i in range(100):
            if len(elements) == 0:
                break
            el = random.choice(elements)
            val = network.upgrade_traffic_matrix(t_mtx, el[0], el[1])
            if (val == 0) | (val == np.inf):
                elements.remove(el)
        sat = 0
        for row in t_mtx:
            for el in row:
                if el == float('inf'):
                    sat += 1
        sat = sat / n_elem * 100
        saturationFix.append(sat)
        MsFix.append(M)
        if sat > sat_percent:
            break
        M += 1
        network.free_space()
    plt.plot(MsFix, saturationFix)
    plt.title('Saturation Fixed-Rate')
    plt.savefig('Plots/M_fixed_rate.png')
    plt.xlabel('M')
    plt.ylabel('% of unsatisfied requests')
    plt.grid(linestyle='-', linewidth=0.5)
    plt.show()

    # flex rate_____________________________________________________________________________
    network_flex_rate = Network('248253.json', 'flex_rate')
    n_node = len(network_flex_rate.nodes.keys())
    saturationflex = []
    Msflex = []
    M = 1
    while (1):
        t_mtx = np.ones((n_node, n_node)) * 100 * M
        for i in range(n_node):
            t_mtx[i][i] = 0
        elements = list(itertools.permutations(network_flex_rate.nodes.keys(), 2))
        n_elem = len(elements)
        for e in elements:  # remove the diagonal
            if e[0] == e[1]:
                elements.remove(e)
        for i in range(100):
            if len(elements) == 0:
                break
            el = random.choice(elements)
            val = network_flex_rate.upgrade_traffic_matrix(t_mtx, el[0], el[1])
            if (val < 0) | (val == np.inf):
                elements.remove(el)
        sat = 0
        for row in t_mtx:
            for el in row:
                if el == float('inf'):
                    sat += 1
        sat = sat / n_elem * 100
        saturationflex.append(sat)
        Msflex.append(M)
        if sat > sat_percent:
            break
        M += 1
        network_flex_rate.free_space()
    plt.plot(Msflex, saturationflex)
    plt.title('Saturation Flex-Rate')
    plt.savefig('results/M_flex_rate.png')
    plt.xlabel('M')
    plt.ylabel('% of unsatisfied requests')
    plt.grid(linestyle='-', linewidth=0.5)
    plt.show()

    # shannon________________________________________________________________________________
    network_shannon = Network('248253.json', 'shannon')
    n_node = len(network_shannon.nodes.keys())
    saturationshan = []
    Msshan = []
    M = 1

    while (1):
        t_mtx = np.ones((n_node, n_node)) * 100 * M
        for i in range(n_node):
            t_mtx[i][i] = 0
        elements = list(itertools.permutations(network_shannon.nodes.keys(), 2))
        n_elem = len(elements)
        for e in elements:  # remove the diagonal
            if e[0] == e[1]:
                elements.remove(e)
        for i in range(100):
            if len(elements) == 0:
                break
            el = random.choice(elements)
            val = network_shannon.upgrade_traffic_matrix(t_mtx, el[0], el[1])
            if (val < 0) | (val == np.inf):
                elements.remove(el)
        sat = 0
        for row in t_mtx:
            for el in row:
                if el == float('inf'):
                    sat += 1
        sat = sat / n_elem * 100
        saturationshan.append(sat)
        Msshan.append(M)
        if sat > sat_percent:
            break
        M += 1
        network_shannon.free_space()
    plt.plot(Msshan, saturationshan)
    plt.title('Saturation Parameter Shannon')
    plt.savefig('results/M_shannon.png')
    plt.xlabel('M')
    plt.ylabel('% of unsatisfied requests')
    plt.grid(linestyle='-', linewidth=0.5)
    plt.show()
    plt.plot(MsFix, saturationFix, label='fixed-rate')
    plt.plot(Msflex, saturationflex, label='flex-rate')
    plt.plot(Msshan, saturationshan, label='shannon')
    plt.xlabel('M')
    plt.ylabel('% of unsatisfied requests')
    plt.grid(linestyle='-', linewidth=0.5)
    plt.legend(loc='lower right')
    plt.title('Saturation Parameter')
    plt.savefig('results/M_all.png')
    plt.show()


if __name__ == "__main__":
    main()
