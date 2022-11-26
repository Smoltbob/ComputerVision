import numpy as np 
from probabilities import NormalDistribution, TriangularDistribution
import sys
sys.path.append("../2DProjectiveGeometry")
from math_utils import cos, sin, sqrt, atan2, exp, pi
import kinematics # TODO add an interface to remove this dependency

class MotionModel:
    def __init__(self):
        self.delta_time = 1
        self.distribution = [NormalDistribution, TriangularDistribution][0]()

class VelocityMotionModel(MotionModel):
    """
    Computes the probability of the robot's current state 
    given its motion and previous state.
    """
    def motion_model_velocity(self, robot: kinematics.Robot):
        state_curr = robot.get_curr_state()
        state_prev = robot.get_prev_state()
        ut = robot.motion

        xp, yp, thetap = state_curr.x, state_curr.y, state_curr.theta
        x, y, theta = state_prev.x, state_prev.y, state_prev.theta

        num_mu = (x - xp) * cos(theta) + (y - yp) * sin(theta)
        den_mu = (y - yp) * cos(theta) - (x - xp) * sin(theta)
        mu = 0.5 * (num_mu / den_mu)

        x_star = 0.5 * (x + xp) + mu * (y - yp)
        y_star = 0.5 * (y + yp) + mu * (xp - x)
        r_star = sqrt((x - x_star)**2 + (y - y_star)**2)

        delta_theta = atan2(yp - y_star, xp - x_star) - atan2(y - y_star, x - x_star)

        v_hat = (delta_theta / self.delta_time) * r_star
        w_hat = delta_theta / self.delta_time
        gamma_hat = ((thetap - theta) / self.delta_time) - w_hat

        first = self.distribution.compute_probability(ut.v - v_hat, robot.alpha1 * abs(ut.v) + robot.alpha2 * abs(ut.w))
        second = self.distribution.compute_probability(ut.w - w_hat, robot.alpha3 * abs(ut.v) + robot.alpha4 * abs(ut.w))
        third = self.distribution.compute_probability(gamma_hat, robot.alpha5 * abs(ut.v) + robot.alpha6 * abs(ut.w))
        
        return first * second * third

    """
    Samples a new state x_t knowing the previous one and a control.
    """
    def sample_motion_model_velocity(self, robot: kinematics.Robot):
        v = robot.motion.v
        w = robot.motion.w
        state_prev = robot.get_curr_state()
        x, y, theta = state_prev.x, state_prev.y, state_prev.theta

        v_hat = v + self.distribution.sample_probability(robot.alpha1 * abs(v) + robot.alpha2 * abs(w))
        w_hat = w + self.distribution.sample_probability(robot.alpha3 * abs(v) + robot.alpha4 * abs(w))
        gamma_hat = self.distribution.sample_probability(robot.alpha5  * abs(v) + robot.alpha6 * abs(w))

        xp = x - (v_hat / w_hat) * sin(theta) + (v_hat / w_hat) * sin(theta + w_hat * self.delta_time)
        yp = y + (v_hat / w_hat) * cos(theta) - (v_hat / w_hat) * cos(theta + w_hat * self.delta_time)
        thetap = theta + w_hat * self.delta_time + gamma_hat * self.delta_time
        return kinematics.State(xp, yp, thetap)


class OdometryMotionModel(MotionModel):
    def __init__(self):
        self.delta_time = 1
        self.distribution = [NormalDistribution, TriangularDistribution][0]()

    """
    Samples a new state x_t based on odometry information.
    The odometry information is given by looking at the current
    and previous state of the robot.
    """
    def sample_motion_model_velocity(self, robot: kinematics.Robot):
        state_curr = robot.get_curr_state()
        xp, yp, thetap = state_curr.x, state_curr.y, state_curr.theta

        state_prev = robot.get_prev_state()
        x, y, theta = state_prev.x, state_prev.y, state_prev.theta

        delta_rot_1 = atan2(yp - y, xp - x) - theta
        delta_trans = sqrt((x - xp)**2 + (y - yp)**2)
        delta_rot_2 = thetap - theta - delta_rot_1

        delta_rot_1_hat = delta_rot_1 - self.distribution.sample_probability(robot.alpha1 * delta_rot_1 + robot.alpha2 * delta_trans)
        delta_trans_hat = delta_trans - self.distribution.sample_probability(robot.alpha3 * delta_trans + robot.alpha4 * (delta_rot_1 + delta_rot_2))
        delta_rot_2_hat = delta_rot_2 - self.distribution.sample_probability(robot.alpha1 * delta_rot_2 + robot.alpha2 * delta_trans)

        xp = x + delta_trans_hat * cos(theta + delta_rot_1_hat)
        yp = y + delta_trans_hat * sin(theta + delta_rot_1_hat)
        thetap = theta + delta_rot_1_hat + delta_rot_2_hat

        return kinematics.State(xp, yp, thetap)