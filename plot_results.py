from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np

def expanded_nodes(heurisitic, expanded_nodes):
    x = np.arange(len(heurisitic))
    # expanded_nodes = [50, 20, 80, 123]
    fig, ax = plt.subplots()
    plt.bar(x, expanded_nodes)
    plt.xticks(x, heurisitic)
    plt.xlabel('heuristic')
    plt.ylabel('expanded nodes')
    ax.xaxis.label.set_color('blue')
    ax.yaxis.label.set_color('blue')
    ax.title.set_color('blue')

    plt.title('expanded nodes for IDA* by heuristic')

    plt.show()