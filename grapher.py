import csv
import networkx
import matplotlib.pyplot as plt

from networkx.drawing.nx_pydot import write_dot

def GetNextPage(page_row_data):
  with open('wiki_connections', 'r') as stupid:
    data = csv.reader(stupid)
    for r in data:
      if r[0] == "https://en.wikipedia.org" + page_row_data[2]:
        return r
    return False

with open("wiki_connections", 'r') as database_file_reader:
  data = csv.reader(database_file_reader)
  thing = []
  for row in data:
    page_row_data = GetNextPage(row)
    if page_row_data:
      thing.append((row[1], page_row_data[1]))

  graph=networkx.Graph()
  graph.add_edges_from(thing)
  networkx.draw_networkx(graph)
  plt.show()

