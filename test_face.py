# Face Detection Helper Functions
# Functions to help with the detection and cropping of faces.

import cv2
import test_config

haar_faces = cv2.CascadeClassifier(test_config.HAAR_FACES)

# Return bounds (x, y, width, height) of detected face in grayscale image.
# If no face or more than one face are detected, None is returned.
def detect_single(image):
	faces = haar_faces.detectMultiScale(image, 
				scaleFactor=test_config.HAAR_SCALE_FACTOR, 
				minNeighbors=test_config.HAAR_MIN_NEIGHBORS, 
				minSize=test_config.HAAR_MIN_SIZE, 
				flags=cv2.CASCADE_SCALE_IMAGE)
	if len(faces) != 1:
		return None
	return faces[0]

# Crop box defined by x, y (upper left corner) and w, h (width and height)
# to an image with the same aspect ratio as the face training data.  Might
# return a smaller crop if the box is near the edge of the image.
def crop(image, x, y, w, h):
	crop_height = int((test_config.FACE_HEIGHT / float(test_config.FACE_WIDTH)) * w)
	midy = y + h/2
	y1 = max(0, midy-crop_height/2)
	y2 = min(image.shape[0]-1, midy+crop_height/2)
	return image[y1:y2, x:x+w]

# Resize a face image to the proper size for training and detection.
def resize(image):
	return cv2.resize(image, (test_config.FACE_WIDTH, test_config.FACE_HEIGHT), interpolation=cv2.INTER_LANCZOS4)
