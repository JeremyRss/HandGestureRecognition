import cv2
import scipy
from scipy.signal import savgol_filter
import os
import csv

from geometry import get_mean_contour
from mask import get_mask
from find_edges import find_edges
import numpy as np
from sorting import sort_edges
from convex_hull import jarvis_walk
from convexity_deflects import get_convexity_deflects
from non_max_suppression import count_real_deflects_by_distance
import sys
from geometry import get_angle


def extract_features(img, hmin, smin, vmin, hmax, smax, vmax):
    img_resized = cv2.resize(img, (256, 256))
    ## CD
    masked = get_mask(img, hmin, smin, vmin, hmax, smax, vmax)
    edges = (find_edges(masked))
    edges = [edges[0][10:edges[0].shape[0] - 10], edges[1][10:edges[1].shape[0] - 10]]
    edges = np.array(edges)
    sorted_edges = sort_edges(edges)
    for i in zip(sorted_edges[0], sorted_edges[1]):
        cv2.circle(img_resized, (i[1], 256 - i[0]), radius=2, color=(255, 0, 0), thickness=1)

    hull = jarvis_walk(sorted_edges)
    hull_points = np.array(hull)[:, :2].reshape(-1, 1, 2).astype(np.int)
    convexity_deflects = get_convexity_deflects(hull, sorted_edges)
    count_cd, real_deflects = count_real_deflects_by_distance(convexity_deflects, sorted_edges)


    ##ANGLES & DISTANCE
    mx, my = get_mean_contour(edges)
    max_angle = 0
    max_distance = 0



    for j in real_deflects:
        point=j[0]
        distance = j[1]
        cv2.circle(img_resized, (point[0], point[1]), radius=2, color=(0, 255, 255), thickness=3)
        x=point[0]
        y=point[1]
        angle = get_angle([0,0],[mx,my],[x,256-y])
        if angle>max_angle:
            max_angle=angle
        if (distance)>max_distance:
            max_distance=distance


    #cv2.putText(img_resized, str(int(max_angle))+str("-")+str((max_distance)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)




    ## PEAKS

    sorted_edges_smoothed = savgol_filter(sorted_edges[0], 53, 1)
    peaks, _ = scipy.signal.find_peaks(sorted_edges_smoothed, distance=10)
    nb_peaks = len(peaks)

    ## THHIGHTNESS

    formatted_sorted_edges = []
    for i in zip(sorted_edges[0], sorted_edges[1]):
        formatted_sorted_edges.append(np.array([i[0], i[1]]).reshape(1, 2))
    formatted_sorted_edges = np.array(formatted_sorted_edges)
    sigma = cv2.contourArea(formatted_sorted_edges) / cv2.contourArea(hull_points)

    ##PLOT
    cv2.circle(img_resized, (mx, 256 - my), radius=2, color=(255, 255, 255), thickness=3)
    img_resized = cv2.polylines(img_resized, [hull_points], True, (0, 255, 0), thickness=2)

    return img_resized, count_cd, nb_peaks, sigma, max_distance, max_angle
    #return count_cd, nb_peaks, sigma,max_distance,max_angle


if __name__ == "__main__":


    data_path = sys.argv[1]
    file = open('features_test.csv', 'w')
    with file:
        writer = csv.writer(file)
        for i in os.listdir(data_path):
            if os.path.isdir(os.path.join(data_path, i)):
                folder_path = os.path.join(data_path, i)
                for j in os.listdir(folder_path):
                    if os.path.isfile(os.path.join(folder_path, j)):
                        if (j !='.DS_Store'):
                            img_path = os.path.join(folder_path, j)
                            img = cv2.imread(img_path)
                            cntcd, peaks, sigma,distance,angle = extract_features(img, 0, 0, 0, 50, 70, 255)

                            writer.writerow([i,cntcd,peaks,sigma,distance,angle])
