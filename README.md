# Raspberry pi portable face recognition attendance system
A portable face recognition system created with a Raspberry Pi 3B+.
<p align="center">
<img src="https://user-images.githubusercontent.com/46261099/52633865-a4a08700-2f00-11e9-9021-52e97a7f9b20.jpg" width="334" height="250" />
<img src="https://user-images.githubusercontent.com/46261099/52636024-6ad27f00-2f06-11e9-8541-92db6999972e.jpg" width="334" height="250" />
</p>

## Introduction
The idea of this portable face recognition system was pioneered to replace the conventional
paper-based attendance system in universities. This system implements the idea of selfie and
Eigenface algorithm to recognize student faces in classes and saves the entire attendance details
of the class in a file.

## Concept of project
### Student registration
Since this is an attendance system, the students need to be registered to as database.
In PETRONAS Technology of Institute, students obtain their identification card by registering
themselves with the security department. Through this process, the students are required to
provice their personal details including name, student ID number, programme, intake. Likewise,
portraits of a student will be taken and the preferred one will be printed on his or her identification 
card. This project takes advantage on this process to register students into a database with the
pictures taken. After the registration of the new students to the database, all the face images in
the database are trained using Eigenface algorithm.
### Attendance taking in class
A small portable device which comprises of the entire circuit of the Raspberry Pi and other
components, is connected to a desktop via Wi-Fi in each class. What the lecturer has to do is just
come to class as usual, type the course code in the raspberry pi terminal running the script in
the desktop and pass the device to students just like ordinary attendance sheet. Students can then
use that device to take a selfie and the selfie captured will be compared with the trained images
taken during registration, according to the registered courses.
### End of class
After the end of attendance taking, a digital attendance sheet will be generated that displays
the course code, date, time and students that are present and absent for the particular class
session.

## Dependencies
* [Python 3.7](https://www.python.org/)
* [Opencv](http://opencv.org/)
* [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO)
* [Picamera](https://picamera.readthedocs.io/en/)
* [LCD_module](https://github.com/adafruit/Adafruit_Python_CharLCD)

## Parts used
* Raspberry Pi 3B+
* Raspberry Pi Camera Module v2
* 16x2 LCD module
* Power bank / Rechargeable batteries
* Mini pushbutton switch
* USB Micro B Cable
* Jumper cables
* 1k Ohm resistor

## Connections of circuit
* GPIO9     :  lcd_rs        
* GPIO10    : lcd_en        
* GPIO22    : lcd_d4        
* GPIO27    : lcd_d5        
* GPIO17    : lcd_d6        
* GPIO18    : lcd_d7       
* GPIO4     : lcd_backlight 
* GPIO23    : Between pull up resistor output and mini pushbutton switch

## Installing
Just put all the scripts in any preferred directory, the scripts will do the job of creating other
required directories.

## Usage
### Student registration
For the registration of the students, the script test_register.py should be executed.
```
sudo python test_register.py
```
By executing this script, students can register by entering name, student id and registered
course codes. Then, their portrait looks will be taken and stored in a folder that are named
after their name and ID number.
<img src="https://user-images.githubusercontent.com/46261099/52636400-73778500-2f07-11e9-977f-655268b23681.jpg"/>
### Image training
After student registration, the images are required to be trained or processed. In order
to train all the images, the script test_train.py should be executed.
```
sudo python test_train.py
```
By executing this script, all the images stored in the student database are trained by using
Eigenface algorithm and the training data will be stored in test_training.xml.
<img src="https://user-images.githubusercontent.com/46261099/52636529-d9fca300-2f07-11e9-9866-bfd372ef025b.jpg"/>
### Attendance taking
After training the all the student images, the image dataset is ready to be compared with.
In order to start the attendance taking process, the script test_attendance has to be executed.
```
python test_attendance.py
```
By executing this script, the lecturers can input the course code and commence the attendance
taking process.</br>
<img src="https://user-images.githubusercontent.com/46261099/52636866-b38b3780-2f08-11e9-8983-fc13cd87f235.jpg"/></br>
Students can then take their selfies using the device by pressing the push button. The capture selfies is then compared to
the trained image data stored in test_training.xml.</br>
<img src="https://user-images.githubusercontent.com/46261099/52637002-01a03b00-2f09-11e9-91f8-62044a7ead6f.jpg"  width="334" height="250" /></br>
Then, the student will be prompted for confirmation for the result of the identity prediction. Press the button if
prediction is wrong in order to retake another selfie, or wait for 5 seconds to confirm the prediction is correct.</br>
<img src="https://user-images.githubusercontent.com/46261099/52637117-53e15c00-2f09-11e9-85fa-cfbd5a94ab54.jpg"  width="504" height="220" /></br>
The system will detect if there is no face in the captured image and also identified student face that are already
marked as present.</br>
<img src="https://user-images.githubusercontent.com/46261099/52637277-c6523c00-2f09-11e9-8c03-81c012cece3c.jpg"  width="504" height="220" /></br>
<img src="https://user-images.githubusercontent.com/46261099/52637346-f7327100-2f09-11e9-9090-7aa2c142e634.jpg"  width="504" height="220" /></br>
After students have finished taking their attendances, only the lecturer has the authority to exit the
process. Upon exiting the process, an attendance file that lists the present and absent students will be
created for that particular class session. Recognized students who did not register for the course code
entered by the lecturer will be automatically removed by the system as well.</br>
<img src="https://user-images.githubusercontent.com/46261099/52637522-5f815280-2f0a-11e9-8344-ef45085a98e2.jpg"/>
An example of the attendance text file:</br>
<img src="https://user-images.githubusercontent.com/46261099/52637598-a53e1b00-2f0a-11e9-98d3-9b733358a9b5.jpg"/>
</br>
## Authors
* Jackson - jackson1412able@gmail.com

