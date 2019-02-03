# Run this script to train the face recognition system with positive and negative
# training images.  The face recognition model is based on the eigen faces
# algorithm implemented in OpenCV.  You can find more details on the algorithm
# and face recognition here:
# http://docs.opencv.org/modules/contrib/doc/facerec/facerec_tutorial.html

import fnmatch
import os
import cv2
import numpy as np
import pickle
from PIL import Image
import test_config
import test_face

MEAN_FILE = 'test_mean.png'
POSITIVE_EIGENFACE_FILE = 'test_positive_eigenface.png'
NEGATIVE_EIGENFACE_FILE = 'test_negative_eigenface.png'

def walk_files(directory, match='*'):
	# Generator function to iterate through all files in a directory recursively
	# which match the given filename match parameter.
	for root, dirs, files in os.walk(directory):
		for filename in fnmatch.filter(files, match):
			yield os.path.join(root, filename)

def prepare_image(filename):
	# Read an image as grayscale and resize it to the appropriate size for
	# training the face recognition model.
	return test_face.resize(cv2.imread(filename, cv2.IMREAD_GRAYSCALE))

def normalize(X, low, high, dtype=None):
	# Normalizes a given array in X to a value between low and high.
	# Adapted from python OpenCV face recognition example at:
	# https://github.com/Itseez/opencv/blob/2.4/samples/python2/facerec_demo.py
	X = np.asarray(X)
	minX, maxX = np.min(X), np.max(X)
	# normalize to [0...1].
	X = X - float(minX)
	X = X / float((maxX - minX))
	# scale to [low...high].
	X = X * (high-low)
	X = X + low
	if dtype is None:
		return np.asarray(X)
	return np.asarray(X, dtype=dtype)


if __name__ == '__main__':
	print "Reading training images..."
	
	faces = []
	names = []
	labels = []
	pos_count = 0
	neg_count = 0
	
	mainpath = 'training'
        path1 = []
        path1 = [os.path.join(mainpath, f) for f in os.listdir(mainpath)]
	for index in range(len(os.listdir(mainpath))):
                # Go through every images
                for filename in walk_files(path1[index], '*.pgm'):
                        # Get student id from image name
                        nbr = int(os.path.split(filename)[1].split(".")[0].replace("subject", ""))
                        # Get student name from image name
                        student_name = os.path.split(filename)[1].split(".")[1].replace("subject", "")
                        # Store resized face images in faces[]
                        faces.append(prepare_image(filename))
                        # Store all student names into names[]
                        names.append(student_name)
                        # Store all student id into labels[]
                        labels.append(nbr)       

	# Train model
	print 'Training model...'
	model = cv2.createEigenFaceRecognizer()
	model.train(np.asarray(faces), np.asarray(labels))

	# Save model results
	model.save(test_config.TRAINING_FILE)
	print 'Training data saved to', test_config.TRAINING_FILE

	# Save mean and eignface images which summarize the face recognition model.
	mean = model.getMat("mean").reshape(faces[0].shape)
	cv2.imwrite(MEAN_FILE, normalize(mean, 0, 255, dtype=np.uint8))
	eigenvectors = model.getMat("eigenvectors")
	pos_eigenvector = eigenvectors[:,0].reshape(faces[0].shape)
	cv2.imwrite(POSITIVE_EIGENFACE_FILE, normalize(pos_eigenvector, 0, 255, dtype=np.uint8))
	neg_eigenvector = eigenvectors[:,1].reshape(faces[0].shape)
	cv2.imwrite(NEGATIVE_EIGENFACE_FILE, normalize(neg_eigenvector, 0, 255, dtype=np.uint8))

        #Saving student names and id in files
        f = open('names.p','w')
        pickle.dump(names, f)
        f.close()

        f = open('labels.p','w')
        pickle.dump(labels, f)
        f.close()
