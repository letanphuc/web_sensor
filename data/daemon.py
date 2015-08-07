import os
import sys
import random
import time

def read_time():
	line = open('test', 'r').readline().strip()
	if 'stop' in line:
		return -1
	else:
		return int(line)
def read_number_of_sensor():
	line = open('number_of_sensor', 'r').readline().strip()
	if '' == line:
		return -1
	else:
		return int(line)

def main():
	begin = True
	state = 0
	time_interval = 0
	output = None
	number_of_sensor = read_number_of_sensor()
	t = 0

	while (1):
		# time.sleep
		time_interval = read_time()
		if state == 0: 

			if time_interval != -1:
				state = 1
				output = open('data.xml', 'w')
				output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
				output.write('<result>\n')
				t = 0
			else:
				time.sleep(0.5)
		else:
			if time_interval == -1:
				state = 0
				output.write('</result>\n')
				output.close()

			else:
				t += time_interval
				output.write('<item>\n')
				output.write('<t>%d</t>\n' %t)

				for i in range(0, number_of_sensor):
					output.write('<sensor>%f</sensor>\n' %random.random())
				output.write('</item>\n')

				time.sleep(time_interval / 1000.0)



if __name__ == '__main__':
	main()