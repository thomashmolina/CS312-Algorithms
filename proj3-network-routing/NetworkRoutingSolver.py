#!/usr/bin/python3


from CS312Graph import *
import time


class NetworkRoutingSolver:
    def __init__(self):
        pass

    def initializeNetwork(self, network):
        assert(type(network) == CS312Graph)
        self.network = network
        self.paths = None
        self.previous = None
        self.costs = None

    def getShortestPath(self, destIndex):
        self.dest = destIndex
        edges = []
        start_node, end_node = self.network.nodes[self.source], self.network.nodes[destIndex]
        while end_node is not None:
            prev_node = self.previous[end_node]
            edge = end_node.neighbors.index(prev_node)
            edges.append(edge)

        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE
    ''' 
    path_edges = []
    total_length = 0
    node = self.network.nodes[self.source]
    edges_left = 3
    while edges_left > 0:
    edge = node.neighbors[2]
    path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))
    total_length += edge.length
    node = edge.dest
    edges_left -= 1
    '''
    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        paths = self.dijkstra(self.network.nodes[srcIndex])
        self.previous = paths['previous']
        self.costs = paths['costs']
        t2 = time.time()
        return (t2-t1)

    def dijkstra(self, s):
        dist = {}
        prev = {}
        for node in self.network.nodes:
            dist[node] = float("Inf")
            prev[node] = None
        dist[s] = 0
        H = self.make_queue(self.network.nodes, dist)
        while len(H.heap) != 1:
            u = H.delete_min()[0]
            for neighbor in u.neighbors:
                if dist[neighbor.dest] > dist[u] + neighbor.length:
                    dist[neighbor.dest] = dist[u] + neighbor.length
                    prev[neighbor.dest] = u
                    H.decrease_key((neighbor.dest, dist[u] + neighbor.length), H.indicies[neighbor.dest])
        return {'costs': dist, 'previous': prev}

    def make_queue(self, nodes, dist):
        return BinaryMinHeap(nodes, dist)


class BinaryMinHeap:
    def __init__(self, network, dist_values):
        self.heap = [None,]
        self.end_position = 1
        self.root = 1
        self.indicies = {}
        for node in dist_values:
            self.insert(node, dist_values[node])

    def insert(self, node, length):
        if len(self.heap) == 1:
            self.heap.append((node, length))
            self.indicies[node] = 1
            return 1
        else:
            self.heap.append((node, length))
            self.bubble_up((node, length), len(self.heap)-1)

    def right_child(self, position):
        if 2 * position + 1 < len(self.heap):
            return self.heap[2 * position + 1]
        return None

    def left_child(self, position):
        if 2 * position < len(self.heap):
            return self.heap[2 * position]
        return None

    def parent(self, position):
        return self.heap[position // 2]

    @staticmethod
    def parent_index(position):
        return position // 2

    @staticmethod
    def right_child_index(position):
        return 2 * position + 1

    @staticmethod
    def left_child_index(position):
        return 2 * position

    def bubble_up(self, x, i):
        p = i//2
        while i != 1 and self.heap[p][1] > x[1]:
            self.heap[i] = self.heap[p]
            self.indicies[self.heap[i][0]] = p
            self.indicies[self.heap[p][0]] = i
            i = p
            p = i // 2
        self.heap[i] = x
        self.indicies[self.heap[i][0]] = i

    def decrease_key(self, x, i):
        self.heap[self.indicies[x[0]]] = x
        self.bubble_up(x, i)

    def delete_min(self):
        if len(self.heap) == 1:
            return None
        else:
            min_value = self.heap[1]
            max_value = self.heap.pop()
            if len(self.heap) > 1:
                self.heap[1] = max_value
                self.sift_down(max_value, 1)
            return min_value

    def sift_down(self, x, i):
        c = self.min_child(i)
        while c != 0 and self.heap[c][1] < x[1]:
            self.heap[i] = (self.heap[c][0], self.heap[c][1])
            i = c
            c = self.min_child(i)
        self.heap[i] = x

    def pop(self):
        return self.heap.pop()

    def min_child(self, index): # returns the index of the smallest child of index
        if 2 * index > len(self.heap):
            return 0
        else:
            lc = self.left_child(index)
            rc = self.right_child(index)
            if rc is None and lc is None:
                return 0
            if rc is None:
                return self.left_child_index(index)
            if lc[1] < rc[1]:
                return self.left_child_index(index)
            elif lc[1] > rc[1]:
                return self.right_child_index(index)
            else:
                return self.left_child_index(index)

    def __str__(self):
        return self.heap.__str__()



if __name__ == "__main__":
    nodes = [4, 5, 3, 2, 1]
    b = BinaryMinHeap(nodes[0], nodes[1:])
    b.decrease_key(-1, 2)






def bfs(graph, starting_node):
    visited = [False]  * len(graph)
    queue = [starting_node]
    visited[starting_node] = True

    while queue:
        starting_node = queue.pop(0)
        for i in graph[starting_node]:
            if not visited[i]:
                queue.append(i)
                visited[i] = True

def dfs(graph, starting_node):
    visited = [False] * len(graph)
    queue = [starting_node]
    visited[starting_node] = True
    index, number = [0, 0]
    visits = [(0, 0)] * len(graph)
    previsit(visits, index, 0)
    for neighbor in starting_node.neighbors:
        if not visited[neighbor]:
            index += 1
            dfs(graph, neighbor)
            number += 1
    postvisit(visits, index, number)


def previsit(total_visits, index, number):
    total_visits[index][0] = number

def postvisit(total_visits, index, number):

    total_visits[index][1] = number



