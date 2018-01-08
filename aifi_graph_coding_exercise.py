import collections
import unittest

Graph = collections.namedtuple('Graph', ('vertices', 'edges'))


def loop_exists(graph):
    if graph.edges:
        start_vertex = next(iter(graph.edges))[0]
        edges_traversed, loop_found = find_loops_from_start_vertex(start_vertex, graph)
        if loop_found:
            return True
        else:
            new_graph = Graph(graph.vertices, graph.edges - edges_traversed)
            return loop_exists(new_graph)
    else:
        return False


def find_loops_from_start_vertex(start_vertex, graph, edges_found=set()):
    edges_starting_at_vertex = [edge for edge in graph.edges if edge[0] == start_vertex]
    for edge in edges_starting_at_vertex:
        if edge in edges_found:
            return edges_found, True  # found a loop
        else:
            edges_found = edges_found | {edge}
            edges_found, loop_found = find_loops_from_start_vertex(edge[1], graph, edges_found)
            if loop_found:
                return edges_found, True
    return edges_found, False


class TestLoopExists(unittest.TestCase):
    def test_with_no_edges(self):
        graph = Graph(vertices={'V', 'W'}, edges={})
        self.assertFalse(loop_exists(graph))

    def test_with_one_edge(self):
        graph = Graph(vertices={'V', 'W'}, edges={('V', 'W')})
        self.assertFalse(loop_exists(graph))

    def test_with_0_cycle(self):
        graph = Graph(vertices={'V', 'W'}, edges={('V', 'V')})
        self.assertTrue(loop_exists(graph))

    def test_with_1_cycle(self):
        graph = Graph(vertices={'V', 'W'}, edges={('V', 'W'), ('W', 'V')})
        self.assertTrue(loop_exists(graph))

    def test_with_complicated_loopless_graph(self):
        graph = Graph(vertices={'U', 'V', 'W', 'X', 'Y'},
                      edges={('U', 'V'), ('V', 'W'), ('X', 'W'), ('Y', 'W'), ('Y', 'X')})
        self.assertFalse(loop_exists(graph))

    def test_with_complicated_graph_with_loop(self):
        graph = Graph(vertices={'U', 'V', 'W', 'X', 'Y'},
                      edges={('U', 'V'), ('V', 'W'), ('X', 'W'),
                             ('Y', 'W'), ('Y', 'X'), ('W', 'U')})
        self.assertTrue(loop_exists(graph))
