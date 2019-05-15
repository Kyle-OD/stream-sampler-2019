#################################################################################################################
#    Author: Kyle O'Donnell
#    Contact: kpod@udel.edu
#    Project: Remote Stream Sampler; MEEG 304 - Machine Design II
#    Organization: University of Delaware
#################################################################################################################
from firebase import firebase
import time
import serial
import RPi.GPIO as GPIO


def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)  # Pin for Motor backwards
    GPIO.setup(23, GPIO.OUT)  # Pin for Motor forwards
    GPIO.setup(24, GPIO.OUT)  # Pin for Pump in
    GPIO.setup(25, GPIO.OUT)  # Pin for Pump out
    GPIO.setup(27, GPIO.OUT)  # Pin for H-Bridge ENA Signal
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Pin for sample button
    GPIO.output(18, False)
    GPIO.output(23, False)
    GPIO.output(24, False)
    GPIO.output(25, False)
    GPIO.output(27, False)


def motor_backwards():
    # Motor to zero position***************************
    GPIO.clean()
    init()
    GPIO.output(18, True)  # Turn motor on
    GPIO.output(23, False)
    GPIO.output(27, True)  # ENA signal on
    time.sleep(1)  # SET TO TIME IT TAKES TO RESET
    GPIO.output(18, 0)  # Turn motor off
    GPIO.output(27, 0)  # ENA signal off
    # *************************************************


def motor_forwards():
    # Motor to down position***************************
    GPIO.clean()
    init()
    GPIO.output(23, 1)  # Turn motor on
    GPIO.output(27, 1)  # ENA signal on
    time.sleep(1)  # SET TO TIME IT TAKES TO GO DOWN
    GPIO.output(23, 0)  # Turn motor off
    GPIO.output(27, 0)  # ENA signal off
    # *************************************************


def pump_sequence():
    # Pump flush --> fill******************************
    GPIO.clean()
    init()
    GPIO.output(18, 1)  # Turn fill pump on
    time.sleep(1)  # SET TO TIME IT TAKES TO FILL
    GPIO.output(18, 0)  # Turn fill pump off
    GPIO.output(18, 1)  # Turn flush pump on
    time.sleep(1)  # SET TO TIME IT TAKES TO FLUSH
    GPIO.output(18, 0)  # Turn flush pump off
    GPIO.output(18, 1)  # Turn fill pump on
    time.sleep(1)  # SET TO TIME IT TAKES TO FILL
    GPIO.output(18, 0)  # Turn fill pump off
    # *************************************************


def run_sequence():
    motor_backwards()
    motor_forwards()
    pump_sequence()
    motor_backwards()


firebase = firebase.FirebaseApplication('https://stream-sampler.firebaseio.com/')  # Set Firebase URL
time.sleep(3)
result = '0'
init()

while True:  # Execution loop

    # ################ INTERNET CHECK #####################
    # Uses try/except to catch any possible loss of internet service
    try:
        result = firebase.get('Data', None)
        if result != 0:
            firebase.put('', 'Data', 0)
            firebase.put('', 'Received', 1)
            run_sequence()
            firebase.put('', 'Sample', 1)
            time.sleep(2)
        time.sleep(5)
    except:
        time.sleep(20)

    # ################ BUTTON COMMANDS ####################
    try:
        if GPIO.input(17) == GPIO.HIGH:  # Checks if button is pressed
            run_sequence()
            time.sleep(2)
    except:
        time.sleep(1)

    time.sleep(2)
