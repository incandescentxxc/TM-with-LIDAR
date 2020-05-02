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
        for i in range(tin.get_tris_num()):
            print("INSERT TRIANGLES " + str(tin.get_tris(i)))
            self.insert_triangle(self.__root,0,tin.get_domain(),i,tin)
        print("START TRIANGLE PR")
        self.pre_order(self.__root,0)
        print("END TRIANGLE PR")
        #  End of the build_tree() function

    # the driver function to write the output required to the files
    def writeOutput(self, tin, task):
        curvature_dict={}
        roughness_dict = {}
        maximum_vertices =[]
        self.getRoughandMax(self.__root,tin,roughness_dict, maximum_vertices)
        self.calCurvature(self.__root, tin, curvature_dict)
        maximum_vertices = sorted(maximum_vertices)
        roughnessList = []
        curvatureList = []
        # write to files
        if (task == 0 or task == 1):
            rough_file = "roughness.txt" 
            with open(rough_file,'w') as ofs:
                for i in range(len(roughness_dict)):
                    ofs.write("{} {}\n".format(i, roughness_dict[i]))
                    roughnessList.append(roughness_dict[i])
            curvature_file = "curvature.txt"
            with open(curvature_file,'w') as cur:
                for i in range(len(curvature_dict)):
                    cur.write("{} {}\n".format(i, curvature_dict[i]))
                    curvatureList.append(curvature_dict[i])
        if (task == 0 or task == 2):
            maximum_file = "maximum.txt"
            with open(maximum_file,'w') as maxf:
                maxf.write("{}\n".format(len(maximum_vertices)))
                for i in range(len(maximum_vertices)):
                    maxf.write("{} ".format(maximum_vertices[i]))
        return roughnessList, curvatureList, maximum_vertices


    def pre_order(self,node,node_label):
        if(node==None):
            return 
        else:
            typeNode = "INTERNAL LEAF"
            if (node.is_leaf()): # FULL LEAF or EMPTY LEAF
                if(node.get_vertices_num() == 0):
                    typeNode = "EMPTY LEAF"
                else:
                    typeNode = "FULL LEAF"
            print(str(node_label) + " " + typeNode)
            if(typeNode == "FULL LEAF"):
                vertices = node.get_vertices()
                tris = node.get_triangles()
                print("  V " +  str(len(vertices)) + " " + str(vertices))
                print("  T " + str(len(tris)) + " " + str(tris))
            for i in range(4): # for the four children
                if(node.is_leaf()):
                    self.pre_order(None, 4*node_label+i+1)
                else:
                    self.pre_order(node.get_child(i),4*node_label+i+1)

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

    def insert_triangle(self,node,node_label,node_domain,t_index,tin):
        tri = tin.get_tris(t_index) # get the triangle (v1,v2,v3)
        print("INSERT TRIANGLE " + str(t_index) + " - " +  str(tri[0]) + " " + str(tri[1]) + " " + str(tri[2]))
        for i in range(3): # three extreme vertices
            v_index = tri[i] # get the index of the triangle vertex
            vertex = tin.get_vertex(v_index) # get the corresponding vertex object
            node_to_insert = self.point_query(node, node_label, node_domain, vertex, tin) # get the node to be inserted
            if(t_index not in node_to_insert.get_triangles()): # if not already existing    
                node_to_insert.add_triangle(t_index) # insert the triangle to the node

    # iterate the tree to calculate and store the roughness an maximum (whether maximum node) into a dictionary
    def getRoughandMax(self, node, tin, roughness_dict, maximum_vertices):
        if(node == None):
            return 
        else:
            if (node.is_leaf()): # FULL LEAF or EMPTY LEAF
                if(node.get_vertices_num() == 0): # Empty
                    pass
                else:
                    nodeVT = node.get_NodeVT(tin)
                    nodeVV = node.get_NodeVV(nodeVT,tin)# e.g. nodeVV = {1:{13,42,10,23}, 3:{12,13,34}}
                    # in this way, we didn't store all VV relationships. Instead, we just calculate the roughness/maximum of
                    # a certain vertex when travsersing the node that contains it
                    self.calRoughandMax(tin,nodeVV,roughness_dict,maximum_vertices)
            for i in range(4): # for the four children
                if(node.is_leaf()):
                    self.getRoughandMax(None,tin,roughness_dict, maximum_vertices)
                else:
                    self.getRoughandMax(node.get_child(i), tin, roughness_dict, maximum_vertices)

        # calculate roughness and maximum given the tin and node VV relationships
    def calRoughandMax(self, tin, nodeVV, roughness_dict, maximum_vertices):
        for key, value in nodeVV.items():
            ele_mean = 0
            dev = 0
            current_ele = tin.get_vertex(key).get_z()
            flag = True
            for vertex in value:
                vertex_ele = tin.get_vertex(vertex).get_z()
                ele_mean += vertex_ele
                if(flag and vertex_ele > current_ele):
                    flag = False  
            ele_mean /= len(value)
            for vertex in value:
                dev += (tin.get_vertex(vertex).get_z() - ele_mean)**2
            dev = (dev/len(value))**(0.5)
            roughness_dict[key] = round(dev,2)
            if(flag): # if the vertex is the maximum
                maximum_vertices.append(key)

    def calCurvature(self, node, tin, cur_dict):
        if(node == None):
            return 
        else:
            if (node.is_leaf()): # FULL LEAF or EMPTY LEAF
                if(node.get_vertices_num() == 0): # EMPTY
                    pass
                else:
                    nodeVT = node.get_NodeVT(tin) # e.g. nodeVT = {1:[12,3,4], 3:[1,2,9]}
                    # finished getting VT relationships
                    for key, value in nodeVT.items():
                        theta = 0
                        dupList = [] # this list is used to identify whethere there is duplication for neighboor
                        for tri in value:
                            v1, v3 = self.findOtherTwoVertices(key,tin.get_tris(tri))
                            theta += tin.get_vertex(key).angle(tin.get_vertex(v1),tin.get_vertex(v3)) # the angle at v in single triangle
                            if v1 not in dupList:
                                dupList.append(v1)
                            else:
                                dupList.remove(v1)
                            if v3 not in dupList:
                                dupList.append(v3)
                            else:
                                dupList.remove(v3)
                        # by this time, the dupList should be empty if the vertex we are checking is INTERNAL
                        if (len(dupList) == 0): # INTERNAL
                            curvature = 2*math.pi - theta
                        else: # BOUNDARY
                            curvature = math.pi - theta
                        cur_dict[key] = round(curvature,2)
            for i in range(4): # for the four children
                if(node.is_leaf()):
                    self.calCurvature(None, tin, cur_dict)
                else:
                    self.calCurvature(node.get_child(i), tin, cur_dict)

    # return another two vertices given one vertex
    def findOtherTwoVertices(self, vertex, triangle):
        others = []
        for i in range(3):
            others.append(triangle[i])
        others.remove(vertex)
        return others[0], others[1]

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
    

