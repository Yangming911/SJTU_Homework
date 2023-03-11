#!/usr/bin/env python3
import queue
import cv2
import numpy as np
import sys


def binarize(gray_image, thresh_val):
  # TODO: 255 if intensity >= thresh_val else 0
  (x,y) = gray_image.shape
  binary_image = np.zeros((x,y))
  for i in range(x):
    for j in range(y):
      if gray_image[i,j] >= thresh_val: binary_image[i,j] = 255
      else: binary_image[i,j] = 0
  return binary_image

def label(binary_image):
  # find connected components and label them by gray level
  label_number = 0
  lable_distance = 40
  (x,y) = binary_image.shape
  labeled_image = np.zeros((x,y))
  for i in range(x):
    for j in range(y):
      if binary_image[i,j] == 255 and labeled_image[i,j] == 0:
        label_number += 1
        label = label_number * lable_distance
        # build a queue
        q = []
        q.append((i,j))
        while len(q) != 0:
          (i,j) = q.pop()
          labeled_image[i,j] = label
          if i-1 >= 0 and binary_image[i-1,j] == 255 and labeled_image[i-1,j] == 0:
            q.append((i-1,j))
          if i+1 < x and binary_image[i+1,j] == 255 and labeled_image[i+1,j] == 0:
            q.append((i+1,j))
          if j-1 >= 0 and binary_image[i,j-1] == 255 and labeled_image[i,j-1] == 0:
            q.append((i,j-1))
          if j+1 < y and binary_image[i,j+1] == 255 and labeled_image[i,j+1] == 0:
            q.append((i,j+1))
              
  return labeled_image

def get_attribute(labeled_image):
  # for every object, compute its position, orientation, and roundedness in a dictionary
  # return a list of dictionaries
  attribute_list = []
  (x,y) = labeled_image.shape
  label_distance = 40
  max_label = 0
  for i in range(x):
    for j in range(y):
      if labeled_image[i,j] > max_label: max_label = labeled_image[i,j]
  max_label_number = int(max_label / label_distance)

  for label_number in range(1, max_label_number+1):
    label = label_number * label_distance  
    temp_list = []
    for i in range(x):
      for j in range(y):
        if labeled_image[i,j] == label:
          temp_list.append((i,j))
    # compute position(mass center)
    mass_center_x = int(sum([i for (i,j) in temp_list]) / len(temp_list))
    mass_center_y = int(sum([j for (i,j) in temp_list]) / len(temp_list))
    # compute orientation
    a = sum([(i - mass_center_x) * (i - mass_center_x) for (i,j) in temp_list])
    b = 2*sum([(i - mass_center_x) * (j - mass_center_y) for (i,j) in temp_list])
    c = sum([(j - mass_center_y) * (j - mass_center_y) for (i,j) in temp_list])  
    
    theta_1 = 0.5 * np.arctan2(b, a-c) 
    theta_2 = theta_1 + np.pi/2
    E_1 = a*np.sin(theta_1)**2 - b*np.sin(theta_1)*np.cos(theta_1) + c*np.cos(theta_1)**2
    E_2 = a*np.sin(theta_2)**2 - b*np.sin(theta_2)*np.cos(theta_2) + c*np.cos(theta_2)**2
    
    # if ((a-c)*np.cos(2*theta_1) + b*np.sin(2*theta_1)) <= 0 : 
    theta = theta_1
    E_min = E_1
    E_max = E_2
    # else : 
    #   theta = theta_2
    #   E_min = E_2
    #   E_max = E_1
    
    # compute roundedness 
    round = E_min / E_max
    attribute_list.append({'x':mass_center_x, 'y':mass_center_y, 'orentation':theta, 'roundedness':round})
  return attribute_list

def main(argv):
  img_name = argv[0]
  thresh_val = int(argv[1])
  #   img = cv2.imread('data/' + img_name + '.png', cv2.IMREAD_COLOR)
  img = cv2.imread('D:\\Grade3_1\\Computer_Vision\\CV_HW1\\data\\' + img_name + '.png', cv2.IMREAD_COLOR)
  gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  #  gray_image.shape = (631, 746)
  binary_image = binarize(gray_image, thresh_val=thresh_val)
  labeled_image = label(binary_image)
  attribute_list = get_attribute(labeled_image)

  cv2.imwrite('output/' + img_name + "_gray.png", gray_image)
  cv2.imwrite('output/' + img_name + "_binary.png", binary_image)
  cv2.imwrite('output/' + img_name + "_labeled.png", labeled_image)
  
  print(attribute_list)


if __name__ == '__main__':
  main(sys.argv[1:])

# CV_HW1/p1_object_attributes.py many_objects_1 100
# [{'x': 265, 'y': 266, 'orentation': 0.11004165482480466, 'roundedness': 1.8520820012841268}, 
# {'x': 317, 'y': 461, 'orentation': 0.8139164310738836, 'roundedness': 1.0126364164173203},
# {'x': 321, 'y': 326, 'orentation': 0.770936200798338, 'roundedness': 6.950199362557659}, 
# {'x': 390, 'y': 418, 'orentation': 2.365549534153963, 'roundedness': 37.90349183005594},
# {'x': 373, 'y': 268, 'orentation': 2.611390082421364, 'roundedness': 2.12557625627485},
# {'x': 451, 'y': 304, 'orentation': 0.45863589737567056, 'roundedness': 3.358118849517503}]
