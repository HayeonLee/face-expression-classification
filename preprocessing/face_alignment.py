#USAGE: python face-alignment.py 
# original code: https://www.pyimagesearch.com/2017/05/22/face-alignment-with-opencv-and-python/
# db_name: dataset folder name
# generate new aligned data in 'db_name_processed'
# if you want to change dataset name, modify all '_processed' words

from imutils import face_utils
from imutils.face_utils import FaceAligner
import numpy as np
import argparse
import imutils
import dlib
import cv2
import os
import csv
import pickle

def search_files(data_path, db_name, detector, fa, new_name):
    try:
        filenames = sorted(os.listdir(data_path))
        for ith, filename in enumerate(filenames): #Emotion/S005
            full_filename = os.path.join(data_path, filename)
            if os.path.isdir(full_filename):
               if not os.path.exists(full_filename.replace(db_name, new_name)):
                  os.makedirs(full_filename.replace(db_name, new_name))
               search_files(full_filename, db_name, detector, fa, new_name)
            else:
              if ith in [0, int(len(filenames)/2), int(len(filenames) - 1)]:
                print(full_filename)
                if 'Thumbs.db' in full_filename:
                    continue
                image = cv2.imread(full_filename)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # detect faces in the grayscale image
                # rects = detector(gray, 1)
                rects = detector(gray, 2)

                # loop over the face detections
                for (i, rect) in enumerate(rects):

                  faceAligned = fa.align(image, gray, rect)
                  faceAligned = faceAligned[35:256-31, 33:256-33]

                  cv2.imwrite(full_filename.replace(db_name, new_name), faceAligned)
                  #print('saved')

    except PermissionError:
        pass

#data_path = 'data/cohn-kanade-images'
#db_name = 'cohn-kanade-images'
#new_path = data_path.replace(db_name, 'ck_align')
data_path = '/data/OriginalImg/VL/Strong'
db_name = 'OriginalImg/VL/Strong'
new_name = 'oulu_align'

if not os.path.exists(new_path):
  os.makedirs(data_path.replace(db_name, new_name))

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('preprocessing/shape_predictor_68_face_landmarks.dat')
fa = FaceAligner(predictor, desiredFaceWidth=256)

search_files(data_path, db_name, detector, fa, new_path)

print('finished')
