# Main script for attendance taking process

import time
import sys
import select
import LCD_module as LCD
import os
import pickle
import RPi.GPIO as GPIO
import cv2
import test_config
import test_face

# Raspberry Pi pin configuration:
lcd_rs        =  9  
lcd_en        = 10
lcd_d4        = 22
lcd_d5        = 27
lcd_d6        = 17
lcd_d7        = 18
lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)

while True:
    path_course = './course'
    count = 0
    registered_course = []
    registered_ID = []
    registered_ID_current_course = []
    registered_names_current_course = []
    name = []
    ID = []
    i = []
    previous_id = []

    # Load student names from names.p to names
    f = open('names.p','r')
    names = pickle.load(f)
    f.close()

    # Load student id from labels.p to 
    f = open('labels.p','r')
    labels = pickle.load(f)
    f.close()
    
    checked_names = []
    checked_ID = []
    count = 0
    key = []
    time_count = 0
    

    def is_letter_input(letter):
            # Utility function to check if a specific character is available on stdin.
            # Comparison is case insensitive.
            if select.select([sys.stdin,],[],[],0.0)[0]:
                    input_char = sys.stdin.read(1)
                    return input_char.lower() == letter.lower()
            return False

    # Prompt lecturer for course code of current class   
    lcd.clear()
    lcd.message('Enter course\ncode')
    os.system("clear")
    current_course = raw_input("Course code for the current class: ")

    while True:

        # Load the student id and course registered into respective lists
        for index in range(len(os.listdir(path_course))):
            f = open(path_course+'/'+os.listdir(path_course)[index],'r')
            registered_course.append(pickle.load(f))
            registered_ID.append(str(os.listdir(path_course)[index]).split(".")[1])
            f.close()

        # Check if any course codes in registered_course matches current course code, then copy corresponding student id into registered_ID_current_course
        for index in range(len(registered_course)):
            for indexx in range(len(registered_course[index])):
                if current_course == registered_course[index][indexx]:
                    registered_ID_current_course.append(registered_ID[index])

        # Get index of student id in labels.p that matches the current course code
        for index in range(len(registered_ID_current_course)):
            for indexx in range(len(labels)):
                if previous_id == str(labels[indexx]):
                    continue
                else:
                    if str(labels[indexx]) == registered_ID_current_course[index]:
                        previous_id = registered_ID_current_course[index]
                        i.append(str(indexx))           

        # Through the indexes from labels.p, the student names that are registered can be obtained from names.p with the same indexes
        # These names are the ones that had registered/enroll in the current course
        # These names are copied to registered_names_current_course list
        for index in range(len(i)):
            registered_names_current_course.append(names[int(i[index])])

        # Print details of students that are registered in this course                  
        print "Names that are registered to this course {}".format(registered_names_current_course)
        print "ID's that are registered to this course :{}".format(registered_ID_current_course)

        # If there are at least one registered student in this course
        if len(registered_names_current_course) != 0:
            # Load training data into model
            lcd.clear()
            lcd.message('Loading\ntraining data...')
            print 'Loading training data...'
            model = cv2.createEigenFaceRecognizer()
            model.load(test_config.TRAINING_FILE)
            lcd.clear()
            lcd.message('Training\ndata loaded!')
            print 'Training data loaded!'
            # Initialize camera.
            camera = test_config.get_camera()
            lcd.clear()
            lcd.message('Press c to start\nPress z to end')
            while True:
                    key = raw_input('Press c to start taking attendance via facial recognition. Press z to cancel.\n')
                    if key == 'c':
                            break
                    if key == 'z':
                            os.system("clear")
                            break
            # If input key is 'c', start enabling students to take images
            if key == 'c':
                    os.system("clear")                
                    print 'Attendance taking started... Press x to end'
                    lcd.clear()
                    lcd.message('Press to capture\nyour face!')
                    # Check if capture should be made.
                    # TODO: Check if button is pressed.
                    while True:
                            # End by pressing 'x' key
                            if is_letter_input('x'):
                                key = 'x'
                                break
                            if not GPIO.input(23):
                                while GPIO.input(23):
                                        pass
                                os.system("clear")
                                print 'Attendance taking process is going on... Press x to end'
                                lcd.clear()
                                lcd.message('Identifying\nface...')
                                print 'Looking for face...'
                                # Check for the positive face and unlock if found.
                                image = camera.read()
                                # Convert image to grayscale.
                                image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                                # Get coordinates of single face in captured image.
                                result = test_face.detect_single(image)
                                # If no face is detected in captured image
                                if result is None:
                                        lcd.clear()
                                        lcd.message('Could not\ndetect face!')
                                        print 'Could not detect single face!'
                                # If face is detected in captured image
                                else:
                                        x, y, w, h = result
                                        # Crop and resize image to face.
                                        crop = test_face.resize(test_face.crop(image, x, y, w, h))
                                        # Test face against model, get the student id of the nearest match
                                        [label, confidence] = model.predict(crop)
                                        # If face captured is recognizable
                                        if confidence < 2500:
                                                # Compare the predicted student id with id in labels.p
                                                for index in range(len(labels)):
                                                        if labels[index] == label :
                                                                # Return the index of the matched id in labels.p
                                                                indexx = labels.index(labels[index])
                                                                break
                                                # Display results
                                                print 'Name: {}'.format(names[indexx])
                                                print 'ID  : {}'.format(label)
                                                print 'Confidence  : {}'.format(confidence)
                                                # If prediction is correct, wait awhile
                                                # If prediction is incorrect, press button on Rpi to retake image
                                                print 'Press if recognition is incorrect, wait if correct'
                                                lcd.clear()
                                                lcd.message('ID :%s? Press\nif incorrect.?' % label)
                                                for index in range(500):
                                                        time.sleep(0.007)
                                                        if index<100:
                                                                time_count=1
                                                        elif index <200:
                                                                time_count=2
                                                        elif index <300:
                                                                time_count=3
                                                        elif index <400:
                                                                time_count=4
                                                        elif index <500:
                                                                time_count=5
                                                        
                                                        time_count = 6 - time_count
                                                        lcd.set_cursor(15,1)
                                                        lcd.message(' %s' % str(time_count))
                                                        confirm = 1
                                                        if not GPIO.input(23):
                                                                while not GPIO.input(23):
                                                                        pass
                                                                confirm = 0
                                                                lcd.clear()
                                                                lcd.message('Press to \nrecapture face')
                                                                break
                                                if confirm == 1:
                                                        # Pass recognized student name and id to lists
                                                        checked_names.append(names[indexx])
                                                        checked_ID.append(label)
                                                        # Check if student is already recognized before in the same attendance taking process
                                                        for index in range(len(checked_names)):
                                                                if checked_names[index] == names[indexx]:
                                                                        count=count+1
                                                                        if count==2:
                                                                               lcd.clear()
                                                                               lcd.message('ID already\ntaken')
                                                                               checked_names.remove(checked_names[index])
                                                                               checked_ID.remove(label)
                                                                               break
                                                        if count != 2:
                                                                lcd.clear()
                                                                lcd.message('ID %s\nchecked!' % label)
                                                        count = 0
                                                        #break
                                                    
                                        else:
                                                # Unfamiliar face detected
                                                lcd.clear()
                                                lcd.message('Recognization\nfailed!')
                                                print 'Did not recognize face! Confidence ({})exceeded threshold'.format(confidence)
                                # Print names and id that are present in the class
                                print "names: {}".format(checked_names)
                                print "ID: {}".format(checked_ID)
            
            # 'x' pressed to end attendance taking process when class is ended
            if key =='x':
                os.system("clear")
                lcd.clear()
                lcd.message('Recordance\nended')                              
                print "Attendance taking ended for the course {}.".format(current_course)
                
                #To eliminate identified students that are not registered in the course entered by lecturer
                for index in range(len(checked_names)):
                    for indexx in range(len(registered_names_current_course)):
                        if registered_names_current_course[indexx] == checked_names[index]:
                            break
                        else:
                            count = count + 1
                            if count == len(registered_names_current_course):
                                name.append(checked_names[index])
                                ID.append(checked_ID[index])
                                continue
                            else:
                                continue
                if len(name) > 0:
                    for index in range (len(name)):
                        checked_names.remove(name[index])
                    for index in range (len(ID)):
                        checked_ID.remove(ID[index])
                        
                for index in range(len(checked_names)):
                    registered_names_current_course.remove(checked_names[index])
                    registered_ID_current_course.remove(str(checked_ID[index]))
                    
                lcd.clear()
                lcd.message('%s present\n' % len(checked_ID))
                lcd.message('%s absent' % len(registered_ID_current_course))

                # Print students that are present and absent in the course session
                print "Students that are present: {}".format(checked_names)
                print "ID's that are present    : {}".format(checked_ID)
                print "Students that are absent : {}".format(registered_names_current_course)
                print "ID's that are not present: {}".format(registered_ID_current_course)
                break
        else:
            # If no students are registered in the course entered by the lecturer
            os.system("clear")
            print "There are no registered students for this course."
        count = 0
        registered_course = []
        registered_ID = []
        registered_ID_current_course = []
        registered_names_current_course = []
        name = []
        ID = []
        i = []
        previous_id = []
        lcd.clear()
        lcd.message('Enter course\ncode')
        current_course = raw_input("Course code for the current class: ")

    # Preparation of attendance list upon ending of class session
    f = open("./attendance_list" + "/" + current_course + "_" + "attendance","w+")
    f.write("Attendance for ")
    f.write(current_course + "\n")
    f.write("Date: %10s" % time.strftime("%x"))
    f.write("        Time: %10s\n\n" % time.strftime("%X"))
    f.write("Student(s) that are present:\n")
    f.write("__________________________________________________\n")
    f.write("Index                   Name           ID\n")
    f.write("--------------------------------------------------\n")

    # Printing students that are present in the class session
    for index in range(len(checked_names)):
        f.write("%3s" % str(index+1))
        f.write("%25s" % checked_names[index])
        f.write("%13s\n" % str(checked_ID[index]))

    f.write("\n\nStudent(s) that are absent:\n")
    f.write("__________________________________________________\n")
    f.write("Index                   Name           ID\n")
    f.write("--------------------------------------------------\n")

    # Printing students that are absent in the class session
    for index in range(len(registered_names_current_course)):
        f.write("%3s" % str(index+1))
        f.write("%25s" % registered_names_current_course[index])
        f.write("%13s\n" % str(registered_ID_current_course[index]))

    f.close()
    lcd.clear()
    lcd.message('File created for\n%s' % current_course)
    print "Attendance for " + current_course + " is generated."
    print "Filename: " + current_course + "_" + "attendance" + ".txt"
    
    again = []

    # Prompt whether to start a new attendance taking process for another class session
    while True:
        del again
        again = raw_input("Take attendance for another class? Yes(y) or No(n)\n")
        if again == 'y':
            break
        elif again == 'n':
            break
        
    if again == 'y':
        os.system("clear")
        continue
    if again == 'n':
        os.system("clear")
        break
