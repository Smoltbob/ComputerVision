import matplotlib
#import skspatial.objects as so
from lib.Math.Math_utils import cross, dot, sqrt, norm, atan2
#from mpl_toolkits.mplot3d import Axes3D

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Point3D():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

"""
Design philosophy:
- Most operations are done Homogeneously,
but we can make inhomogeneous if needed
"""
class InhomogeneousPoint(): 
    def __init__(self, vector):
        assert(isinstance(vector, list))
        assert(len(vector) == 2)
        self.vector = vector

    # TODO this should be common to both classes
    def __repr__(self):
        return f"x: {self.vector[0]}, y: {self.vector[1]}"

    # TODO homogenize function notation (camel case ?)
    def to_Homogeneous(self):
        return HomogeneousPoint([self.vector[0], self.vector[1], 1])

    def plot(self, ax, color = "r"):
        """
        Plots the inhomogeneous point as a point in R2
        """
        if isinstance(ax, Axes3D):
            self.to_Homogeneous().plot(ax, color)
        else: # we assume we have a valid normal axis
            _point = so.Point(self.vector)
            _point.plot_2d(ax, c = color)


class HomogeneousPoint():
    def __init__(self, *args):
        def _fromVector(vector: list):
            assert(len(vector) == 2 or len(vector) == 3)

            if len(vector) == 2:
                return [*vector, 1]
            if len(vector) == 3:
                return vector

        if isinstance(*args, list):
            self.vector = _fromVector(*args)
        else:
            print(type(args))
            assert(False)

    def __repr__(self) -> str:
        return f"x: {self.vector[0]}, y: {self.vector[1]}, z: {self.vector[2]}"

    def distance_from(self, point):
        difference = [x - y for x, y in zip(self.vector, point.vector)]
        return norm(difference)

    def angle(self):
        """
        TODO
        angle of the point as defined in the trigonometric circle
        """
        _inhom = self.toInhomogeneous()
        return atan2(_inhom.vector[1], _inhom.vector[0])

    def angle_from(self, hpoint):
        pass

    def join(self, lineA):
        '''
        Note: this is the same thing as Line.intersection()
        '''
        return Line(cross(self.vector, lineA.vector))

    def toInhomogeneous(self):
        return InhomogeneousPoint(
            [self.vector[0] / self.vector[2], self.vector[1] / self.vector[2]])

    def __plot3d(self, ax3d, color):
        """
        Plots the homogeneous point as a line in P2
        """
        _ray = so.Line([0, 0, 0], self.vector)
        _ray.plot_3d(ax3d, c = 'k', linestyle='--')
        _image_plane = so.Plane([0,0,1], [0,0,1])
        
        if self.vector[2] != 0:
            _point_intersection = _image_plane.intersect_line(_ray)
            _point_intersection.plot_3d(ax3d, c = color, s = 50)
        else:
            so.Point(self.vector).plot_3d(ax3d, c = color, s = 50)
    
    
    def plot(self, ax, color = "r"):
        if isinstance(ax, Axes3D):
            self.__plot3d(ax, color)
        else: # we assume we have a valid normal axis
            # TODO deal with ideal points
            _inhomo = self.toInhomogeneous()
            _inhomo.plot(ax, color)


class Line():
    """
    A line can be defined from:
    - An equation ax+by+c=0 (vector [a,b,c])
    - Two points
    - A point and an angle
    """

    # TODO also init directly from vector
    # TODO add direction of line
    def __init__(self, vector):
        assert(len(vector) == 3)
        self.vector = vector

    def line_from_points(self, pt1, pt2):
        """
        Line from two inhomogeneous points
        Assert: points are inhomogeneous
        """
        x0, y0 = pt1.vector
        x1, y1 = pt2.vector
        a = y0 - y1
        b = x1 - x0
        c = y1*x0 - y0*x1
        self.vector = [a, b, c]

    # TODO define the tolerance properly
    def __contains__(self, p: HomogeneousPoint):
        return dot(self.vector, p.vector) < 1E-6

    def intersection(self, lineA):
        return HomogeneousPoint(cross(self.vector, lineA.vector))

    def __repr__(self) -> str:
        return f"a: {self.vector[0]}, b: {self.vector[1]}, c: {self.vector[2]}"

    def ideal_point(self):
        """
        Returns the point at infinity where every line parallel
        to self intersect
        """
        return HomogeneousPoint([self.vector[1], -self.vector[0], 0])

    def project_inhomogeneous_point(self, point):
        """
        Using the equation (vector) form of the line, project a point onto it.

        assert: the point must be inhomogeneous
        """
        x0, y0 = point.vector
        a, b, c = self.vector

        den = a ** 2 + b **2
        x =  (b * (b*x0 - a*y0) -a * c) / den
        y = (a*(-b*x0 + a*y0)-b*c) /den

        return InhomogeneousPoint([x, y])


class Utils():
    """
    A kind of anonymous namespace with utilities
    """

    def distance_line_point(line, point):
        # TODO create two functions in Line and Point that use this
        """
        Distance between a line and an inhomogeneous point
        Assert:
        - Point is inhomogeneous
        """
        a, b, c = line.vector
        x0, y0 = point.vector
        return abs(a*x0 + b*y0 + c) / sqrt(a**2 + b**2)
