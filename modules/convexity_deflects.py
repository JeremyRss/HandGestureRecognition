import math

def get_distance(h1_x, h1_y, h2_x, h2_y, cp_x, cp_y, index, next_index):


    h1_y = 256 - h1_y
    h2_y = 256 - h2_y

    dx0 = h2_x - h1_x
    dy0 = h2_y - h1_y

    if (dx0 == 0) and (dy0 == 0):
        scale = 0
    else:
        scale = 1 / math.sqrt(dx0 * dx0 + dy0 * dy0)

    dx = h1_x - cp_x
    dy = h1_y - cp_y

    return (abs(-dy0 * dx + dx0 * dy) * scale)


def get_convexity_deflects(hull, edges):
    convexity_deflects = []
    for hull_point_index in range(0, len(hull) - 1):

        hull_point = hull[hull_point_index]
        next_hull_point = hull[hull_point_index + 1]

        index = hull_point[2]
        h1_x = hull_point[0]
        h1_y = hull_point[1]

        next_index = next_hull_point[2]
        h2_x = next_hull_point[0]
        h2_y = next_hull_point[1]

        max_distance = 0
        res_cp_x = -1
        res_cp_y = -1
        res_index = 0

        for j in range(index + 1, next_index):

            cp_x = edges[1][j]
            cp_y = edges[0][j]

            distance = get_distance(h1_x, h1_y, h2_x, h2_y, cp_x, cp_y, index, next_index)

            if (distance > max_distance):
                res_cp_x = cp_x
                res_cp_y = cp_y
                res_index = j
                max_distance = distance
        if (res_cp_x != -1):
            convexity_deflects.append([(h1_x, h1_y), (h2_x, h2_y), (res_cp_x, res_cp_y), max_distance])

    return (convexity_deflects)