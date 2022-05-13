# Generate a declination ruler for astrolabe star chart
# Triggered within generate_star_chart.py

import numpy as np
import matplotlib.pyplot as plt
import math

def triggerDeclinationCalculations(ruler_length, dec_min, dec_max, increment):
	# access via script in generate_star_chart
	graphPlotsegments = False # should plot the segments on a graph
	total_ruler_length = ruler_length
	declination_ruler_dict = calculateRuler(graphPlotsegments, total_ruler_length, dec_min, dec_max, increment)
	return declination_ruler_dict

def calculateLength(angle_of_inclination, radius_of_circle):
	# convert angle into length of radius
	#print("Angle {0} = Angle {1}".format(angle_of_inclination, 45-angle_of_inclination/2))
	angle_in_radians = np.deg2rad(45 - angle_of_inclination/2)
	equation_of_length = radius_of_circle * math.tan(angle_in_radians) # calculated
	return equation_of_length

def calculateRadiusOfCircle(min_dec, total_ruler_len):
	# calculate radius of full circle from -80 to 80 where min dec is the radius of smaller circle
	radius_of_circle_at_min_dec = (total_ruler_len/2) / math.tan(np.deg2rad(45 - min_dec/2))
	#print("Min declination = {0} for ruler length [{1} cm] = radius of {2:.4f}".format(min_dec, total_ruler_len/2, radius_of_circle_at_min_dec))
	return radius_of_circle_at_min_dec

def calculateRuler(graphPlotSegments, total_ruler_length, declination_min, declination_max, increment):
	# define the length of each segment in ruler when radius = 1
	x_angleOfDeclination = np.arange(-80, 80+1,increment) # declination max range from -80 to 80
	y_lengthSegments = []

	declination_angles_ruler = np.arange(-80, 80+1, increment) # declination max range from -80 to 80
	#print("\nDeclination Range of Angles: {0}".format(declination_angles_ruler))

	# calculate full size of circle to find declination for smaller range
	radius_of_circle = calculateRadiusOfCircle(declination_min, total_ruler_length)
	ruler_position_dict = {} # dict: {degree : position_on_ruler }
	for n_angle in declination_angles_ruler:
		ruler_position = calculateLength(n_angle, radius_of_circle)
		y_lengthSegments.append(ruler_position)
		if n_angle >= declination_min and n_angle <= declination_max:
			ruler_position_dict[n_angle] = round(ruler_position, 4)
			print("Angle {0} = {1:.4f} cm".format(n_angle, ruler_position))

	# optional graph of segments
	if graphPlotSegments:
		plotLengthSegments(x_angleOfDeclination, y_lengthSegments)

	return ruler_position_dict

def plotLengthSegments(x_degreeSegments, y_lengthSegments):
	# plot segments (n) vs. Length of segments
	fig = plt.figure(figsize=(10,10), dpi=100)
	ax = fig.subplots()
	plt.xticks(x_degreeSegments)
	plt.title("Length of Declination Ruler Position: tan(45 - angle/2) * (1/2)")
	plt.xlabel("Degree")
	plt.ylabel("Length")
	plt.scatter(x_degreeSegments, y_lengthSegments)
	plt.show()
