import numpy as np
from sorting import find_extreme_point

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
def orientation(p, q, r):
    '''
    To find orientation of ordered triplet (p, q, r).
    The function returns following values
    0 --> p, q and r are colinear
    1 --> Clockwise
    2 --> Counterclockwise
    '''
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)

    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2


def jarvis_walk(edges):
    x_start, y_start, first_index = find_extreme_point(edges)
    edges_x = edges[1]
    edges_y = edges[0]
    hull = ([[x_start, y_start, first_index]])

    next_point = Point(0, 0)
    start_point = Point(x_start, y_start)
    current_point = Point(x_start, y_start)
    hull_index = first_index

    while (True):

        for index in range(0, len(edges_x)):

            x = edges_x[index]
            y = edges_y[index]
            test_point = Point(x, y)
            orient = orientation(current_point, next_point, test_point)
            if (orient == 2):
                next_point = test_point
                hull_index = index
        if (next_point.x == x_start and next_point.y == y_start):
            break
        hull.append([next_point.x, next_point.y, hull_index])

        current_point, next_point = next_point, current_point
        hull_index = None
    hull = np.array(hull)
    hull[:, 1] = 256 - hull[:, 1]
    hull = list(hull)
    hull.append(hull[0])
    hull = np.array(hull)
    return hull[hull[:, 2].argsort()]

