import numpy as np
import config

class BodyTrajectory:
    def __init__(self, mass, radius, friction, angle):
        self.m = mass
        self.R = radius
        self.mu = friction
        self.alpha = angle
        self.g = config.GRAVITY
        self.v0_min = None

    def find_min_initial_velocity(self):
        self.v0_min = np.sqrt(
            (2 * (self.m * self.g * self.R * (1 - np.cos(self.alpha)) + self.m * self.g * np.sin(self.alpha) * self.mu * self.R * self.alpha)) / self.m
        )

    def calculate_trajectory(self, initial_distance=3.0, step_size=0.01, t_max=5.0, dt=0.01):
        if self.v0_min is None:
            self.find_min_initial_velocity()

        theta = 0
        v = self.v0_min
        x_arc, y_arc = [], []

        while theta <= self.alpha:
            x_arc.append(self.R * np.sin(theta))
            y_arc.append(self.R * (1 - np.cos(theta)))

            dv = self.dv_dtheta(theta, v) * step_size
            v += dv
            theta += step_size

        theta_final = theta - step_size
        v_final = v
        v_x = v_final * np.cos(theta_final)
        v_y = v_final * np.sin(theta_final)

        t = np.arange(0, t_max, dt)
        x_flight = np.zeros_like(t)
        y_flight = np.zeros_like(t)
        x_flight[0] = x_arc[-1]
        y_flight[0] = y_arc[-1]

        last_index = 0

        for i in range(1, len(t)):
            x_flight[i] = x_flight[i - 1] + v_x * dt
            y_flight[i] = y_flight[i - 1] + v_y * dt
            v_y -= self.g * dt

            if y_flight[i] <= 0:
                last_index = i
                break

        x_flight = x_flight[:last_index + 1]
        y_flight = y_flight[:last_index + 1]

        x_initial = np.linspace(-initial_distance, 0, 100)
        y_initial = np.zeros_like(x_initial)

        x_full = np.concatenate((x_initial, x_arc, x_flight))
        y_full = np.concatenate((y_initial, y_arc, y_flight))

        start_point = (x_arc[0], y_arc[0])
        end_point = (x_arc[-1], y_arc[-1])

        return x_full, y_full, x_flight, y_flight, v_final, start_point, end_point

    def dv_dtheta(self, theta, v):
        if v <= 0:
            return 0
        return (-self.g * np.sin(theta) - self.mu * (v**2 / self.R + self.g * np.cos(theta))) / (v + self.mu * self.R)
