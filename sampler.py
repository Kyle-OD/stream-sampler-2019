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

firebase = firebase.FirebaseApplication('https://stream-sampler.firebaseio.com/') #Set Firebase URL
time.sleep(3)
result = '0'

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT); #Pin for Motor backwards
GPIO.setup(23, GPIO.OUT); #Pin for Moror forwards
GPIO.setup(24, GPIO.OUT); #Pin for Pump in
GPIO.setup(25, GPIO.OUT); #Pin for Pump out
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN);  #Pin for sample button
GPIO.setup(27, GPIO.OUT); #Pin for H-Bridge ENA Signal


while True:	#Execution loop

	#################### INTERNET CHECK ######################
	#Uses try/except to catch any possible loss of internet service
	try:
		result = firebast.get('Data', None)
		if(result!=0):
			firebase.put('','Data','0);
			firebase.put('','Received',1);
			execute_command()
			firebase.put('','Sample',1);
			time.sleep(2)
		time.sleep(5)
	except:
		time.sleep(20)

	#################### BUTTON COMMANDS #####################
	try:
		if GPIO.input(17) == GPIO.HIGH: #Checks if button is pressed
			execute_command()
			time.sleep(2)
	except:
		time.sleep(1)


	time.sleep(2)

def execute_command():
	#Motor to zero position***************************

	GPIO.output(18,1) #Turn motor on
	GPIO.output(27,1) #ENA signal on
	time.sleep(1) #SET TO TIME IT TAKES TO RESET
	GPIO.output(18,0) #Turn motor off
	GPIO.output(27,0) #ENA signal off
	#*************************************************

	#Motor to down position***************************

	GPIO.output(23,1) #Turn motor on
	GPIO.output(27,1) #ENA signal on
	time.sleep(1) #SET TO TIME IT TAKES TO GO DOWN
	GPIO.output(23,0) #Turn motor off
	GPIO.output(27,0) #ENA signal off
	#*************************************************

	#Pump flush --> fill******************************

	GPIO.output(18,1) #Turn fill pump on
	time.sleep(1) #SET TO TIME IT TAKES TO FILL
	GPIO.output(18,0) #Turn fill pump off
	GPIO.output(18,1) #Turn flush pump on
	time.sleep(1) #SET TO TIME IT TAKES TO FLUSH
	GPIO.output(18,0) #Turn flush pump off
	GPIO.output(18,1) #Turn fill pump on
	time.sleep(1) #SET TO TIME IT TAKES TO FILL
	GPIO.output(18,0) #Turn fill pump off
	#*************************************************

	#Motor to zero position***************************
	GPIO.output(18,1) #Turn motor on
	GPIO.output(27,1) #ENA signal on
	time.sleep(1) #SET TO TIME IT TAKES TO RESET
	GPIO.output(18,0) #Turn motor off
	GPIO.output(27,0) #ENA signal off
	#*************************************************

