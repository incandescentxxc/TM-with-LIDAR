from domain import Domain
from triangle import Triangle
from point import Point

# children legend:
#   ne = 0
#   nw = 1
#   sw = 2
#   se = 3

class Node(object):
    '''Creates Class node'''
    def __init__(self):
        self.__vertex_ids = list() #indices of points
        self.__triangle_ids = list() #indices of triangles
        self.__children = None # a list of Node type objects. Equals to None when it is a leaf node.
        # When the current node is INTERNAL:
        # children[0]:ne quadrant  children[1]:nw quadrant children[2]:sw quadrant children[3]:se quadrant


    def add_vertex(self,id):  # When you add a vertex to a node, you add the index of it.
        # Here the id is the index of the Vertex on the global list
        # Should implement similar function for adding triangle
        self.__vertex_ids.append(id)
    def add_triangle(self,id): # When you add a triangle to a node, you add the index of it.
        # Here the id is the index of the Vertex on the global list
        self.__triangle_ids.append(id)

    def init_children(self): # initialize four empty Nodes as the children.
        self.__children = [Node() for _ in range(4)]

    def get_child(self,i): # it returns a Node object children[i] according to the input i from 0 to 3.
        return self.__children[i]

    def reset_vertices(self):    # remove all vertices ids in the vertex list of the node
        self.__vertex_ids = list()

    def overflow(self,capacity):  # if the number of vertices exceed the capacity
        return len(self.__vertex_ids) > capacity

    def compute_child_label_and_domain(self,child_position,node_label,node_domain,mid_point): # Compute subdivision and labels of four children
        if child_position == 0: # "ne":
            return 4*node_label+1,Domain(mid_point,node_domain.get_max_point())
        elif child_position == 1: # "nw":
            min = Point(node_domain.get_min_point().get_x(),mid_point.get_y())
            max = Point(mid_point.get_x(),node_domain.get_max_point().get_y())
            return 4*node_label+2,Domain(min,max)
        elif child_position == 2: # "sw":
            return 4*node_label+3,Domain(node_domain.get_min_point(),mid_point)
        elif child_position == 3: # "se":
            min = Point(mid_point.get_x(),node_domain.get_min_point().get_y())
            max = Point(node_domain.get_max_point().get_x(),mid_point.get_y())
            return 4*node_label+4,Domain(min,max)
        else:
            return None,None # #


    def is_duplicate(self, v_index, tin):   # vertex with index v_index has the same x,y coordinates as an existing vertex in the node
        for i in self.get_vertices():# check the vertices in this node to see if there is any vertex with same x,y coordinates as the inserting vertex
            if tin.get_vertex(i) == tin.get_vertex(v_index): # == for vertices is based on the x,y coordinates
                return True
        return False


    def get_vertices(self): # returns the list of vertex ids. Should implement similar function for triangles.
        return self.__vertex_ids
    
    def get_triangles(self): # returns the list of triangle ids.
        return self.__triangle_ids

    def get_vertices_num(self):
        return len(self.__vertex_ids)

    def is_leaf(self): # returns True if the node is leaf node, otherwise returns False
        return self.__children == None