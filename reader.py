import sys
import getopt

from tin import TIN
from vertex import Vertex
from triangle import Triangle
from domain import Domain

class Reader(object):
    # def __init__(self):

    # input file format: OFF
    def read_tin_file(self,url_in): # It will read the .off file and store the vertices into the global vertex array in a TIN object.
        #it will return a TIN object.
        # You should COMPLETE the code for reading and storing the triangles
        with open(url_in) as infile:
            tin = TIN()
            trash = infile.readline()
            line = (infile.readline()).split()
            vertices_num = int(line[0])  # store the number of vertices .
            # You should write code for getting the number of triangles from the file
            for l in range(vertices_num): # use vertices_num to decide how many lines will be read as vertices
                line = (infile.readline()).split() # split the line based on space separator
                v=Vertex(float(line[0]),float(line[1]),float(line[2])) # in each line, read input as x,y,z
                tin.add_vertex(v)
                if l == 0:
                    tin.set_domain(v,v)
                else:
                    tin.get_domain().resize(v)   # domain is determined by input vertices.
                    # You don't need to change domain when reading triangles
            ###### COMPLETE THE CODE for reading and storing the triangles.
            #
            #
            #
            #
            #
            #
            infile.close() # close the file after input.
            return tin
