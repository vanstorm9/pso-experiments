import sys
import matplotlib.pyplot as plt
from pprint import pprint

#dict to label points
mylabel = {1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H'}

#dict to derive coordinates
mylabel2 = {
         'A':(0,5),
         'B':(1,0),
         'C':(5,1),
         'D':(2,4),
         'E':(3,6),
         'F':(0,7),
         'G':(4,8),
         'H':(6,2)
           }
#Adjancency and State Matrix
Adj_Matrix = [[0, 20, 0, 0, 0, 0, 15, 0],
             [20, 0, 8, 9, 0, 0, 0, 0],
             [0,  8,  0,  6, 15, 0, 0, 10],
             [0, 9, 6, 0, 7, 0, 0, 0],
             [0, 0, 15, 7, 0, 22, 18, 0],
             [0, 0, 0, 0, 22, 0, 0, 0],
             [15, 0, 0, 0, 18, 0, 0, 0],
             [0, 0, 10, 0, 0, 0, 0, 0]]

xCoord=[mylabel2[k][0] for k in sorted(mylabel2)]
yCoord=[mylabel2[k][1] for k in sorted(mylabel2)]
plt.plot(xCoord, yCoord, 'bo')
plt.axis([-1, 7, -1, 9])
for i in xrange(8):
    plt.text(xCoord[i]-0.5, yCoord[i], mylabel[i+1])
for i in xrange(8):
    for j in xrange(8):
        if Adj_Matrix[i][j]:
            plt.plot([xCoord[i], xCoord[j]],[yCoord[i], yCoord[j]], 'b')
#Dijkstra Algorithm
def dijkstra(graph,start,target):
    inf = reduce(lambda x,y: x+y,(i[1] for u in graph for i in graph[u]))
    dist = dict.fromkeys(graph,inf)
    prev = dict.fromkeys(graph)
    q = graph.keys()
    dist[start] = 0
    while q:
        u = min(q, key=lambda x: dist[x])
        q.remove(u)
        for v,w in graph[u]:
            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
    #”way”
    trav = []
    temp = target
    while temp != start:
        trav.append(prev[temp])
        temp = prev[temp]
    trav.reverse()
    trav.append(target)
    return " -> ".join(trav),dist[target]

graph = {
    'A' : [('B',20), ('G', 15)],
    'B' : [('A', 20),('C', 8), ('D', 9)],
    'C' : [('B', 8),('D', 6), ('E', 15), ('H', 10)],
    'D' : [('B', 9),('C', 6),('E', 7)],
    'E' : [('C', 15),('D', 7),('F', 22),('G', 18)],
    'F' : [('E', 22)],
    'G' : [('A', 15),('E', 18)],
    'H' : [('C', 10)]
    }
traverse, dist = dijkstra(graph,'F','H')
print traverse
#Drawing of coordinates
mydrawing = traverse.split('-> ')
plt.plot([ mylabel2[n.rstrip()][0] for n in mydrawing ],[ mylabel2[n.rstrip()][1] for n in mydrawing])
print "Distance:",dist
plt.show()

