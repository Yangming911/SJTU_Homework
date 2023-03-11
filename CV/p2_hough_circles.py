#!/usr/bin/env python3
from itertools import accumulate
import cv2
import numpy
import sys
import numpy as np

def detect_edges(image):
    """Find edge points in a grayscale image.

    Args:
    - image (2D uint8 array): A grayscale image.

    Return:
    - edge_image (2D float array): A heat map where the intensity at each point
        is proportional to the edge magnitude.
    """
    # use sobel filter to find edges
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    edge_image = np.zeros(image.shape)
    edge_image = cv2.filter2D(image, -1, sobel_x) + cv2.filter2D(image, -1, sobel_y)
    return edge_image
    
    
def draw_circle(x0, y0, radius, image):
    # Reference: https://en.wikipedia.org/wiki/Midpoint_circle_algorithm
    x = radius
    y = 0
    criterion = 1 - x
    while x >= y:
        if 0<(x0+x)<image.shape[0] and 0<(y0+y)<image.shape[1]: image[x0+x, y0+y] += 1
        if 0<(x0+y)<image.shape[0] and 0<(y0+x)<image.shape[1]: image[x0+y, y0+x] += 1
        if 0<(x0-y)<image.shape[0] and 0<(y0+x)<image.shape[1]: image[x0-y, y0+x] += 1
        if 0<(x0-x)<image.shape[0] and 0<(y0+y)<image.shape[1]: image[x0-x, y0+y] += 1
        if 0<(x0-x)<image.shape[0] and 0<(y0-y)<image.shape[1]: image[x0-x, y0-y] += 1
        if 0<(x0-y)<image.shape[0] and 0<(y0-x)<image.shape[1]: image[x0-y, y0-x] += 1
        if 0<(x0+y)<image.shape[0] and 0<(y0-x)<image.shape[1]: image[x0+y, y0-x] += 1
        if 0<(x0+x)<image.shape[0] and 0<(y0-y)<image.shape[1]: image[x0+x, y0-y] += 1           
        y += 1
        if criterion <= 0:
            criterion += 2 * y + 1
        else:
            x -= 1
            criterion += 2 * (y - x) + 1
    return image
    

def hough_circles(edge_image, edge_thresh, radius_values):
    """Threshold edge image and calculate the Hough transform accumulator array.

    Args:
    - edge_image (2D float array): An H x W heat map where the intensity at each
        point is proportional to the edge magnitude.
    - edge_thresh (float): A threshold on the edge magnitude values.
    - radius_values (1D int array): An array of R possible radius values.

    Return:
    - thresh_edge_image (2D bool array): Thresholded edge image indicating
        whether each pixel is an edge point or not.
    - accum_array (3D int array): Hough transform accumulator array. Should have
        shape R x H x W.
    """
    thresh_edge_image = edge_image.copy()
    for i in range(edge_image.shape[0]):
        for j in range(edge_image.shape[1]):
            if edge_image[i, j] > edge_thresh:
                thresh_edge_image[i, j] = 255
            else:
                thresh_edge_image[i, j] = 0
    edges = np.where(thresh_edge_image==255)
    height = edge_image.shape[0]
    width = edge_image.shape[1]
    max_radius = 50
    accum_array = np.zeros((height, width, max_radius))

    for radius in radius_values:
        # print('len:', len(edges[0]))
        for i in range(len(edges[0])):
            x = edges[0][i]
            y = edges[1][i]
            accum_array[:,:,radius] = draw_circle(x, y, radius, accum_array[:,:,radius])
    return thresh_edge_image, accum_array
            
def find_circles(image, accum_array, radius_values, hough_thresh):
    """Find circles in an image using output from Hough transform.

    Args:
    - image (3D uint8 array): An H x W x 3 BGR color image. Here we use the
        original color image instead of its grayscale version so the circles
        can be drawn in color.
    - accum_array (3D int array): Hough transform accumulator array having shape
        R x H x W.
    - radius_values (1D int array): An array of R radius values.
    - hough_thresh (int): A threshold of votes in the accumulator array.

    Return:
    - circles (list of 3-tuples): A list of circle parameters. Each element
        (r, y, x) represents the radius and the center coordinates of a circle
        found by the program.
    - circle_image (3D uint8 array): A copy of the original image with detected
        circles drawn in color.
    """
    #find circles voted larger than threshold
    
    # print('max_vote: ', np.max(accum_array))
    # circle_list = []
    # for radius in radius_values:
    #     for x in range(accum_array.shape[1]):
    #         for y in range(accum_array.shape[0]):
    #             if accum_array[y, x, radius] > hough_thresh:
    #                 circle_list.append((radius, y, x))
    #                 cv2.circle(image, (x, y), radius, (0, 255, 0), 2)
    # return circle_list, image
    
    print('max_vote: ', np.max(accum_array))
    circle_list = []
    for radius in radius_values:
        for x in range(accum_array.shape[1]):
            for y in range(accum_array.shape[0]):
                if accum_array[y, x, radius] > hough_thresh:
                    flag = True
                    for i in range(len(circle_list)):
                        (r0,y0,x0) = circle_list[i]
                        if( ((y-y0)**2<=9) and ((x-x0)**2<=9) ):
                            flag = False # Have been detected and join in list
                            break
                    if(flag):
                        circle_list.append((radius, y, x))
                        cv2.circle(image, (x, y), radius, (0, 255, 0), 2)
    return circle_list, image
                    

def main(argv):

    origin_image = cv2.imread('data\\coins.png', cv2.IMREAD_COLOR)
    gray_image = cv2.cvtColor(origin_image, cv2.COLOR_BGR2GRAY)
    output = origin_image.copy()
    
    edge_thresh_value = 100
    vote_thresh_value = 80
    
    # detect edge
    edge_image = detect_edges(gray_image)
    # edge_image = cv2.Canny(gray_image, 75, 150)
    height = edge_image.shape[0]
    width = edge_image.shape[1]
    max_radius = 40
    # Hough transform
    thresh_edge_image,accum_array = hough_circles(edge_image, edge_thresh_value, numpy.arange(1, max_radius))
    circles, circle_image = find_circles(origin_image, accum_array, numpy.arange(1, max_radius), vote_thresh_value)
    print(circles)
    cv2.imwrite('output/coins_thresh_edge.png', thresh_edge_image)
    cv2.imwrite('output/coins_circled.png', circle_image)
    
if __name__ == '__main__':
    main(sys.argv[1:])

# max_vote:  67.0
# [(22, 83, 109), (23, 82, 107), (23, 82, 108), (23, 83, 108), (23, 84, 108), (23, 82, 109), (23, 83, 109), (24, 48, 53), (24, 48, 54), (24, 49, 54), (24, 48, 55), (24, 49, 55), (24, 50, 55), (24, 81, 107), (24, 82, 107), (24, 83, 107), (24, 81, 108), (24, 82, 108), (24, 83, 108), (24, 84, 108), (24, 85, 108), (24, 84, 109), (24, 171, 234), (24, 172, 234), (24, 172, 235), (24, 173, 235), (24, 173, 236), (24, 101, 263), (24, 101, 264), (24, 102, 264), (24, 101, 265), (24, 102, 265), (25, 49, 54), (25, 49, 55), (25, 50, 55), (25, 49, 56), (25, 50, 56), (25, 51, 56), (25, 84, 109), (25, 85, 109), (25, 85, 110), (25, 86, 
# 110), (25, 173, 235), (25, 173, 236), (25, 174, 236), (25, 102, 264), (25, 103, 264), (25, 102, 265), (25, 103, 265), (25, 103, 266), (25, 104, 266), (26, 51, 56), (26, 34, 144), (26, 104, 265), (26, 104, 266), (27, 107, 33), (27, 53, 55), (27, 34, 145), (27, 34, 146), (27, 32, 148), (28, 52, 53), (28, 53, 55), (28, 54, 55), (28, 53, 56), (28, 54, 56), (28, 144, 95), (28, 32, 146), (28, 33, 146), (28, 33, 147), (28, 34, 147), (28, 33, 148), 
# (28, 34, 148), (28, 35, 149), (28, 118, 172), (28, 119, 172), (28, 119, 173), (28, 69, 214), (28, 69, 215), (28, 70, 215), (28, 70, 216), (29, 105, 35), (29, 106, 35), (29, 106, 
# 36), (29, 107, 36), (29, 106, 37), (29, 107, 38), (29, 144, 94), (29, 145, 94), (29, 145, 95), (29, 146, 95), (29, 146, 96), (29, 207, 118), (29, 208, 119), (29, 207, 120), (29, 
# 33, 147), (29, 34, 147), (29, 35, 147), (29, 34, 148), (29, 35, 148), (29, 35, 149), (29, 36, 149), (29, 118, 173), (29, 119, 173), (29, 119, 174), (29, 120, 174), (29, 120, 175), (29, 69, 215), (29, 70, 215), (29, 70, 216), (29, 71, 216), (29, 70, 217), (29, 71, 217), (29, 72, 217), (30, 106, 36), (30, 107, 36), (30, 108, 36), (30, 106, 37), (30, 107, 37), (30, 108, 37), (30, 108, 38), (30, 145, 95), (30, 146, 95), (30, 145, 96), (30, 146, 
# 96), (30, 147, 96), (30, 147, 97), (30, 207, 118), (30, 207, 119), (30, 208, 119), (30, 209, 119), (30, 208, 120), (30, 209, 120), (30, 209, 121), (30, 35, 148), (30, 36, 148), (30, 36, 149), (30, 37, 149), (30, 37, 150), (30, 120, 174), (30, 121, 174), (30, 120, 175), (30, 121, 175), (30, 71, 216), (30, 72, 217), (30, 73, 217), (30, 72, 218), (30, 73, 218), (31, 108, 37), (31, 109, 37), (31, 108, 38), (31, 109, 38), (31, 147, 96), (31, 148, 96), (31, 147, 97), (31, 148, 97), (31, 209, 120), (31, 210, 120), (31, 209, 121), (31, 
# 210, 121), (31, 37, 148), (31, 38, 150), (31, 73, 218), (31, 74, 218), (33, 76, 216), (33, 75, 217), (34, 39, 145), (34, 41, 148), (34, 77, 220), (34, 77, 221)]

# [test0]Canny edge detection
# output:
# max_vote:  118.0
# [(24, 84, 109), (24, 172, 234), (25, 50, 55), (25, 173, 235), (25, 103, 265), (28, 105, 38), (28, 145, 97), (28, 34, 147), (28, 119, 173), (28, 119, 175), (28, 70, 215), (28, 70, 217), (29, 106, 37), (29, 145, 95), (29, 145, 96), (29, 208, 118), (29, 208, 119), (29, 
# 207, 120), (29, 208, 120), (29, 35, 148), (29, 119, 174), (29, 120, 174), (29, 69, 216), 
# (29, 70, 216), (29, 71, 216), (30, 144, 95), (30, 146, 95), (30, 146, 96), (30, 207, 119), (30, 208, 119), (30, 209, 119), (30, 209, 120)]

# [test1] edge_thresh_value = 200, vote_thresh_value = 40
# [test2] edge_thresh_value = 100, vote_thresh_value = 80
# [test3] filt the circle list

