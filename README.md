# Raspberry pi portable face recognition attendance system
A portable face recognition system created with a Raspberry Pi 3B+.

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

## Running the scripts
For the registration of the students, the script test_register.py should be executed.
```
sudo python test_register.py
```
By executing this script, students can register by entering name, student id and registered
course codes. Then, their portrait looks will be taken and stored in a folder that are named
after their name and ID number.
</br>
Email me at jackson1412able@gmail.com if you have any questions regarding this project.
