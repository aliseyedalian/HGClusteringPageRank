import sys
import ast
import networkx as nx
from operator import itemgetter

json_string = sys.argv[1]
adjacency_dict = ast.literal_eval(json_string)
G = nx.Graph(adjacency_dict)
index = nx.betweenness_centrality(G)
# reverse = False --> ascending                  
# reverse = True --> decsending                     
nodes_priority = [t[0] for t in sorted(index.items(),key= itemgetter(1),reverse=True)] 
print(nodes_priority)