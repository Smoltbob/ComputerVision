import skspatial.objects as so
from line import Line
from geometry import cross
class InhomogeneousPoint(): 
    def __init__(self, vector):
        assert(isinstance(vector, list))
        assert(len(vector) == 2)
        self.vector = vector

    # TODO this should be common to both classes
    def __repr__(self) -> str:
        return f"x: {self.vector[0]}, y: {self.vector[1]}"

    def plot(self, ax):
        """
        Plots the inhomogeneous point as a point in R2
        """
        _point = so.Point(self.vector)
        _point.plot_2d(ax)


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

    def plot(self, ax3d):
        """
        Plots the homogeneous point as a line in P2
        """
        _point = so.Line([0, 0, 0], self.vector)
        _point.plot_3d(ax3d, c = 'k')
        _image_plane = so.Plane([0,0,1], [0,0,1])
        
        _point_intersection = _image_plane.intersect_line(_point)
        _point_intersection.plot_3d(ax3d, c = 'r', s = 75)
        #_image_plane.plot_3d(ax3d, lims_x=(0, 5), lims_y=(0, 5), alpha=0.3)

