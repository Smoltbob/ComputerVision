from point import HomogeneousPoint
from geometry import dot, cross

class Line():
    # TODO also init directly from vector
    def __init__(self, a, b, c):
        self.vector = [a, b, c]

    # TODO define the tolerance properly
    def __contains__(self, p: HomogeneousPoint):
        return dot(self.vector, p.vector) < 1E-6

    @staticmethod
    def intersection(lineA, lineB):
        return HomogeneousPoint(cross(lineA.vector, lineB.vector))


    def __repr__(self) -> str:
        return f"a: {self.vector[0]}, b: {self.vector[1]}, c: {self.vector[2]}"
