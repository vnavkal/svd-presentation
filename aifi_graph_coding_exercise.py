import unittest


def loop_exists(edges):
    """Detect whether a given set of graph edges has a cycle

    Parameters
    ----------
    edges : set of pairs of vertices, e.g. {('V', 'W'), ('W', 'X')}

    Returns
    -------
    bool : indicates whether `edges` contains a cycle
    """
    if edges:
        start_vertex = next(iter(edges))[0]
        edges_traversed, loop_found = (
            find_loops_from_start_vertex(start_vertex, edges))
        if loop_found:
            return True
        else:
            remaining_edges = edges - edges_traversed
            return loop_exists(remaining_edges)
    else:
        return False


def find_loops_from_start_vertex(start_vertex, edges, edges_visited_this_traversal=set(),
                                 edges_visited_this_path=set()):
    """Traverse subgraph starting at `start_vertex`, checking for cycles"""
    edges_starting_at_vertex = [edge for edge in edges
                                if edge[0] == start_vertex]
    for edge in edges_starting_at_vertex:
        edges_visited_this_traversal = edges_visited_this_traversal | {edge}
        if edge in edges_visited_this_path:
            return edges_visited_this_traversal, True  # found a cycle
        else:
            edges_visited_this_traversal, loop_found = (
                find_loops_from_start_vertex(
                    edge[1],
                    edges,
                    edges_visited_this_traversal=edges_visited_this_traversal,
                    edges_visited_this_path=edges_visited_this_path | {edge}
                )
            )
            if loop_found:  # subgraph traversal found a cycle
                return edges_visited_this_traversal, True
    return edges_visited_this_traversal, False


class TestLoopExists(unittest.TestCase):
    def test_no_edges(self):
        edges = {}
        self.assertFalse(loop_exists(edges))

    def test_one_edge(self):
        edges = {('V', 'W')}
        self.assertFalse(loop_exists(edges))

    def test_cycle_of_length_1(self):
        edges = {('V', 'V')}
        self.assertTrue(loop_exists(edges))

    def test_cycle_of_length_2(self):
        edges = {('V', 'W'), ('W', 'V')}
        self.assertTrue(loop_exists(edges))

    def test_cycle_of_length_4(self):
        edges = {('U', 'V'), ('V', 'W'), ('W', 'X'), ('X', 'U')}
        self.assertTrue(loop_exists(edges))

    def test_complicated_loopless_graph(self):
        edges = {('U', 'V'), ('V', 'W'), ('X', 'W'),
                 ('Y', 'W'), ('Y', 'X'), ('W', 'Z')}
        self.assertFalse(loop_exists(edges))

    def test_complicated_graph_with_loop(self):
        edges = {('U', 'V'), ('V', 'W'), ('X', 'W'),
                 ('Y', 'W'), ('Y', 'X'), ('W', 'U')}
        self.assertTrue(loop_exists(edges))
