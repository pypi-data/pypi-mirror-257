import matplotlib.pyplot as plt
import networkx as nx
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra

nodes = [
    "velocity",
    "displacement",
    "acceleration",
    "pressure",
    "strain_rate",
    "strain",
    "deformation_rate",
]

func_graph = [
    [
        None,
        "integrate",
        "differentiate",
        "velocity_2_pressure",
        "velocity_2_strain_rate",
        None,
        None,
    ],
    ["differentiate", None, None, None, None, None, None],
    ["integrate", None, None, None, None, None, None],
    ["pressure_2_velocity", None, None, None, None, None, None],
    ["strain_rate_2_velocity", None, None, None, None, "integrate", None],
    [None, None, None, None, "differentiate", None, None],
    [None, None, None, None, "deformation_rate_2_strain_rate", None, None],
]


def map(self, out="velocity", nodes=nodes, func_graph=func_graph):
    """
    Plot the conversion path from one type to another.

    :param out: Output type. Default is 'velocity'.
    :param nodes: List of nodes. Default is ['velocity', 'displacement', 'acceleration', 'pressure', 'strain_rate', 'strain', 'deformation_rate'].
    """
    if self.stats.type == "unknown":
        raise ValueError("Cannot plot convert unknown type")

    _, path, adjacency_graph = _get_function_by_graph(
        nodes,
        func_graph,
        start=self.stats.type,
        end=out,
    )

    # create graph
    G = nx.DiGraph()
    for i, node in enumerate(nodes):
        for j, edge in enumerate(adjacency_graph[i]):
            if edge == 1:
                G.add_edge(node, nodes[j])

    path_nodes = [nodes[i] for i in path]
    node_colors = [
        "red" if node == path_nodes[0] or node == path_nodes[-1] else "black"
        for node in G.nodes()
    ]

    # plot graph
    pos = nx.spring_layout(G, iterations=200)
    nx.draw(
        G,
        pos,
        with_labels=False,
        node_color="skyblue",
        node_size=1500,
        arrowstyle="-|>",
        arrowsize=15,
        width=1,
    )

    # plot node labels
    labels = {node: node for node in G.nodes()}
    for i, node in enumerate(G.nodes()):
        plt.text(
            pos[node][0],
            pos[node][1],
            labels[node],
            ha="center",
            va="center",
            color=node_colors[i],
        )

    # plot text
    text = f"PATH: {' --> '.join(path_nodes)}"
    plt.text(
        0.4,
        -0.2,
        text,
        fontsize=12,
        ha="center",
        va="center",
        transform=plt.gca().transAxes,
    )

    plt.axis("off")
    plt.show()


def _get_function_by_graph(nodes, func_graph, start="displacement", end="acceleration"):
    start_node = nodes.index(start)
    end_node = nodes.index(end)
    adjacency_graph = [
        [1 if item is not None else 0 for item in row] for row in func_graph
    ]
    graph = csr_matrix(adjacency_graph)
    _, predecessors = dijkstra(
        csgraph=graph,
        directed=True,
        indices=start_node,
        return_predecessors=True,
        unweighted=True,
        min_only=False,
    )

    path = []
    i = end_node  # destination node
    while i != -9999:
        path.append(i)
        i = predecessors[i]
    path = path[::-1]

    funcs = []
    for i in range(len(path) - 1):
        funcs.append(func_graph[path[i]][path[i + 1]])

    return funcs, path, adjacency_graph
