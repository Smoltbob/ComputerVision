from point import HomogeneousPoint
from geometry import dot, cross

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
