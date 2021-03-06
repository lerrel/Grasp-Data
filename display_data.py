'''
Code to display the Patch dataset used in training grasping network in
https://arxiv.org/pdf/1609.09025v1.pdf

Dependencies:   argparse ('pip install argparse')
                cv2 ('conda install -c menpo opencv=2.4.11' or install opencv from source)
                numpy ('pip install numpy' or 'conda install numpy')

Change variable 'grasp_path_path' to the path of the dataset, or place this script in the dataset folder.
Template run:
    python display_data.py --dat {'Train','Test','Val'} --pos {0, 1} --ran {0, 1} --msec{1, 2, 3, ...}
Example run:
    python display_data.py --dat 'Train' --pos 1 --ran 0 --msec 1000
'''
grasp_patch_path = 'PATH_TO_DATASET'

import os
import argparse
import cv2
import numpy as np

## This function resizes the image to new_size X new_size and then draws a rectangle rotated by the grasp_angle
def process_and_draw_rect(I, grasp_angle, new_size = 500):
    I_temp = cv2.resize(I, (new_size,new_size))
    grasp_l = new_size/3.0
    grasp_w = new_size/6.0
    points = np.array([[-grasp_l, -grasp_w],
                       [grasp_l, -grasp_w],
                       [grasp_l, grasp_w],
                       [-grasp_l, grasp_w]])
    R = np.array([[np.cos(grasp_angle), -np.sin(grasp_angle)],
                  [np.sin(grasp_angle), np.cos(grasp_angle)]])
    rot_points = np.dot(R, points.transpose()).transpose()
    im_points = rot_points + new_size/2.0
    cv2.line(I_temp, tuple(im_points[0].astype(int)), tuple(im_points[1].astype(int)), color=(0,255,0), thickness=5)
    cv2.line(I_temp, tuple(im_points[1].astype(int)), tuple(im_points[2].astype(int)), color=(0,0,255), thickness=5)
    cv2.line(I_temp, tuple(im_points[2].astype(int)), tuple(im_points[3].astype(int)), color=(0,255,0), thickness=5)
    cv2.line(I_temp, tuple(im_points[3].astype(int)), tuple(im_points[0].astype(int)), color=(0,0,255), thickness=5)
    return I_temp

## Reset dataset path if path is not set
if grasp_patch_path is 'PATH_TO_DATASET':
    grasp_patch_path = os.path.dirname(os.path.abspath(__file__))+'/data' # Path to the dataset

parser = argparse.ArgumentParser()
parser.add_argument('--dat', type=str, default='Train', help='The dataset you want to display: Train, Test or Validation')
parser.add_argument('--pos', type=int, default=1, help='0 if you want to display negative data; 1 if you want to display positive data')
parser.add_argument('--ran', type=int, default=1, help='1 if you want to display is random sequence; 0 otherwise')
parser.add_argument('--msec', type=int, default=500, help='milliseconds between display')

## Parse arguments
args = parser.parse_args()
dat = args.dat
if args.pos==1: dat_typ='positive'
else: dat_typ='negative'
shuf = args.ran
msec = args.msec

## Create paths
dat_path = os.path.join(grasp_patch_path, dat, dat_typ)
images_path = os.path.join(dat_path, 'Images')
info_path = os.path.join(dat_path, 'dataInfo.txt')

with open(info_path) as f:
    content = f.readlines()
del(content[0]) # since first line is a description

proc_content = []
for x in content:
    x_l = x.strip().split(',')
    x_l[1] = float(x_l[1])
    proc_content.append(x_l)

if shuf==1:
    import random
    random.shuffle(proc_content)

for d in proc_content:
    impath = os.path.join(images_path, d[0])
    grasp_angle = d[1]
    I = cv2.imread(impath)
    I_grasp = process_and_draw_rect(I,grasp_angle)
    cv2.imshow('image',I_grasp)
    cv2.waitKey(msec)

cv2.destroyAllWindows()
