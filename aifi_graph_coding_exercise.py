import collections

Graph = collections.namedtuple('Graph', 'vertices', 'edges')


def loop_exists(graph):
    if graph.edges:
        start_vertex = graph.edges.first[0]
        edges_traversed, loop_found = find_loops_from_starting_vertex(start_vertex, graph)
        if loop_found:
            return True
        else:
            new_graph = Graph(graph.vertices, graph.edges - edges_traversed)
            return loop_exists(new_graph)
    else:
        return False


def find_loops_from_starting_vertex(start_vertex, graph, edges_found=set()):
    edges_starting_at_vertex = [edge for edge in graph.edges if edge[0] == start_vertex]
    for edge in edges_starting_at_vertex:
        if edge in edges_found:
            return None, True  # found a loop
        else:
            edges_found.add(edge)
            new_edges, result = find_loops_from_starting_vertex(edge[1], graph, edges_found)
