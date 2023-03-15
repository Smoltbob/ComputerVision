from lib.Math.math_utils import norm


class so3:
    def __init__(self, w):
        self.w = w  # euler angles

    def __repr__(self):
        return f"so3: {self.w}"

    def __add__(self, rhs):
        # TODO
        # https://en.wikipedia.org/wiki/Baker%E2%80%93Campbell%E2%80%93Hausdorff_formula
        pass

    def angle(self):
        return norm(self.w)
