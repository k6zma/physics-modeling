import matplotlib.pyplot as plt


def calculate_parabolic_trajectory(x, y, vx, vy, g, t_flight):
    x_flight = x + vx * t_flight
    y_flight = y + vy * t_flight - 0.5 * g * t_flight**2
    return x_flight, y_flight
