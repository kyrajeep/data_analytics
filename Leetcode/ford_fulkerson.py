# do a dfs or bfs for a residual graph

from collections import defaultdict
import graphlib

class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.ROW = len(graph)
        #print(self.ROW)

    def ford_fulkerson(self, source, sink):
        parent = [-1] * self.ROW
        max_flow = 0
        
        while self.bfs(source, sink, parent):
            flow = float("Inf")
            s = sink
            while(s != source):
                flow = min(flow, self.graph[parent[s]][s])
                s = parent[s]
            max_flow += flow
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= flow
                self.graph[v][u] += flow
                v = parent[v]
        return max_flow

    def bfs(self, s, t, parent):
        # indicate which node has been visited
        visited = [False] * (self.ROW)
        queue = []
        queue.append(s)
        visited[s] = True
        while queue:
            u = queue.pop(0)
            for index, val in enumerate(self.graph[u]):
                if visited[index] == False and val > 0:
                    queue.append(index)
                    visited[index] = True
                    parent[index] = u
                    if index == t:
                        return True
        return False



graph = [[1, 2], [0, 2, 100], [0, 1, 100]]
source = 0
sink = 100
flow = Graph(graph)
print(flow.ford_fulkerson(source, sink))