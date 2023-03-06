# controller library
import pygame

# Robot Library
import RPi.GPIO as GPIO
import time

#Definition of servo pin
ServoPin = 23

#Definition of  motor pin 
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#Set the GPIO port to BCM encoding mode.
GPIO.setmode(GPIO.BCM)

#Ignore warning information
GPIO.setwarnings(False)

global pos
global axis1
global axis2
global axis3
global axis4
global axis5

def remote_init():
    # joystick init
    pygame.init()
    joysticks = []

    # init joystick
    global joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    
    
    # for all the connected joysticks
    for i in range(0, pygame.joystick.get_count()):
        # create an Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
        # initialize them all (-1 means loop forever)
        joysticks[-1].init()
        # print a statement telling what the name of the controller is
        print ("Detected joystick "),joysticks[-1].get_name(),"'"
    global axis1
    global axis2
    global axis3
    global axis4
    global axis5   
    axis1 = 0
    axis2 = 0
    axis3 = 0
    axis4 = 0
    axis5 = 0
    

def motor_init():
    #Motor pin initialization operation
    global pwm_ENA
    global pwm_ENB
    global delaytime
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    #Set the PWM pin and frequency is 2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)

def servo_init():    
    GPIO.setup(ServoPin, GPIO.OUT)
    global pwm_servo
    pwm_servo = GPIO.PWM(ServoPin, 50)
    pwm_servo.start(0)
    
    global pos
    pos = 0

def init():
    remote_init()
    motor_init()
    servo_init()

#advance
def run(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)
    time.sleep(delaytime)

#back
def back(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)
    time.sleep(delaytime)

#brake
def brake(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)
    time.sleep(delaytime)

def remote_input():
    # Loads every event that can be called
    for event in pygame.event.get():
        # The 0 button is the 'a' button, 1 is the 'b' button, 3 is the 'x' button, 4 is the 'y' button
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                print ("A Has Been Pressed")
            elif event.button == 1:
                print ("B Has Been Pressed")                
            elif event.button == 3:
                print ("X Has Been Pressed")
            elif event.button == 4:
                print ("Y Has Been Pressed")
            elif event.button == 12:
                keepPlaying = False;
            else:
                print (event.button)
                
        # joystick event
        if event.type == pygame.JOYAXISMOTION:
            # Left joystick
            # axis0 is left right input, axis1 is up down
            axis0 = round(joystick.get_axis(0), 2)
            axis1 = -round(joystick.get_axis(1), 2)
            
            # Right joystick
            # axis2 is left right input, axis3 is up down
            axis2 = round(joystick.get_axis(2), 2)
            axis3 = -round(joystick.get_axis(3), 2)
            
            # Left Trigger
            axis4 = round(joystick.get_axis(5), 2)
            
            # Right Trigger
            axis5 = round(joystick.get_axis(4), 2)
            
            print("pos {}".format(pos))
            # print info
            print("Left joystick: x:{} y:{}".format(axis0, axis1))
            #print("Right joystick: x:{} y:{}".format(axis2, axis3*-1))
            #print("Left trigger: {}".format(axis4))
            #print("Right trigger: {}".format(axis5))

# initializes the clock and makes sure the game will keep playing
clock = pygame.time.Clock()
global keepPlaying
keepPlaying = True

# initializes remote, servo, and motor
init()
    
# main game
while keepPlaying:
    clock.tick(60)
    
    # checks if the remote is telling the robot to move forward
    if(axis1 > 0):
        run(0)
    elif(axis1 < 0):
        back(0)
    else:
        brake(0)
    
    # changes the servo pos
    if(axis4 > 0):
        pos -= .1    
    if(axis5 > 0):
        pos += .1
    
    # makes sure servo does not go over its limit
    if(pos > 100):
        pos = 100
    elif(pos < 0):
        pos = 0
    
    # moves servo to needed position
    pwm_servo.ChangeDutyCycle(pos)
    
    # Loads every event that can be called
    for event in pygame.event.get():
        # The 0 button is the 'a' button, 1 is the 'b' button, 3 is the 'x' button, 4 is the 'y' button
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                print ("A Has Been Pressed")
            elif event.button == 1:
                print ("B Has Been Pressed")                
            elif event.button == 3:
                print ("X Has Been Pressed")
            elif event.button == 4:
                print ("Y Has Been Pressed")
            elif event.button == 12: # kills the program
                keepPlaying = False;
            else:
                print (event.button)
                
        # joystick event
        if event.type == pygame.JOYAXISMOTION:
            # Left joystick
            # axis0 is left right input, axis1 is up down
            axis0 = round(joystick.get_axis(0), 2)
            axis1 = -round(joystick.get_axis(1), 2)
            
            # Right joystick
            # axis2 is left right input, axis3 is up down
            axis2 = round(joystick.get_axis(2), 2)
            axis3 = -round(joystick.get_axis(3), 2)
            
            # Left Trigger
            axis4 = round(joystick.get_axis(5), 2)
            
            # Right Trigger
            axis5 = round(joystick.get_axis(4), 2)
                        
            # print info
            #print("servo pos {}".format(pos))
            #print("Left joystick: x:{} y:{}".format(axis0, axis1))
            #print("Right joystick: x:{} y:{}".format(axis2, axis3*-1))
            #print("Left trigger: {}".format(axis4))
            #print("Right trigger: {}".format(axis5))


# stops components
pwm_servo.stop()
pwm_ENA.stop()
pwm_ENB.stop()
GPIO.cleanup() 