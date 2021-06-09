# Course: 
# Author: 
# Assignment: 
# Description:
from collections import deque


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """

        if v not in self.adj_list:
            self.adj_list[v] = []

    def add_edge_helper(self, u, v):

        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
        if u not in self.adj_list[v]:
            self.adj_list[v].append(u)

    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u == v:
            return None

        if v not in self.adj_list and u not in self.adj_list:
            self.add_vertex(v)
            self.add_vertex(u)
            self.add_edge_helper(u, v)

        if v in self.adj_list and u not in self.adj_list:
            self.add_vertex(u)
            self.add_edge_helper(u, v)

        if v not in self.adj_list and u in self.adj_list:
            self.add_vertex(v)
            self.add_edge_helper(u, v)

        if v in self.adj_list and u in self.adj_list:
            if v not in self.adj_list[u]:
                self.adj_list[u].append(v)
            if u not in self.adj_list[v]:
                self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """

        if v not in self.adj_list and u not in self.adj_list:
            return None

        if v in self.adj_list and u not in self.adj_list:
            return None

        if v not in self.adj_list and u in self.adj_list:
            return None

        if v in self.adj_list and u in self.adj_list:
            if v in self.adj_list[u]:
                self.adj_list[u].remove(v)
            if u in self.adj_list[v]:
                self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """

        if v in self.adj_list:
            self.adj_list.pop(v)
        for value_list in self.adj_list.values():
            if v in value_list:
                value_list.remove(v)

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """

        vertices = self.adj_list.keys()
        list_of_vertices = list(vertices)
        return list_of_vertices

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        list = []
        for k, v in self.adj_list.items():
            for z in v:
                whatever = (k, z)
                whatever_inv = (z, k)
                if whatever_inv not in list:
                    list.append(whatever)
        return list

    def is_valid_path_helper(self, path, index):
        if index == len(path) - 1:
            return True

        if path[index + 1] in self.adj_list[path[index]]:
            return self.is_valid_path_helper(path, index + 1)

        if path[index + 1] not in self.adj_list[path[index]]:
            return False

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        if len(path) == 0:
            return True

        for vertex in path:
            if vertex not in self.adj_list.keys():
                return False

            if vertex in self.adj_list.keys() and len(path) == 1:
                return True
        return self.is_valid_path_helper(path, 0)

    def rec_dfs(self, v_start, v_end, visited_vertices, stack):

        if len(stack) == 0:
            return

        if len(stack) != 0:
            v = stack.popleft()
            if v == v_end:
                visited_vertices.append(v)
                return

            if v not in visited_vertices:
                visited_vertices.append(v)
                self.adj_list[v].sort(reverse=True)

                for i in self.adj_list[v]:
                    if i not in visited_vertices:
                        stack.appendleft(i)

            self.rec_dfs(v_start, v_end, visited_vertices, stack)

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """

        visited_vertices = []
        stack = deque()
        stack.append(v_start)

        if v_start not in self.adj_list.keys():
            return []

        self.rec_dfs(v_start, v_end, visited_vertices, stack)
        return (visited_vertices)

    def rec_bfs(self, v_start, v_end, visited_vertices, queue):
        if len(queue) == 0:
            return

        if len(queue) != 0:
            v = queue.popleft()
            if v == v_end:
                visited_vertices.append(v)
                return

            if v not in visited_vertices:
                visited_vertices.append(v)
                self.adj_list[v].sort()

                for i in self.adj_list[v]:
                    if i not in visited_vertices:
                        queue.append(i)

            self.rec_bfs(v_start, v_end, visited_vertices, queue)

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        visited_vertices = []
        queue = deque()
        queue.append(v_start)

        if v_start not in self.adj_list.keys():
            return []

        self.rec_bfs(v_start, v_end, visited_vertices, queue)

        return (visited_vertices)

    def count_connected_components(self):
        """
        Return number of connected components in the graph
        """
        gv = self.get_vertices()
        counter = 0
        return self.rec_count_connected_components(gv, counter)

    def rec_count_connected_components(self, gv, counter):
        if len(gv) == 0:
            return counter

        if len(gv) != 0:
            dfs = self.dfs(gv[0])
            for i in dfs:
                if i in gv:
                    gv.remove(i)
            counter += 1
            return self.rec_count_connected_components(gv, counter)

    def dfs_mod_cycle(self, v_start):
        visited_vertices = []
        stack = deque()
        stack.append(v_start)
        parent = None
        if v_start not in self.adj_list.keys():
            return []
        return self.rec_dfs_mod_cycle(v_start, visited_vertices, stack, parent)

    def rec_dfs_mod_cycle(self, v_start, visited_vertices, stack, parent):
        if len(stack) == 0:
            return False
        if len(stack) != 0:
            v = stack.popleft()
            parent = v
            if v not in visited_vertices:
                visited_vertices.append(v)
                self.adj_list[v].sort(reverse=True)
                for i in self.adj_list[v]:
                    if i not in visited_vertices:
                        stack.appendleft(i)
                if parent in stack:
                    return True
            return self.rec_dfs_mod_cycle(v_start, visited_vertices, stack, parent)

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        path = self.get_vertices()
        index = 0
        v_start = path[index]
        return self.rec_has_cycle(v_start, index, path)

    def rec_has_cycle(self, v_start, index,
                      path):  # RECURSIVE FUNCTION WITHIN ANOTHER RECURSIVE FUNCTION HAHAHAHAHHAHAHAHAHAH
        if self.dfs_mod_cycle(v_start) is True:
            return True
        if self.dfs_mod_cycle(v_start) is False:
            index += 1
            if index > len(path) - 1:
                return False
            v_start = path[index]
            return self.rec_has_cycle(v_start, index, path)


if __name__ == '__main__':

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = UndirectedGraph()
    # print(g)
    #
    # for v in 'ABCDE':
    #     g.add_vertex(v)
    # print(g)
    #
    # g.add_vertex('A')
    # print(g)
    #
    # for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
    #     g.add_edge(u, v)
    # print(g)
    #
    # #
    # print("\nPDF - method remove_edge() / remove_vertex example 1")
    # print("----------------------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    # g.remove_vertex('DOES NOT EXIST')
    # g.remove_edge('A', 'B')
    # g.remove_edge('X', 'B')
    # print(g)
    # g.remove_vertex('D')
    # print(g)
    # #
    # #
    # print("\nPDF - method get_vertices() / get_edges() example 1")
    # print("---------------------------------------------------")
    # g = UndirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    #
    #
    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    # test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    # # test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '']
    # for path in test_cases:
    #     print(list(path), g.is_valid_path(list(path)))
    #
    #
    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = 'ABCDEGH'
    # for case in test_cases:
    #     print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    # print('-----')
    # for i in range(1, len(test_cases)):
    #     v1, v2 = test_cases[i], test_cases[-1 - i]
    #     print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')
    # #
    #
    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = 'ABCDEGH'
    # for case in test_cases:
    #     print(f'{case} DFS:{g.dfs(case)}')
    # print('-----')
    # for i in range(1, len(test_cases)):
    #     v1, v2 = test_cases[i], test_cases[-1 - i]
    #     print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    #
    # print("\nPDF - method count_connected_components() example 1")
    # print("---------------------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = (
    #     'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #     'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #     'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #     'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    # for case in test_cases:
    #     command, edge = case.split()
    #     u, v = edge
    #     g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    #     print(g.count_connected_components(), end=' ')
    # print()
    # #
    #
    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)

    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
