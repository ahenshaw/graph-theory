#%%
import networkx as nx 

def draw_from_edges(edges, layout='s'):
    edges =edges.split()
    edges = list(zip(*[edges[i::2] for i in range(2)]))
    g = nx.from_edgelist(edges)
    layout_fn = nx.spring_layout
    if layout == 'c':
        layout_fn = nx.circular_layout
    elif layout == 'r':
        layout_fn = nx.random_layout

    pos = layout_fn(g)    
    nx.draw(g, pos, node_color="orange")
    nx.draw_networkx_labels(g, pos)
    return g


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    edges = '''
W5  W5a
W5  W5b
W5  W5c
W5  W5d
W5a W5b
W5b W5c
W5c W5d
W5d W5a
'''
    draw_from_edges(edges, 's')
    plt.show()