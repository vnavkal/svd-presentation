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
        edges_traversed, loop_found = find_loops_from_start_vertex(start_vertex, edges)
        if loop_found:
            return True
        else:
            new_edges = edges - edges_traversed
            return loop_exists(new_edges)
    else:
        return False


def find_loops_from_start_vertex(start_vertex, edges, edges_found=set()):
    edges_starting_at_vertex = [edge for edge in edges if edge[0] == start_vertex]
    for edge in edges_starting_at_vertex:
        if edge in edges_found:
            return edges_found, True  # found a loop
        else:
            edges_found = edges_found | {edge}
            edges_found, loop_found = find_loops_from_start_vertex(edge[1], edges, edges_found)
            if loop_found:
                return edges_found, True
    return edges_found, False


class TestLoopExists(unittest.TestCase):
    def test_with_no_edges(self):
        edges = {}
        self.assertFalse(loop_exists(edges))

    def test_with_one_edge(self):
        edges = {('V', 'W')}
        self.assertFalse(loop_exists(edges))

    def test_with_0_cycle(self):
        edges = {('V', 'V')}
        self.assertTrue(loop_exists(edges))

    def test_with_1_cycle(self):
        edges = {('V', 'W'), ('W', 'V')}
        self.assertTrue(loop_exists(edges))

    def test_with_complicated_loopless_graph(self):
        edges = {('U', 'V'), ('V', 'W'), ('X', 'W'), ('Y', 'W'), ('Y', 'X')}
        self.assertFalse(loop_exists(edges))

    def test_with_complicated_graph_with_loop(self):
        edges = {('U', 'V'), ('V', 'W'), ('X', 'W'),
                 ('Y', 'W'), ('Y', 'X'), ('W', 'U')}
        self.assertTrue(loop_exists(edges))
