from org.openide.util import Lookup
from org.gephi.graph.api import GraphController
import os

base_path = "D:/Documents/TDL/GRAFOS APLICADOS/Tema 3.- Redes y grafos, algoritmos/PEC3/tables/"
path_degree = base_path + "degree_distribution/"
path_weighted = base_path + "weighted_degree/"

if not os.path.exists(path_degree):
    os.makedirs(path_degree)
if not os.path.exists(path_weighted):
    os.makedirs(path_weighted)

graphController = Lookup.getDefault().lookup(GraphController)
graphModel = graphController.getGraphModel()
graph = graphModel.getGraph()
nodeTable = graphModel.getNodeTable()

col_mod = nodeTable.getColumn("modularity_class")
col_degree = nodeTable.getColumn("degree")
col_weighted = nodeTable.getColumn("weighted degree")

columns = []
for col in nodeTable:
    columns.append(col)

nodes = list(graph.getNodes())
communities = []

for n in nodes:
    value = n.getAttribute(col_mod)
    if value not in communities:
        communities.append(value)

print "Iniciando exportacion..."

for c in sorted(communities):

    community_nodes = []

    for n in nodes:
        if n.getAttribute(col_mod) == c:
            degree_val = n.getAttribute(col_degree)
            weighted_val = n.getAttribute(col_weighted)
            community_nodes.append((n, degree_val, weighted_val))

    if len(community_nodes) == 0:
        continue

    top_degree = sorted(community_nodes, key=lambda x: x[1], reverse=True)[:10]
    top_weighted = sorted(community_nodes, key=lambda x: x[2], reverse=True)[:10]

    # ----- EXPORT DEGREE -----
    f1 = open(path_degree + "comunidad_" + str(c) + "_top10_grado.csv", "w")

    header = []
    for col in columns:
        header.append(col.getTitle())
    f1.write(",".join(header) + "\n")

    for item in top_degree:
        n = item[0]
        row = []
        for col in columns:
            value = n.getAttribute(col)
            if value is None:
                value = ""
            value = str(value).replace(",", "")
            row.append(value)
        f1.write(",".join(row) + "\n")

    f1.close()

    # ----- EXPORT WEIGHTED -----
    f2 = open(path_weighted + "comunidad_" + str(c) + "_top10_pesos.csv", "w")

    f2.write(",".join(header) + "\n")

    for item in top_weighted:
        n = item[0]
        row = []
        for col in columns:
            value = n.getAttribute(col)
            if value is None:
                value = ""
            value = str(value).replace(",", "")
            row.append(value)
        f2.write(",".join(row) + "\n")

    f2.close()

    print "Comunidad", c, "exportada."

print "Proceso finalizado."
