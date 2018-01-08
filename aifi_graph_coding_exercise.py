import unittest


def cycle_exists(edges):
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
        edges_traversed, cycle_found = (
            find_cycles_from_start_vertex(start_vertex, edges))
        if cycle_found:
            return True
        else:
            remaining_edges = edges - edges_traversed
            return cycle_exists(remaining_edges)
    else:
        return False


def find_cycles_from_start_vertex(start_vertex,
                                  all_edges,
                                  current_path=set()):
    """Traverse subgraph starting at `start_vertex`, checking for cycles

    This function iterates through all paths starting from `start_vertex`,
        logging visited edges in the set `edges_visited_this_traversal` and
        checking whether any path can be appended to `current_path` to create
        a path with a cycle

    Parameters
    ----------
        start_vertex : vertex at which to start traversal
        all_edges : set of all edges in the graph
        current_path : set of edges in the current path

    Returns
    -------
        edges_visited_this_traversal : set of edges, indicating which edges
            have been traversed by the time the function returns
        cycle_found : bool, indicating whether the union of
            {edges reachable from `start_vertex`} and `current_path` contains a
            cycle
    """
    edges_visited_this_traversal = set()
    edges_starting_at_vertex = [edge for edge in all_edges
                                if edge[0] == start_vertex]

    for edge in edges_starting_at_vertex:
        edges_visited_this_traversal.add(edge)
        if edge in current_path:
            return edges_visited_this_traversal, True
        else:
            edges_visited_in_subtraversal, cycle_found = (
                find_cycles_from_start_vertex(
                    edge[1],
                    all_edges,
                    current_path=(current_path | {edge})
                )
            )
            edges_visited_this_traversal.update(edges_visited_in_subtraversal)
            if cycle_found:
                return edges_visited_this_traversal, True
    return edges_visited_this_traversal, False


class TestCycleExists(unittest.TestCase):
    def test_no_edges(self):
        edges = {}
        self.assertFalse(cycle_exists(edges))

    def test_one_edge(self):
        edges = {('V', 'W')}
        self.assertFalse(cycle_exists(edges))

    def test_cycle_of_length_1(self):
        edges = {('V', 'V')}
        self.assertTrue(cycle_exists(edges))

    def test_cycle_of_length_2(self):
        edges = {('V', 'W'), ('W', 'V')}
        self.assertTrue(cycle_exists(edges))

    def test_cycle_of_length_4(self):
        edges = {('U', 'V'), ('V', 'W'), ('W', 'X'), ('X', 'U')}
        self.assertTrue(cycle_exists(edges))

    def test_complicated_cyclefree_graph(self):
        edges = {(x, y) for x in range(10) for y in range(x+1, 20)}
        self.assertFalse(cycle_exists(edges))

    def test_complicated_graph_with_cycle(self):
        edges = {(x, y) for x in range(10) for y in range(x+1, 20)} | {(15, 2)}
        self.assertTrue(cycle_exists(edges))
