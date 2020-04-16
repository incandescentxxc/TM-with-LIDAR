General tips:
1. The code is implemented in an object-oriented way. Therefore, you cannot directly use class attributes in external functions. You should implement functions to get and set object attributes, e.g., Vertex.set_x(), Vertex.get_x()

2. The current code can successfully generate PR-quadtree based on the vertex array stored in the TIN object. No modification on the Domain class or codes for inserting vertices is needed. 

3. The Vertex objects and Triangle objects should only be stored in two global arrays encoded in TIN object. In nodes, only indexes are stored. To get a Vertex, you should use tin.get_vertex(vid). For example, if we want to get the third vertex on the array vertices=node.get_vertices(), we should use tin.get_vertex(vertices[2]). You should design and implement similar functions for triangles.

4. The generate_TIN() and plot_TIN_with_marks() functions are in the main_test_demo.py. The test_demo can be excuted by entering:
python main_test_demo.py [point_file_path] [capacity]  
in the command line. One example of using test_1.pts point file and 1 as capacity:
python main_test_demo.py ./data/test_1.pts 1

5. You may want to test your code for the second part on the small datasets given for the first part to see if it works correctly.