# Register students with their registered courses by taking their photos at a booth.
# Run this script to capture positive images for training the face recognizer.

import glob
import os
import sys
import select
import pickle
import cv2
import test_config
import test_face

# Prefix for positive training image filenames.
POSITIVE_FILE_PREFIX = 'positive_'

def is_letter_input(letter):
	# Utility function to check if a specific character is available on stdin.
	# Comparison is case insensitive.
	if select.select([sys.stdin,],[],[],0.0)[0]:
		input_char = sys.stdin.read(1)
		return input_char.lower() == letter.lower()
	return False

if __name__ == '__main__':
	camera = test_config.get_camera()
	var = 1  # Dummy variable
	std_id = []
	std_id_previous = []
	while True :
                print 'Registration for new students'
                # Prompt student for name, id and registered courses
                std_name = raw_input("Student name: ")
                std_id = raw_input("Student id: ")
                course = raw_input("Enter registered course codes, separated by commas: ")
                std_course = course.split(',')

                # Create a file of each student that stores each registered course by them
                # COURSE_LIST = './course'
                f = open(test_config.COURSE_LIST + '/' + 'course' + ‘.’ + std_id + '.p','w')
                pickle.dump(std_course, f)
                f.close()
                
                # Directory for storing student images
                directory = test_config.POSITIVE_DIR
                directory += '/s'
                directory += std_id
                directory += '.'
                directory += std_name
                
                # Create the directory for positive training images if it doesn't exist.
                if not os.path.exists(directory):
                        os.makedirs(directory)
                        
                # Photo taking process
                count = len(os.listdir(directory)) + 1
                key = raw_input('Press button or type c (and press enter) to capture an image, z to quit.')
                while True:
                        # Check if button was pressed or 'z' was received, then stop capturing image.
                        if key == 'z':
                                break
                        # Check if button was pressed or 'c' was received, then capture image.
                        if key == 'c':
                                print 'Capturing image...'
                                image = camera.read()
                                # Convert image to grayscale.
                                image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                                # Get coordinates of single face in captured image.
                                result = test_face.detect_single(image)
                                # If no face is detected in captured image.
                                if result is None:
                                        print 'Could not detect single face!'
                                        var = 0
                                # If face is detected, save.
                                if var == 1:
                                        x, y, w, h = result
                                        # Crop image as close as possible to desired face aspect ratio.
                                        # Might be smaller if face is near edge of image.
                                        crop = test_face.crop(image, x, y, w, h)
                                        # Save image to file.
                                        filename = os.path.join(directory, 'subject' + '%s.' %std_id + '%s.' %std_name + '%d.pgm' % count)
                                        cv2.imwrite(filename, crop)
                                        print 'Found face and wrote training image', filename
                                        count += 1
                                var = 1
                        print ''                
                        key = raw_input('')
