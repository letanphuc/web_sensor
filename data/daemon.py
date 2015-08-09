#!/usr/bin/python
import os
import sys
import random
import time

import RPi.GPIO as GPIO

PATH = '/var/www/data/'

class UltraSonicSensor:
	def __init__ (self):
		GPIO.setmode(GPIO.BCM)
		self.GPIO_TRIGGER = 2
		self.GPIO_ECHO = 3
		# Set pins as output and input
		GPIO.setup(self.GPIO_TRIGGER,GPIO.OUT)  # Trigger
		GPIO.setup(self.GPIO_ECHO,GPIO.IN)      # Echo
		
		time.sleep(0.5)

	def getValue(self):
		# Set trigger to False (Low)
		GPIO.output(self.GPIO_TRIGGER, False)

		# Send 10us pulse to trigger
		GPIO.output(self.GPIO_TRIGGER, True)
		time.sleep(0.00001)
		GPIO.output(self.GPIO_TRIGGER, False)
		start = time.time()
		
		while GPIO.input(self.GPIO_ECHO)==0:
		  start = time.time()

		while GPIO.input(self.GPIO_ECHO)==1:
		  stop = time.time()

		# Calculate pulse length
		elapsed = stop-start
		print "elapsed = ", elapsed

		# Distance pulse travelled in that time is time
		# multiplied by the speed of sound (cm/s)
		distance = elapsed * 34000

		# That was the distance there and back so halve the value
		distance = distance / 2

		return distance


def read_time():
	line = open(PATH + 'test', 'r').readline().strip()
	if 'stop' in line:
		return -1
	else:
		return int(line)
def handle_number_of_sensor():
	# TODO: read number of sensor connected with host save to number_of_sensor file and return
	os.system('echo 1 > number_of_sensor')
	# line = open(PATH + 'number_of_sensor', 'r').readline().strip()
	# if '' == line:
	# 	return -1
	# else:
	# 	return int(line)
	return 1

def main():
	begin = True
	state = 0
	time_interval = 0
	output = None
	number_of_sensor = handle_number_of_sensor()
	t = 0
	sensor = UltraSonicSensor()
	led = True
	GPIO.setup(4, GPIO.OUT)

	while (1):
		# time.sleep
		print state
		time_interval = read_time()
		if state == 0: 
			if time_interval != -1:
				state = 1
				output = open(PATH + 'data.xml', 'w')
				output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
				output.write('<result>\n')
				t = 0
			else:
				# update number of sensor 2 times a second
				number_of_sensor = handle_number_of_sensor()
				led = not led
				if (led):
					GPIO.output(4, GPIO.HIGH)
				else:
					GPIO.output(4, GPIO.LOW)
				time.sleep(0.5)
		else:
			if time_interval == -1:
				state = 0
				output.write('</result>\n')
				output.close()

			else:
				start = time.time()
				t += time_interval
				output.write('<item>\n')
				output.write('<t>%d</t>\n' %t)

				for i in range(0, number_of_sensor):
					output.write('<sensor>%f</sensor>\n' %sensor.getValue())
				output.write('</item>\n')
				cycle = time_interval / 1000.0
				start = time.time() - start
				if (start < cycle):
					time.sleep(cycle - start)



if __name__ == '__main__':
	main()
