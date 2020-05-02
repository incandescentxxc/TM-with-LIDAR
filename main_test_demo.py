#!/usr/bin/python3
"""
Demo.
Authors:
Xin Xu: xinxu629@umd.edu
Yunting Song: ytsong@terpmail.umd.edu 
Apr-06-2020
"""
import sys
import os

from reader import Reader

from tin import TIN
from tree import Tree
from point import Point

# generate TIN
from scipy.spatial import Delaunay 

# plot
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D  
from matplotlib.ticker import LinearLocator, FormatStrFormatter


def generate_TIN(pts_file):
    '''
    Generate TIN from input point file.
    Return
    tin_file: name of TIN .off file
    points1: updated 2D points (x,y). each pair of (x,y) is unique
    zs1: updated z values of points, in the same order of points1
    tris: triangles of TIN. each triangle is saved as [vid1, vid2, vid3]. vid is point index based on points1
    '''
    points = np.empty(shape=[0, 2])
    zs=list()
    with open(pts_file) as infile:
        lines_num= infile.readline().strip()
        lines_num=int(lines_num) # how many points we have
        for l in range(lines_num):
            line = (infile.readline()).split() # get three values of the point [x, y, z]
            v1 = float(line[0])
            v2 = float(line[1])
            existed_p = False
            for p in points: # see if there is repeated points already
                if p[0]==v1 and p[1]==v2:
                    existed_p = True
                    break
            if existed_p == False:
                points = np.append(points, [[v1,v2]], axis=0) # add points. note the np-array
                zs.append(float(line[2])) # add z value of this point into zs
    
    triangles = Delaunay(points) # get the results of triangulation
    
    tris = np.empty(shape=[0, 3]) # initiate the np array of storing triangles
    used_pts = set()
    for tri in triangles.simplices: # tri: e.g.[2,3,0], where the value is the index of the point in points array
        used_pts.add(tri[0])
        used_pts.add(tri[1])
        used_pts.add(tri[2])
    o2n = dict()
    n2o = list()
    zs1 = list()
    points1= np.empty(shape=[0, 2])
    for pid in used_pts: # pid is just the index referring to the point in points array
        points1 = np.append(points1,[[points[pid][0], points[pid][1]]],axis=0)
        o2n[pid] = len(points1)-1
        n2o.append(pid)
        zs1.append(zs[pid])
    for tri in triangles.simplices:
        v1 = tri[0]
        v2 = tri[1]
        v3 = tri[2]
        nv1 = o2n[v1]
        nv2 = o2n[v2]
        nv3 = o2n[v3]
        tris = np.append(tris,[[nv1, nv2, nv3]],axis=0)
   
   # output TIN file, Note:  you can rename the file name
    tin_file = "pts-dt.off" 
    with open(tin_file,'w') as ofs:
        ofs.write("OFF\n")
        ofs.write("{} {} 0\n".format(len(points1), len(tris)))
        for pid in range(len(points1)):
            ofs.write("{} {} {}\n".format(points[pid][0], points[pid][1],zs1[pid]))
        for tri in tris:
            ofs.write("3 {} {} {}\n".format(int(tri[0]), int(tri[1]), int(tri[2])))
    return tin_file, points1, zs1, tris


def plot_tin_with_marks(xs,ys,zs,tris,vals,mxs,mys,mzs,filename="test"):
    """
    Plot TIN 3D with markers. TIN is colored  based on values of each triangle. The triangle value is the  average value of 3 extreme points.
    Inputs:
    xs,ys,zs: lists of the same size. Points.
    (xs[i],ys[i], zs[i]) present a point
    tris: np.array. triangles. each triangle is presented as [vid1, vid2, vid3]. vid is point index.
    vals: list. values of points with the same order as points.
    mxs,mys,mzs: lists. Markers
    (mxs[i],mys[i], mzs[i]) present a marker
    filename: output figure name.
    """
    tri_avg = []
    for tri in tris:
        v1 = vals[int(tri[0])]
        v2 =  vals[int(tri[1])]
        v3 =  vals[int(tri[2])]
        v  = (v1+ v2 + v3) / 3
        tri_avg.append(v)
    vals_np = np.array(vals)
    zs_np = np.array(zs)
    triang = mtri.Triangulation(xs, ys, tris)
    maskedTris = triang.get_masked_triangles()
    xt = triang.x[maskedTris]
    yt = triang.y[maskedTris]
    zt = zs_np[maskedTris]
    verts = np.stack((xt, yt,zt), axis=-1)
    norm = cm.colors.Normalize(vmin=min(tri_avg), vmax=max(tri_avg))
    nm = norm(tri_avg)
    
    my_col = cm.jet(nm)
    newcmp = cm.colors.ListedColormap(my_col)
    
    collection = Poly3DCollection(verts)
    collection.set_facecolor(my_col)

    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.gca(projection='3d')
    
    ax.add_collection(collection)
    # add markers
    ax.scatter(mxs, mys, mzs, c='r', marker='^', s = 40)
    
    ax.set_title(filename)
    ax.set_xlim3d(min(xs), max(xs))
    ax.set_xlabel('X')
    ax.set_ylim3d(min(ys), max(ys))
    ax.set_ylabel('Y')
    ax.set_zlim3d(min(zs), max(zs))
    ax.set_zlabel('Z')
    ax.autoscale_view()
    
    m = cm.ScalarMappable(cmap=cm.jet, norm=norm)
    m.set_array([])
    fig.colorbar(m)
    
    # output tin figure
    plt.savefig(filename+".png", dpi=96)
    plt.show()
    
if __name__ == '__main__':
    # usage: pts_file capacity
    tin_file, pts, zs, tris = generate_TIN(sys.argv[1]) # sys.argv[1] should be the point file name
    # the above function will generate the TIN based on the input point file
    # plot_tin_with_marks(pts[:,0], pts[:,1], zs,tris,zs, [], [],[],"tin-og") # This function will plot the original TIN

    reader = Reader() # initialize a Reader object

    tin = reader.read_tin_file(tin_file) # This function will read the TIN file written by generate_TIN() function.
    # You need to COMPLETE the read_tin_file() function in the reader.py


    capacity = sys.argv[2] #sys.argv[2] should be the capacity value
    

    tree = Tree(int(capacity)) #initialize a Tree object.
    tree.build_tree(tin)   # build_tree() will generate a Triangle PR-quadtree on the input TIN.
    # You need to COMPLETE the build_tree() function in the tree.py

    ''' 
    Note I added this on purpose to distinguish the first and the second task
    Note the extra task is also included in the first task by default
    0 stands for execute all three tasks in one shot
    1 stands for execute the first and the extra task
    2 stands for execute the second task
    '''
    task = int(sys.argv[3])
    print(pts)
    roughnessList, curvatureList, maximum_vertices = tree.writeOutput(tin, task) # for the project of the second part
    # Plot the three graphs
    print(roughnessList)
    print(curvatureList)
    print(maximum_vertices)
    if (task == 0 or task == 1):
        plot_tin_with_marks(pts[:,0], pts[:,1], zs,tris,roughnessList, [], [],[],"tin-roughness"+capacity) # This function will plot the TIN with roughness colored
        plot_tin_with_marks(pts[:,0], pts[:,1], zs,tris,curvatureList, [], [],[],"tin-curvature"+capacity) # This function will plot the TIN with curvature colored
    if (task == 0 or task == 2):
        print('ss')
        points= np.empty(shape=[0, 2])
        zpoints = list()
        for vertex in maximum_vertices:
            points = np.append(points,[[pts[vertex][0], pts[vertex][1]]],axis=0)
            zpoints.append(zs[vertex])
        plot_tin_with_marks(pts[:,0], pts[:,1], zs,tris,zs, points[:,0], points[:,1],zpoints,"tin-max"+capacity) # This function will plot the TIN with curvature colored
 


