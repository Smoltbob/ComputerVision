class so3:
    def __init__(self, w):
        self.w = w  # euler angles

    def __repr__(self):
        return f"so3: {self.w}"

    def angle(self):
        return norm(self.w)
