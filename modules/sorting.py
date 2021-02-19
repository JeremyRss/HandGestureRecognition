import numpy as np
from scipy.spatial import distance_matrix
import scipy


def find_extreme_point(edges):
    start_y = 0
    start_x = 0
    idx = 0
    for index in range(0, len(edges[1])):
        y = edges[0][index]
        x = edges[1][index]
        if (y > start_y):
            start_x = x
            start_y = y
            idx = index

    return (start_x, start_y, idx)


def sort_edges(edges):
    x, y, indx = find_extreme_point(edges)
    formatted_edge_points = []
    for i in range(0, edges.shape[1]):
        x = edges[1][i]
        y = 256 - edges[0][i]
        formatted_edge_points.append([x, y])

    formatted_edge_points = np.array(formatted_edge_points)

    dm = scipy.spatial.distance_matrix(formatted_edge_points, formatted_edge_points)

    prev_point = indx
    number_of_points_found = 0

    new_points = []
    new_points.append(formatted_edge_points[prev_point])

    total_distance = 0

    while (number_of_points_found < formatted_edge_points.shape[0] - 1):
        row_to_scan = dm[prev_point, :]
        argmin = np.argmin(row_to_scan)
        new_points.append(formatted_edge_points[argmin])
        total_distance += dm[prev_point][argmin]

        dm[:, argmin] = np.inf
        number_of_points_found += 1
        prev_point = argmin

    new_points_formatted = [[], []]

    for point in new_points:
        new_points_formatted[0].append(point[1])
        new_points_formatted[1].append(point[0])

    new_points_formatted = np.array(new_points_formatted)

    return (new_points_formatted)