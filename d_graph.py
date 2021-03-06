from collections import deque
import heapq


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Add vertex
        """
        self.v_count += 1
        matrix = [[0 for i in range(self.v_count)] for g in range(self.v_count)]
        self.adj_matrix = matrix

        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """for src, dst, weight in edges:for src, dst, weight in edges:
        Add edge
        """
        if src == dst:
            return

        if weight < 0:
            return

        if src > self.v_count - 1 and dst > self.v_count - 1:
            return

        if src > self.v_count - 1 or dst > self.v_count - 1:
            return

        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Remove edge
        """
        if src < 0 or dst < 0:
            return

        if src > self.v_count - 1 or dst > self.v_count - 1:
            return

        if src == dst:
            return

        if self.adj_matrix[src][dst] == 0:
            return
        if self.adj_matrix[src][dst] != 0:
            self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Get all vertices
        """
        vertices_list = []
        for i in range(self.v_count):
            vertices_list.append(i)
        return vertices_list

    def get_edges(self) -> []:
        """
        Get all edges
        """
        edge_list = []
        for row in range(len(self.adj_matrix)):
            for col in range(len(self.adj_matrix[row])):
                if self.adj_matrix[row][col] != 0:
                    weight = self.adj_matrix[row][col]
                    output = (row, col, weight)
                    edge_list.append(output)
        return edge_list

    def rec_is_valid_path(self, path, index, next, counter1, counter2):

        if self.adj_matrix[index][next] != 0:
            counter1 += 1
            counter2 += 1

            if counter2 == len(path):  # base case here
                return True

            index = path[counter1]
            next = path[counter2]
            return self.rec_is_valid_path(path, index, next, counter1, counter2)

        else:
            return False

    def is_valid_path(self, path: []) -> bool:
        """
        Check if valid path
        """
        if len(path) == 0:
            return True

        if len(path) == 1:
            return True

        index = path[0]
        next = path[1]

        return self.rec_is_valid_path(path, index, next, 0, 1)

    def dfs(self, v_start, v_end=None) -> []:
        """
        DFS search
        """
        visited_vertices = []
        stack = deque()
        stack.append(v_start)

        g = self.get_vertices()
        if v_start not in g:
            return []

        self.rec_dfs(v_start, v_end, visited_vertices, stack)
        return visited_vertices

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

                for i in range(len(self.adj_matrix[v]) - 1, -1, -1):  # append larger to smaller numbers
                    if self.adj_matrix[v][i] != 0:
                        stack.appendleft(i)  # append left then pop left = LIFO

            self.rec_dfs(v_start, v_end, visited_vertices, stack)

    def bfs(self, v_start, v_end=None) -> []:
        """
        BFS search
        """
        visited_vertices = []
        queue = deque()
        queue.append(v_start)

        g = self.get_vertices()
        if v_start not in g:
            return []

        self.rec_bfs(v_start, v_end, visited_vertices, queue)
        return visited_vertices

    def rec_bfs(self, v_start, v_end, visited_vertices, queue):

        if len(queue) == 0:
            return

        if len(queue) != 0:
            v = queue.pop()

            if v == v_end:
                visited_vertices.append(v)
                return

            if v not in visited_vertices:
                visited_vertices.append(v)

                for i in range(len(self.adj_matrix[v])):  # append smaller to larger numbers
                    if self.adj_matrix[v][i] != 0:
                        queue.appendleft(i)  # append left + pop right = FIFO

            self.rec_bfs(v_start, v_end, visited_vertices, queue)

    def dfs_mod_cycle(self, v_start):
        visited_vertices = []
        stack = deque()
        stack.append(v_start)
        parent = None

        g = self.get_vertices()
        if v_start not in g:
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

                counter = 0
                for i in range(len(self.adj_matrix[v]) - 1, -1, -1):  # append larger to smaller numbers

                    if self.adj_matrix[v][i] != 0:
                        stack.appendleft(i)
                        if i in visited_vertices and i != parent:
                            return True
                    if self.adj_matrix[v][i] == 0:
                        counter += 1
                        if counter == len(self.adj_matrix):
                            return False

            return self.rec_dfs_mod_cycle(v_start, visited_vertices, stack, parent)

    def has_cycle(self):
        """
        Check if cyclic
        """

        path = self.get_vertices()
        index = 0
        v_start = path[index]
        return self.rec_has_cycle(v_start, index, path)


    def rec_has_cycle(self, v_start, index, path):
        if self.dfs_mod_cycle(v_start) is True:
            return True
        if self.dfs_mod_cycle(v_start) is False:
            index += 1
            if index > len(path) - 1:
                return False
            v_start = path[index]
            return self.rec_has_cycle(v_start, index, path)


    def dijkstra(self, src: int) -> []:
        """
        dijkstra check
        """
        visited_vertices = dict()
        priority_queue = []
        priority_queue.append((0, src))
        heapq.heapify(priority_queue)

        if src < 0:
            return None
        if src > len(self.adj_matrix):
            return None

        self.rec_dijkstra(src, visited_vertices, priority_queue)

        return_list = [float('inf') for i in range(self.v_count)]
        for i in visited_vertices.keys():
            return_list[i] = (visited_vertices[i])
        return return_list

    def rec_dijkstra(self, src, visited_vertices, priority_queue):

        if len(priority_queue) == 0:
            return
        if len(priority_queue) != 0:
            z = heapq.heappop(priority_queue)
            v = z[1]
            d = z[0]

            if v not in visited_vertices.keys():
                visited_vertices[v] = d

                for i in range(len(self.adj_matrix[v])):
                    if self.adj_matrix[v][i] != 0:
                        di = self.adj_matrix[v][i]
                        total_d = di + d
                        heapq.heappush(priority_queue, (total_d, i))

            return self.rec_dijkstra(src, visited_vertices, priority_queue)




if __name__ == '__main__':

    # g = DirectedGraph()
    # for i in range(13):
    #     g.add_vertex()
    #
    # edges = [(2, 10, 11), (7, 9, 3), (9, 6, 11), (11, 2, 15), ]
    # for src, dst, weight in edges:
    #     g.add_edge(src, dst, weight)
    # print(g)
    #
    # list = [(9, 4), (0, 3), (4, 9), (2, 10), (0, 2), (8, 3), (8, 7), (0, 7), (7, 8), (2, 5), (5, 11), (2, 7), (7, 11),
    #         (10, 2), (1, 10), (2, 0), (12, 8), (1, 5), (0, 10), (0, 12), (8, 4), (2, 2)]
    # for src, dst, in list:
    #     g.remove_edge(src, dst)
    # print(g)
    # print("AAAAAAAA")
    # print(g)

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = DirectedGraph()
    # print(g)
    # for _ in range(5):
    #     g.add_vertex()
    # print(g)
    #
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # for src, dst, weight in edges:
    #     g.add_edge(src, dst, weight)
    # print(g)
    #
    # print("\nPDF - method get_edges() example 1")
    # print("----------------------------------")
    # g = DirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # #
    #
    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    # for path in test_cases:
    #     print(path, g.is_valid_path(path))

    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # for start in range(5):
    #     print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')
    #
    #
    # print("\nPDF - method has_cycle() example 1")
    # print("----------------------------------")
    # # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    # #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # edges = [(0, 1, 10), (1,3,1), (1, 4, 15), (2, 1, 23),
    #          (2,3,1), (4,3,1)]
    # g = DirectedGraph(edges)

    # edges_to_remove = [(4,0)]
    # edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    # for src, dst in edges_to_remove:

    # print(g.get_edges(), g.has_cycle(), sep='\n')
    # print(g.__str__())
    #
    # edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    # for src, dst in edges_to_add:
    #     g.add_edge(src, dst)
    #     print(g.get_edges(), g.has_cycle(), sep='\n')
    # print('\n', g)




    # print("\nPDF - method has_cycle() example 1")
    # print("----------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    #
    # edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    # for src, dst in edges_to_remove:
    #     g.remove_edge(src, dst)
    #     print(g.get_edges(), g.has_cycle(), sep='\n')
    #
    # edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    # for src, dst in edges_to_add:
    #     g.add_edge(src, dst)
    #     print(g.get_edges(), g.has_cycle(), sep='\n')
    # print('\n', g)


    # print("\nPDF - dijkstra() example 1")
    # print("--------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # for i in range(5):
    #     print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    # g.remove_edge(4, 3)
    # print('\n', g)
    # for i in range(5):
    #     print(f'DIJKSTRA {i} {g.dijkstra(i)}')
