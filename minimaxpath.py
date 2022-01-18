"""Program for solving minimax path problem

Kruskal's algorithm is used first for finding the minimum spanning tree,
in which lies the minimax path. Then breadth first search algorithm and 
backtracking are used for finding the shortest path to the goal node.
"""

import time

fname = input("Enter file name: ")
file = open(fname)
lines = file.readlines()
file.close()

start_time = time.time()

#extracting information
vertices_N, edges_N = lines[0].split(' ')
vertices_N = int(vertices_N)
edges_N = int(edges_N)
goalstate = lines[edges_N+1]
goalstate = int(goalstate)
edges = []
for i in range(1, edges_N+1):
    x, y, z = lines[i].split(' ')
    edges.append((int(x), int(y), int(z)))
 
vertices = {}

def findset(u):
    if u != vertices[u]:
        vertices[u] = findset(vertices[u])
    return vertices[u]

def union(u, v):
    uu = findset(u)
    uv = findset(v)
    vertices[uu] = uv

def kruskal(edges, vn):
    global MST
    global MST_w
    MST = []
    MST_w = []
    for i in range(1, vn+1):    #creating separate sets
        vertices[i] = i 
    
    edges.sort(key=lambda x: x[2]) 
    for e in edges:
        if findset(e[0]) != findset(e[1]):
            MST.append((e[0], e[1]))
            MST_w.append(e)
            union(e[0],e[1])
    return MST


def bfs(graph, startNode, goal, n):
    #breadth first search algorithm
    visited = []
    queue = []
    visited.append(startNode)
    queue.append(startNode)
    route = []
    
    while queue: 
        x = queue.pop(0)
        if x == goal:
            return visited
        neighbours = []
        for i in range(0,len(graph)):   #finding neighbours for current node
            if x == graph[i][0]:
                neighbours.append(graph[i][1])
            elif x == graph[i][1]:
                neighbours.append(graph[i][0])
                if (graph[i][1]) == goal:
                    visited.append(graph[i][1])
                elif (graph[i][0]) == goal:
                    visited.append(graph[i][0])
                    return visited
        for neighbour in neighbours:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
    return "Path can not be found"
    
def backtrack(route, goal):
    path = []
    path.append(goal)
    x = goal
    
    for i in range(1,len(route)):
        if ((route[-i-1], x)) in MST or ((x, route[-i-1])) in MST:
            path.append(route[-i-1])
            x = route[-i-1]
    path.reverse()
    return path

x = kruskal(edges, vertices_N)
x.sort(key=lambda x: x[0])  
route = bfs(x, 1, goalstate, vertices_N)

if type(route) is not str:  #finding the weigths for shortest path
    route = backtrack(route, goalstate)
    route_edges = []
    height = []
    for i in range((len(route)-1)):
        route_edges.append((route[i], route[i+1]))
    for r_edge in route_edges:
        for mst_edge in MST_w: 
            if ((r_edge[0] == mst_edge[0]) and (r_edge[1] == mst_edge[1])) or ((r_edge[1] == mst_edge[0]) and (r_edge[0] == mst_edge[1])):
                height.append(mst_edge[2])
    max_height = max(height)
    
print("Final path: {} \nmaximum height: {}".format(route, max_height))
print("--- %s seconds ---" % (time.time() - start_time))