import os
import networkx as nx

class Files:
  def __init__(self, file=' '):
    self.file = file

  def read_graph_file(self, cut_graph_file, cut_graph, cut_number):
    RG = nx.Graph()
    with open(self.file) as f:
      lines = f.readlines()

    cut = len(lines)
    if(cut_graph):
      cut -= (cut_number +1)
    cut_list = []
    for line in lines:
      v1 =int(line.split(", ")[0]) # node 1
      v2 =int(line.split(", ")[1]) # node 2
      w = float(line.split(", ")[2]) # weight

      if(cut >= 0):
        RG.add_edge(v1, v2, weight = w) # include two node and your weight
        cut -=1
        if(cut_graph):
          cut_graph_file.save_graph_data(v1, v2, w)

      else:
        if(w == -1):
          v1 =int(line.split(", ")[0]) # node 1
          v2 =int(line.split(", ")[1]) # node 2
          if(v1 <= v2):
            if(not (v2 in cut_list)):
              RG.add_node(v1)
              cut_graph_file.save_graph_data(v1, ' ', ' ')
              cut_list.append(v2)
              cut -=1
          else:
            if(not (v1 in cut_list)):
              RG.add_node(v2)
              cut_graph_file.save_graph_data(v2, ' ', ' ')
              cut_list.append(v1)
              cut -=1
    return RG

  def create_folder(self, folder_name):
    if not os.path.isdir(f"../models/{folder_name}"):
        os.makedirs(f"../models/{folder_name}")

  def save_graph_data(self, v1, v2, weight):
    f = open(self.file, "a")
    if(v2==' '):
      data = "{}\n".format(v1)
    elif(weight == ".jpg"):
      data = "{}{}\n".format(v1, weight)
    else:
      data = "{}, {}, {}\n".format(v1, v2, weight)
    f.write(data)
    f.close()