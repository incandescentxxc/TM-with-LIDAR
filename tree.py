from node import Node
from domain import Domain
from tin import TIN
from point import Point

import math
import numpy as np
import matplotlib.pyplot as plt

class Tree(object):
    '''Creates Class tree'''
    def __init__(self,c):
        self.__root = Node()
        self.__capacity = c

    def get_root(self):
        return self.__root

    def get_leaf_threshold(self):
        return self.__capacity

    def build_tree(self,tin):
        # first we insert the vertices of the TIN
        for i in range(tin.get_vertices_num()):
            print ("INSERT POINT %s"%tin.get_vertex(i))  ## you can use this line to check the vertex input. Can comment it out if you don't need it.
            self.insert_vertex(self.__root,0,tin.get_domain(),i,tin)
        # ADD THE CODE for inserting its triangles
        
        #  End of the build_tree() function

    def insert_vertex(self,node,node_label,node_domain,v_index,tin):
        if node_domain.contains_point(tin.get_vertex(v_index),tin.get_domain().get_max_point()):
            if node.is_leaf():
                if node.is_duplicate(v_index,tin): # if the inserting vertex is the same as one vertex in the tree.
                    return                          # do not insert it
                node.add_vertex(v_index) #update append list
                if node.overflow(self.__capacity):
                    # WE HAVE TO PERFORM A SPLIT OPERATION WHEN NUMBER OF VERTICES EXCEED CAPACITY
                    # current node become internal, and we initialize its children
                    node.init_children()
                    for i in node.get_vertices():
                        self.insert_vertex(node,node_label,node_domain,i,tin)
                    node.reset_vertices() #empty the list of the current node

            else: # otherwise we are visiting an INTERNAL node
                mid_point = node_domain.get_centroid()
                for i in range(4):
                    s_label,s_domain = node.compute_child_label_and_domain(i,node_label,node_domain,mid_point)
                    self.insert_vertex(node.get_child(i),s_label,s_domain,v_index,tin)

    def point_query(self, node, node_label, node_domain, search_point, tin):
        # node: Node object; node_label: int; node_domain: Domain object;search_point: Vertex object, the vertex you want to search
        # when point_query used in other functions for searching point:
        # node is the root of the tree,node_label is the node label of the root node(0), node_domain is the domain of the TIN(tin.get_domain()).
        # You will use this for identifying nodes containing the extreme vertices of a triangle
        #
        # This function will return the node that contains the input search_point.
        if node_domain.contains_point(search_point, tin.get_domain().get_max_point()):
            if node.is_leaf():
                isfound = False
                x = None  # x is the point id
                for i in node.get_vertices():  # for each point index in each node, if that point is equal to the query point, then it is found. Otherwise, it is not found.
                    if tin.get_vertex(i) == search_point: # here tin.get_vertex(i) and search_point are Vertex objects
                        isfound = True
                        x = i  # x is the point index that is equal to the search point.
                        print("Vertex　"+str(x)+" is in Node "+str(node_label))
                        break
                if isfound:
                    return node
                else:
                    return None
            else:  # Internal node
                ### we visit the children in the following order: NE -> NW -> SW -> SE
                mid_point = node_domain.get_centroid()
                s_label, s_domain = node.compute_child_label_and_domain(0, node_label, node_domain, mid_point)
                ret_node = self.point_query(node.get_child(0), s_label, s_domain, search_point, tin)
                if ret_node is not None:
                    return ret_node
                else:
                    s_label, s_domain = node.compute_child_label_and_domain(1, node_label, node_domain, mid_point)
                    ret_node = self.point_query(node.get_child(1), s_label, s_domain, search_point, tin)
                    if ret_node is not None:
                        return ret_node
                    else:
                        s_label, s_domain = node.compute_child_label_and_domain(2, node_label, node_domain, mid_point)
                        ret_node = self.point_query(node.get_child(2), s_label, s_domain, search_point, tin)
                        if ret_node is not None:
                            return ret_node
                        else:
                            s_label, s_domain = node.compute_child_label_and_domain(3, node_label, node_domain, mid_point)
                            ret_node = self.point_query(node.get_child(3), s_label, s_domain, search_point, tin)
                            return ret_node

    

    def get_points(self, tin, pts):
        """return xs,ys"""
        xs = list()
        ys = list()
        for v in pts:
            xs.append(tin.get_vertex(v).get_x())
            ys.append(tin.get_vertex(v).get_y())
        return xs,ys
    
    def get_pts_feature_values(self,tin, fid):
        vals=list()
        for v in range(tin.get_vertices_num()):
            ver = tin.get_vertex(v)
            #print(ver, fid,ver.get_fields_num() )
            #ver.print_fields()
            if fid >= ver.get_fields_num():
                sys.exit()
            else:
                vals.append(ver.get_field(fid))
        return vals
    

