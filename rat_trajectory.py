import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Rat(object):
    def __init__(self, speed, position, direction):
        self.speed = speed
        self.position = position
        self.direction = direction


class QuadraticCage(object):
    def __init__(self, side_length):
        self.side_length = side_length
        self.x_boundaries, self.y_boundaries = self._get_boundaries()

    def _get_boundaries(self):
        boundary = 0.5 * self.side_length
        return np.array([-boundary, boundary]), np.array([-boundary, boundary])

    def is_in_bounds(self, position):
        if (self.x_boundaries[0] <= position[0] <= self.x_boundaries[1] and
                self.y_boundaries[0] <= position[1] <= self.y_boundaries[1]):
            return True


def simulate_rat_path(rat: Rat, cage: QuadraticCage, sd_direction, t_max, dt):
    steps = np.int(t_max / dt)
    positions = np.zeros((2, steps))
    directions = np.zeros(steps)
    positions[:, 0] = rat.position
    directions[0] = rat.direction
    adaptive_sd = sd_direction

    for step in np.arange(1, steps):
        while_counter = 0
        while True and while_counter < 1000:
            new_direction = np.random.normal(directions[step - 1], adaptive_sd)
            new_position = positions[:, step - 1] + rat.speed * dt * np.array(
                [np.cos(new_direction), np.sin(new_direction)])
            if cage.is_in_bounds(new_position):
                positions[:, step] = new_position
                directions[step] = new_direction
                adaptive_sd = sd_direction
                break
            else:
                # increase direction SD by 5% for each failed attempt to avoid
                # getting stuck
                adaptive_sd *= 1.05
                while_counter += 1

        if while_counter == 1000:
            print("no valid direction found in 1000 attempts")
            break

    return positions, directions


def main():
    rat_speed = 0.4 # in meters per second
    rat_start_position = np.array([0, 0])
    rat_start_direction = 0
    rat = Rat(rat_speed, rat_start_position, rat_start_direction)
    cage = QuadraticCage(1.25) # dimensions in meters
    sd_direction = 0.2 # in radians
    t_max = 400 # in seconds
    dt = 0.01 # in seconds
    positions, directions = simulate_rat_path(
        rat, cage, sd_direction, t_max, dt)

    fig, sp = plt.subplots(1)
    sp.add_patch(
        patches.Rectangle(
            (cage.x_boundaries[0], cage.y_boundaries[0]),
            cage.side_length,
            cage.side_length,
            fill=False,
            linewidth=3
        )
    )
    colormap = plt.cm.viridis
    path_colors = colormap(np.arange(directions.size) / directions.size)
    sp.scatter(
        positions[0, :], positions[1, :], c=path_colors, edgecolor="None", s=2)
    sp.set_aspect("equal")
    sp.margins(0)
    plt.show()


if __name__ == "__main__":
    main()
