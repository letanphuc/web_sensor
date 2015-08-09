import time
import RPi.GPIO as GPIO
from pykalman import KalmanFilter
import numpy as np


class UltraSonicSensor:
	def __init__ (self):
		GPIO.setmode(GPIO.BCM)
		self.GPIO_TRIGGER = 2
		self.GPIO_ECHO = 3
		# Set pins as output and input
		GPIO.setup(self.GPIO_TRIGGER,GPIO.OUT)  # Trigger
		GPIO.setup(self.GPIO_ECHO,GPIO.IN)      # Echo
		time.sleep(0.5)
		kf = KalmanFilter(transition_matrices = [[1, 1], [0, 1]], observation_matrices = [[0.1, 0.5], [-0.3, 0.0]])

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

# Test code
# x = UltraSonicSensor()
# while 1:
# 	s = time.time()
# 	print "Value = %f (cm)" %x.getValue()
# 	s = time.time() - s
# 	if (s < 0.2):
# 		time.sleep(float(0.2 - s))