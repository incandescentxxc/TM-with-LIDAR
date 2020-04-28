from point import Point
import numpy as np

class Vertex(Point):
    """ A Vertex is an extension of Class Point and takes (x,y) attributes plus an elevation."""
    def __init__(self,x,y,z): # use x,y,z to initialize a vertex
        Point.__init__(self,x,y)
        self.__field_values = [z] # default.. a vertex has one field value when you initialize it... it can be extended!

    def get_z(self):
        return self.__field_values[0]

    def set_z(self,z):
        return self.__field_values[0]

    def get_c(self,pos):
        if pos in (0,1): # when pos is 0 or 1: return x or y;
            return super().get_c(pos)
        else:
            try:
                return self.__field_values[pos-2] #when pos>=2, read from field_values list.
            except IndexError as e:
                raise e

    def set_c(self,pos,c):
        if pos in (0,1):
            super().set_c(pos,c)
        else:
            try:
                self.__field_values[pos-2] = c
            except IndexError as e:
                # raise e
                # instead of raising an exception we append the field value to the end of the array
                self.__field_values.append(c)

    def get_last_field_item(self):
        # returns the last item in the field_values list.
        return self.__field_values[-1]
    
    def get_fields_num(self):
        return len(self.__field_values)
    
    def add_field(self, f):
        # The new field value will be added to the end of the list. You can use get_last_field_item() function to get it.
        self.__field_values.append(f)
    def get_field(self, pos): # it will return the field value in position pos in the field value list.
        return self.__field_values[pos]
    def print_fields(self):
        for f in self.__field_values:
            print(f)

    def __str__(self):
        return "Vertex(%s,%s,%s)"%(self.get_x(),self.get_y(),self.get_z())

    # calculate the angle at this vertex provided with other two adjacent vertices
    def angle(self,v1,v3):
        print("Calculate angle")
        print(self.get_z())
        V21 = [v1.get_c(0)-self.get_c(0),v1.get_c(1)-self.get_c(1),v1.get_z()-self.get_z()]
        V23 = [v3.get_c(0)-self.get_c(0),v3.get_c(1)-self.get_c(1),v3.get_z()-self.get_z()]
        cos_angle = np.dot(V21, V23) / (np.sqrt(np.dot(V21, V21)) * np.sqrt(np.dot(V23, V23)))
        angle = np.arccos(cos_angle)
        return angle
