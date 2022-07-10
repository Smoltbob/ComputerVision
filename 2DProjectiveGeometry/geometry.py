import skspatial.objects as so
from math_utils import cross, dot
from mpl_toolkits.mplot3d import Axes3D
class InhomogeneousPoint(): 
    def __init__(self, vector):
        assert(isinstance(vector, list))
        assert(len(vector) == 2)
        self.vector = vector

    # TODO this should be common to both classes
    def __repr__(self) -> str:
        return f"x: {self.vector[0]}, y: {self.vector[1]}"

    def plot(self, ax, color = "r"):
        """
        Plots the inhomogeneous point as a point in R2
        """
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
    # TODO also init directly from vector
    def __init__(self, vector):
        assert(len(vector) == 3)
        self.vector = vector

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

    def __plot3d(self, ax3d, color, show_plane):
        """
        Plot the line as a plane that goes through the origin
        """
        origin = [0, 0, 0]
        # TODO use a more generic solution
        if self.vector[0] != 0:
            y = 0
            x = (-self.vector[2] - (self.vector[1] * y)) / self.vector[0]
            vertex1 = [x, y, 1]
            y = 1
            x = (-self.vector[2] - (self.vector[1] * y)) / self.vector[0]
            vertex2 = [x, y, 1]
        elif self.vector[1] != 0:
            x = 0
            y = (-self.vector[2] - (self.vector[0] * x)) / self.vector[1]
            vertex1 = [x, y, 1]
            x = 1
            y = (-self.vector[2] - (self.vector[0] * x)) / self.vector[1]
            vertex2 = [x, y, 1]
        else:
            assert(False, "Cannot plot degenerate line")

        if show_plane:
            plane = so.Plane.from_points(origin, vertex1, vertex2)
            plane.plot_3d(ax3d, lims_x = (-2, 2), lims_y = (-2, 2), color = color, alpha = 0.2)

        line = so.Line(point = vertex1, direction = [self.vector[1], -self.vector[0], 0])
        line.plot_3d(ax3d, t_1 = -1, t_2 = 1, c = color)

    def __plot2d(self, ax, color):
        """
        Plot the line as a plane that goes through the origin
        """
        if self.vector[0] != 0:
            y = 0
            x = (-self.vector[2] - (self.vector[1] * y)) / self.vector[0]
            vertex1 = [x, y]
        elif self.vector[1] != 0:
            x = 0
            y = (-self.vector[2] - (self.vector[0] * x)) / self.vector[1]
            vertex1 = [x, y]
        else:
            assert(False, "Cannot plot degenerate line")
        
        line =  so.Line(point = vertex1, direction = [self.vector[1], -self.vector[0]])
        line.plot_2d(ax, t_1 = -1, t_2 = 1, c = color)

    def plot(self, ax, color = "r", show_plane = True):
        if isinstance(ax, Axes3D):
            self.__plot3d(ax, color, show_plane)
        else:
            self.__plot2d(ax, color)