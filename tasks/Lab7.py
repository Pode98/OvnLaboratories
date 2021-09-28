import numpy as np

from core.elements import *


def main():
    network_fixed_rate = Network('nodes_full_fixed_rate.json')
    network_flex_rate = Network('nodes_full_flex_rate.json', 'flex_rate')
    network_shannon = Network('nodes_full_shannon.json', 'shannon')
    bins = np.linspace(90, 700, 20)
    # Fixed Rate
    node_labels1 = list(network_fixed_rate.nodes.keys())
    connections1 = []
    for i in range(100):
        shuffle(node_labels1)
        connection = Connection(node_labels1[0], node_labels1[-1], 1e-3)
        connections1.append(connection)
    streamed_connection_fixed_rate = network_fixed_rate.stream(connections1, best='snr')
    snrs = [connection.snr for connection in streamed_connection_fixed_rate]
    snrs_ = np.ma.masked_equal(snrs, 0)
    plt.hist(snrs_, bins=20)

    plt.title('SNR Distribution Full fixed-rate')
    plt.xlabel('dB')
    plt.savefig('results/SNRDistributionFullfixed_rate.png')
    plt.show()

    bit_rate_fixed_rate = [connection.bit_rate for connection in streamed_connection_fixed_rate]
    brfr = np.ma.masked_equal(bit_rate_fixed_rate, 0)
    plt.hist(brfr, bins, label='fixed-rate')

    plt.title('BitRate Full fixed-rate')
    plt.xlabel('Gbps')
    plt.savefig('results/BitRateFullfixed_rate.png')
    plt.show()

    # Flex rate
    node_labels2 = list(network_flex_rate.nodes.keys())
    connections2 = []
    for i in range(100):
        shuffle(node_labels2)
        connection = Connection(node_labels2[0], node_labels2[-1], 1e-3)
        connections2.append(connection)
    streamed_connection_flex_rate = network_flex_rate.stream(connections2, best='snr')
    snrs = [connection.snr for connection in streamed_connection_flex_rate]
    snrs_ = np.ma.masked_equal(snrs, 0)
    plt.hist(snrs_, bins=20)

    plt.title('SNR Distribution Full flex-rate')
    plt.xlabel('dB')
    plt.savefig('results/SNRDistributionFullflex_rate.png')
    plt.show()

    bit_rate_flex_rate = [connection.bit_rate for connection in streamed_connection_flex_rate]
    brfr = np.ma.masked_equal(bit_rate_flex_rate, 0)
    plt.hist(brfr, bins, label='flex-rate')

    plt.title('BitRate Full flex-rate')
    plt.xlabel('Gbps')
    plt.savefig('results/BitRateFullflex_rate.png')
    plt.show()

    # Shannon
    node_labels3 = list(network_shannon.nodes.keys())
    connections3 = []
    for i in range(100):
        shuffle(node_labels3)
        connection = Connection(node_labels3[0], node_labels3[-1], 1e-3)
        connections3.append(connection)
    streamed_connection_shannon = network_shannon.stream(connections3, best='snr')
    snrs = [connection.snr for connection in streamed_connection_shannon]
    snrs_ = np.ma.masked_equal(snrs, 0)
    plt.hist(snrs_, bins=20)

    plt.title('SNR Distribution Full shannon')
    plt.xlabel('dB')
    plt.savefig('results/SNRDistributionFullshannon.png')
    plt.show()

    bit_rate_shannon = [connection.bit_rate for connection in streamed_connection_shannon]
    brfr = np.ma.masked_equal(bit_rate_shannon, 0)
    plt.hist(brfr, bins, label='shannon')

    plt.title('BitRate Full shannon')
    plt.xlabel('Gbps')
    plt.savefig('results/BitRateFullshannon.png')
    plt.show()

    # total capacities

    # streamed_connections = network_fixed_rate.stream(connections1)
    # latencies = [connection.latency for connection in streamed_connection_shannon]
    # plt.hist(np.ma.masked_equal(latencies, 0), bins=25)
    # plt.title('Latency Distribution')
    # plt.savefig('Plots/LatencyDistribution.png')
    # plt.show()
    # snrs=[connection.snr for connection in streamed_connection_shannon]
    # plt.hist(np.ma.masked_equal(snrs, 0), bins=20)
    # plt.title('SNR Dstribution')
    # plt.savefig('Plots/SNRDistribution.png')
    # plt.show()

    # print("Average Latency: ", np.average(np.ma.masked_equal(latencies,0)))
    # print("Average SNR: ", np.average(np.ma.masked_equal(snrs,0)))
    print("Total Capacity Fixed-Rate:", np.sum(bit_rate_fixed_rate))
    print("Average Capacity Fixed-Rate:", np.mean(np.ma.masked_equal(bit_rate_fixed_rate, 0)))
    print("Total Capacity Flex-Rate:", np.sum(bit_rate_flex_rate))
    print("Average Capacity Flex-Rate:", np.mean(np.ma.masked_equal(bit_rate_flex_rate, 0)))
    print("Total Capacity Shannon:", np.sum(bit_rate_shannon).round(2))
    print("Average Capacity Shannon:", np.mean(np.ma.masked_equal(bit_rate_shannon, 0).round(2)))
