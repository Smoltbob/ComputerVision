from ProjectiveGeometry.geometry import Point, Point3D
from Interpolation.LinearInterpolation import LinearInterpolator


class BilinearInterpolator:
    def __init__(self, Q11: Point3D, Q12: Point3D, Q21: Point3D, Q22: Point3D):
        assert(Q11.x == Q12.x) # x1
        assert(Q11.y == Q21.y) # y1
        assert(Q12.y == Q22.x) # y2
        assert(Q21.x == Q22.x) # x2
        self.Q11 = Q11
        self.Q12 = Q12
        self.Q21 = Q21
        self.Q22 = Q22
        
    def interpolate(self, x, y):
        assert(x <= self.Q22.x)
        assert(x >= self.Q11.x)
        assert(y <= self.Q22.y)
        assert(y >= self.Q11.y)
        
        # Interpolate in the x direction
        x_interpolator_y1 = LinearInterpolator(Point(self.Q11.x, self.Q11.z), Point(self.Q21.x, self.Q21.z))
        x_interpolator_y2 = LinearInterpolator(Point(self.Q12.x, self.Q12.z), Point(self.Q22.x, self.Q22.z))
        
        f_x_y1 = x_interpolator_y1.interpolate(x)
        f_x_y2 = x_interpolator_y2.interpolate(x)
        
        # Interpolate in the y direction
        y_interpolator = LinearInterpolator(Point(self.Q11.y, f_x_y1), Point(self.Q12.y, f_x_y2))
        return y_interpolator.interpolate(y)