#!/usr/bin/python3


from CS312Graph import *
import time


class NetworkRoutingSolver:
    def __init__( self ):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex

        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE

        path_edges = []
        total_length = 0
        node = self.network.nodes[self.source]
        edges_left = 3
        while edges_left > 0:
            edge = node.neighbors[2]
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            total_length += edge.length
            node = edge.dest
            edges_left -= 1
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        self.dijkstra(self.network.nodes[srcIndex])
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)


        t2 = time.time()
        return (t2-t1)

    def dijkstra(self, s):
        dist = {}
        prev = {}
        for node in self.network.nodes:
            dist[node] = float("Inf")
            prev[node] = None
        dist[s] = 0
        H = [x for x in self.network.nodes[::-1]]
        while H:
            u = H.pop()
            for neighbor in u.neighbors:
                if dist[neighbor.dest] > dist[u] + neighbor.length:
                    dist[neighbor.dest] = dist[u] + neighbor.length
                    prev[neighbor.dest] = u
                    self.decreasekey(H, neighbor, dist[u] + neighbor.length)

    def makequeue(self, start, nodes):
        pass


class BinaryMinHeap:
    def __init__(self, source, network):
        self.LEFT_BRANCH = 2
        self.RIGHT_BRANCH = 2
        self.heap = [None,]
        self.heap.append(source)
        self.end_position = 1
        self.root = 1
        for node in network:
            self.insert(node)

    def insert(self, node):
        self.heap.append(node)
        self.end_position += 1
        self.bubble_up(self.end_position)

    def right_child(self, position):
        return self.heap[2 * position + 1]

    def left_child(self, position):
        return self.heap[2 * position]

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

    def bubble_up(self, position):
        parent_index = self.parent_index(position)
        if parent_index <= 0:
            return
        child = self.heap[position]
        parent = self.parent(position)
        if self.parent(position) > child:
            child_index = position
            self.heap[parent_index] = child
            self.heap[child_index] = parent
            self.bubble_up(parent_index)

    def decrease_key(self, target, new_value):
        index = self.find(self.heap[self.root], target)
        self.heap[index] = new_value
        self.bubble_up(index)

    def delete_min(self):
        min_value = self.heap[1]
        max_value = self.heap.pop()
        self.heap[1] = max_value
        self.trickle_down(1)
        return min_value

    def side_next_position(self, position):
        if position == 2:
            return position
        if position == 3:
            return position
        else:
            return self.side_next_position(position // 2)

    def trickle_down(self, position):
        node = self.heap[position]
        rc, rc_index = self.right_child(position), self.right_child_index(position)
        lc, lc_index = self.left_child(position), self.left_child_index(position)
        if rc < lc:
            if node > rc:
                self.heap[rc_index] = node
                self.heap[position] = rc
                self.trickle_down(rc_index)
        elif lc < rc:
            if node > lc:
                self.heap[lc_index] = node
                self.heap[position] = lc
                self.trickle_down(lc_index)

    def find(self, current_index, target):
        if current_index > self.end_position:
            return float('-Inf')
        if self.heap[current_index] == target:
            return current_index
        else:
            return max(self.find(self.left_child(current_index), target), self.find(self.right_child(current_index), target))

    def __str__(self):
        return self.heap.__str__()



if __name__ == "__main__":
    nodes = [4,5,3,2,1]
    b = BinaryMinHeap(nodes[0], nodes[1:])
    b.delete_min()






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



