import matplotlib.pyplot as plt

from math import gamma
import sys
sys.path.append("../2DProjectiveGeometry")
from math_utils import cos, sin, sqrt, atan2, exp, pi

class State:
    """
    State of a wheeled robot moving in 2D at a given time.
    """
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

    def __repr__(self):
        return f"State [x = {self.x}, y = {self.y}, theta = {self.theta}]"

    def as_vector(self):
        return [self.x, self.y, self.theta]

class Motion:
    """
    Defines the motion model at a given time.
    The motion model has two parameters: 
    - The transational velocity v
    - The roational velocity w
    """
    def __init__(self, v, w ):
        self.v = v
        self.w = w

    def __repr__(self):
        return f"Motion: [v = {self.v}, w = {self.w}"

    def as_vector(self):
        return [self.v, self.w]

class Robot:
    def __init__(self, state: State, motion: Motion):
        # State and control of the robot at the 
        # current moment t
        self.states = [state]
        self.motion = motion
        # Motion error parameters
        self.alpha1 = 1
        self.alpha2 = 1
        self.alpha3 = 1
        self.alpha4 = 1
        self.alpha5 = 1
        self.alpha6 = 1

    def __repr__(self):
        return f"Robot: \nState: {self.get_curr_state()}"

    def push_new_state(self, new_state):
        self.states.append(new_state)

    def get_curr_state(self):
        return self.states[-1]

    def get_prev_state(self):
        return self.states[-2]

    def apply_control(self, ut):
        self.motion = ut

    def plot(self, ax):
        x = self.get_curr_state().x
        y = self.get_curr_state().y
        theta = self.get_curr_state().theta

        dx = 1
        dy = 0

        dx = dx * cos(theta) - dy * sin(theta)
        dy = dx * sin(theta) + dy * cos(theta)
        plt.arrow(x, y, dx, dy, width = 0.1)
        plt.plot(x, y, marker = "x", markersize = 1)

