import numpy as np

class InhomogeneousPoint(): 
    def __init__(self, x, y):
        self.vector = [x, y]

    # TODO this should be common to both classes
    def __repr__(self) -> str:
        return f"x: {self.vector[0]}, y: {self.vector[1]}"


class HomogeneousPoint():
    def __init__(self, *args):
        def _fromVector(vector: list):
            assert(len(vector) == 2 or len(vector) == 3)

            if len(vector) == 2:
                return [*vector, 1]
            if len(vector) == 3:
                return vector

        if len(args) == 2: # and ints
            self.vector = [*args, 1]
        elif len(args) == 3:
            self.vector = [*args] # and ints
        elif isinstance(*args, list):
            self.vector = _fromVector(*args)
        else:
            print(type(args))
            assert(False)


    def __repr__(self) -> str:
        return f"x: {self.vector[0]}, y: {self.vector[1]}, z: {self.vector[2]}"

