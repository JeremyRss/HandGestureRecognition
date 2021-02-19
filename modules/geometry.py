import math
import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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

def get_angle(point1 ,point2 ,point3):
    x1 =point1[0]
    y1 =point1[1]

    x2 =point2[0]
    y2 =point2[1]

    x3 =point3[0]
    y3 =point3[1]

    a = math.sqrt((x1 -x2 )**2 + (y1 -y2 )**2)
    b = math.sqrt((x3 -x2 )**2 + (y3 -y2 )**2)
    c = math.sqrt((x3 -x1 )**2 + (y3 -y1 )**2)

    angle = math.acos(( a** 2 + b** 2 - c**2 ) /( 2 * a * b +0.0000001) ) *360 /(math.pi *2)

    p1 =Point(x2 ,y2)
    p2 =Point(x2 +1000 ,y2 +1000)
    p3 =Point(x3 ,y3)
    o=orientation(p1,p2,p3)
    if(o== 1) :
        return(360 - angle)
    else:
        return(angle)

def get_mean_contour(edges):
    mean_x = int(np.mean(edges[1]))
    mean_y = 256-int(np.mean(edges[0]))
    return (mean_x,mean_y)
