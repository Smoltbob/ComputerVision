from geometry import Line
import skspatial.objects as so
from mpl_toolkits.mplot3d import Axes3D

def __plot_line_3d(line, ax3d, color, show_plane):
        """
        Plot the line as a plane that goes through the origin
        """
        origin = [0, 0, 0]
        # TODO use a more generic solution
        if line.vector[0] != 0:
            y = 0
            x = (-line.vector[2] - (line.vector[1] * y)) / line.vector[0]
            vertex1 = [x, y, 1]
            y = 1
            x = (-line.vector[2] - (line.vector[1] * y)) / line.vector[0]
            vertex2 = [x, y, 1]
        elif line.vector[1] != 0:
            x = 0
            y = (-line.vector[2] - (line.vector[0] * x)) / line.vector[1]
            vertex1 = [x, y, 1]
            x = 1
            y = (-line.vector[2] - (line.vector[0] * x)) / line.vector[1]
            vertex2 = [x, y, 1]
        else:
            assert(False, "Cannot plot degenerate line")

        if show_plane:
            plane = so.Plane.from_points(origin, vertex1, vertex2)
            plane.plot_3d(ax3d, lims_x = (-2, 2), lims_y = (-2, 2), color = color, alpha = 0.2)

        so_line = so.Line(point = vertex1, direction = [line.vector[1], -line.vector[0], 0])
        so_line.plot_3d(ax3d, t_1 = -1, t_2 = 1, c = color)

def __plot_line_2d(line, ax, color):
    """
    Plot the line as a plane that goes through the origin
    """
    if line.vector[0] != 0:
        y = 0
        x = (-line.vector[2] - (line.vector[1] * y)) / line.vector[0]
        vertex1 = [x, y]
    elif line.vector[1] != 0:
        x = 0
        y = (-line.vector[2] - (line.vector[0] * x)) / line.vector[1]
        vertex1 = [x, y]
    else:
        assert(False, "Cannot plot degenerate line")
    
    so_line =  so.Line(point = vertex1, direction = [line.vector[1], -line.vector[0]])
    so_line.plot_2d(ax, t_1 = -1, t_2 = 1, c = color)


def plot_line(line, ax, color = "r", show_plane = True):
    if isinstance(ax, Axes3D):
        __plot_line_3d(line, ax, color, show_plane)
    else:
        __plot_line_2d(line, ax, color)