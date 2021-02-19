import numpy as np
import math


def get_angle(point1, point2, point3):
    x1 = point1[0]
    y1 = point1[1]

    x2 = point2[0]
    y2 = point2[1]

    x3 = point3[0]
    y3 = point3[1]

    a = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    b = math.sqrt((x3 - x2) ** 2 + (y3 - y2) ** 2)
    c = math.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2)

    angle = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b + 0.0000001)) * 360 / (math.pi * 2)

    return angle


def count_real_deflects(defects):

    cnt = 0
    real_deflect = []
    for i in defects:  # calculate the angle
        end, start, far, _ = i

        x_start = start[0]
        x_end = end[0]

        end_ = (end[0], end[1])
        start_ = (start[0], start[1])
        far_ = (far[0], 256 - far[1])

        angle = get_angle(start_, far_, end_)

        if angle < 90:  # angle less than 90 degree, treat as fingers
            cnt += 1
            real_deflect.append(far_)


    if cnt > 0:
        cnt = cnt + 1

    return (cnt, real_deflect)


def count_real_deflects_by_distance(defects, sorted_edges):
    cnt = 0
    real_deflect = []
    y = 256 - sorted_edges[0]
    threshold = (y.max() - y.min()) / 5

    for i in defects:  # calculate the angle
        end, start, far, distance = i
        far_ = (far[0], 256 - far[1])
        if (distance > threshold):
            cnt += 1
            real_deflect.append([far_,distance])

    if cnt > 0:
        cnt = cnt + 1
    # cv.putText(img, str(cnt), (120, 250), cv.FONT_HERSHEY_SIMPLEX,1, (255, 255, 255) , 2, cv.LINE_AA)
    return (cnt, real_deflect)
