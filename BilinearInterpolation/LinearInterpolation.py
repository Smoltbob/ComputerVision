import Geometry.Point as Point

class LinearInterpolation:
    def __init__(self, point1: Point, point2: Point):
        # Set up the range in between which we will interpolate
        self.range = [point1.x, point2.y]
        self.data = [point1.y, point2.y]

 
    def interpolate(self, x):
        pass