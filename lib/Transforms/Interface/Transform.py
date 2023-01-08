class Transform:
    """
    Generic transform class.
    Can be used with any transform that can be composed, 
    for instance SE3, SO3, S1, etc
    """
    
    def __init__(self, transform, to: str, frm: str):
        self.transform_type = type(transform)
        self.transform = transform
        self.to = to
        self.frm = frm
        
    def __repr__(self):
        return f"Transforms from {self.frm} to {self.to} using {self.transform}"
        
    def __matmul__(self, rhs):
        """
        Composes two transforms of the same type, if they are compatible.
        """
        assert(self.transform_type == rhs.transform_type, f"Trying to compose transform of type {self.transform_type} with type {rhs.transform_type}")
        assert(self.to == rhs.frm, f"Left transform goes to {self.to}, but right transform goes from {rhs.frm}")
        matmul_op = getattr(self, "__matmul__", None)
        assert(callable(matmul_op), f"Underlying transform {self.transform} has no @ composition function")
        return Transform(
            transform = self.transform @ rhs.transform,
            to = rhs.to,
            frm = self.frm)
    
    def inverse(self):
        """
        Computes the inverse of the transform.
        The underlying transform must have an inverse() function
        """
        invert_op = getattr(self, "inverse", None)
        assert(callable(invert_op), f"Underlying transform {self.transform} has no inverse() function")
        return Transform(self.transform.inverse(), to = self.frm, frm = self.to)