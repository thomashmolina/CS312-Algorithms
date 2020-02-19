class Graph:
    def __init__(self):
        self.verticies = {}

    def add_vertex(self, parent: str, child: str, weight: int):
        if parent not in self.verticies:
            self.verticies[parent] = [(child, weight)]
        else:
            self.verticies[parent].append((child, weight))

    def __str__(self):
        return self.verticies.__str__()

    def __iter__(self):
        return self.verticies.__iter__()


def dijkstra(G, l, s):
        pass
        # TODO initialize all distances to infinity



if __name__ == "__main__":
    simple_graph = [("a", "b", 2), ("b", "c", 4), ("c", "d", 3)]
    G = Graph()
    for v in simple_graph:
        p, c, w = v[0], v[1], v[2]
        G.add_vertex(p, c, w)
    print(G)


