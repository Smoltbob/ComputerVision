import skspatial.objects as so
from line import Line
from geometry import cross
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