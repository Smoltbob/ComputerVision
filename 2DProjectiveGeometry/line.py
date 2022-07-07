from point import HomogeneousPoint
from geometry import dot, cross
import skspatial.objects as so
from matplotlib import axes
from mpl_toolkits.mplot3d import Axes3D
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
        y = 0
        x = (-self.vector[2] - (self.vector[1] * y)) / self.vector[0]
        vertex1 = [x, y, 1]
        y = 1
        x = (-self.vector[2] - (self.vector[1] * y)) / self.vector[0]
        vertex2 = [x, y, 1]
        if show_plane:
            plane = so.Plane.from_points(origin, vertex1, vertex2)
            plane.plot_3d(ax3d, lims_x = (-2, 2), lims_y = (-2, 2), color = color, alpha = 0.2)

        line = so.Line(point = vertex1, direction = [self.vector[1], -self.vector[0], 0])
        line.plot_3d(ax3d, t_1 = -1, t_2 = 1, c = color)

    def __plot2d(self, ax, color):
        """
        Plot the line as a plane that goes through the origin
        """
        y = 0
        x = (-self.vector[2] - (self.vector[1] * y)) / self.vector[0]
        vertex1 = [x, y]
        
        line =  so.Line(point = vertex1, direction = [self.vector[1], -self.vector[0]])
        line.plot_2d(ax, t_1 = -1, t_2 = 1, c = color)

    def plot(self, ax, color = "r", show_plane = True):
        if isinstance(ax, Axes3D):
            self.__plot3d(ax, color, show_plane)
        else:
            self.__plot2d(ax, color)

        
