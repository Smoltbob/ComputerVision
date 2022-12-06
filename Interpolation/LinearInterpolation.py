from ProjectiveGeometry.geometry import Point

class LinearInterpolator:
    def __init__(self, pointA: Point, pointB: Point):
        assert(pointA.x < pointB.x)
        self.pointA = pointA
        self.pointB = pointB
        
    def interpolate(self, x):
        num = self.pointA.y * (self.pointB.x - x) + self.pointB.y * (x - self.pointA.x)
        den = self.pointB.x - self.pointA.x
        return num / den