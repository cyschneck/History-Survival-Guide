# Generate a star chart for astrolabe
# python3 generate_declination_ruler.py
import numpy as np
import matplotlib.pyplot as plt
import math

def triggerDeclinationCalculations(dec_min, dec_max):
	# access via script in generate_star_chart
	graphPlotsegments = True # should plot the segments on a graph
	total_ruler_length = 30
	declination_ruler_dict = calculateRuler(graphPlotsegments, total_ruler_length, dec_min, dec_max)
	return declination_ruler_dict

def calculateLength(angle_of_inclination):
	# convert angle into length of radius
	angle_in_radians = np.deg2rad((90 - angle_of_inclination)/2)
	equation_of_length = math.tan(angle_in_radians) # calculated
	return equation_of_length

def calculateRuler(graphPlotSegments, total_ruler_length, declination_min, declination_max):
	# define the length of each segment in ruler when radius = 1
	x_angleOfDeclination = np.arange(-80,90,10)
	y_lengthSegments = []

	# convert segments into length segments
	for angle_of_inclination in x_angleOfDeclination:
		length_of_segment = calculateLength(angle_of_inclination)
		#print("{0}  = {1:.4f}".format(angle_of_inclination, length_of_segment))
		y_lengthSegments.append(length_of_segment)

	# optional graph of segments
	if graphPlotSegments:
		plotLengthSegments(x_angleOfDeclination, y_lengthSegments)

	# Calculate the ruler based on a ruler length and the range of the declinations
	length_of_the_ruler_to_be_used = total_ruler_length/2 # cut ruler in half

	declination_angles_ruler = np.arange(declination_min, declination_max+1, 10)
	#print("\nDeclination Range of Angles: {0}".format(declination_angles_ruler))

	total_ruler_ratio_length = 0
	for angle_declination in declination_angles_ruler:
		#print("{0:.4f} + {1:.4f} = {2:.4f}".format(total_ruler_ratio_length, calculateLength(angle_declination), total_ruler_ratio_length + calculateLength(angle_declination)))
		total_ruler_ratio_length += calculateLength(angle_declination)
	#print("Total length of ruler with r = 1: {0}".format(total_ruler_ratio_length))
	#print("Length of ruler to compare to (1/2 total) = {0} cm".format(length_of_the_ruler_to_be_used))

	ratio_of_ruler = length_of_the_ruler_to_be_used / total_ruler_ratio_length
	#print("Ratio of ruler: {0}".format(ratio_of_ruler))
	ruler_position_dict = {} # dict: {degree : position_on_ruler }
	ruler_position_for_n = 0
	for n_angle in reversed(declination_angles_ruler): # add values from the largest to the smallest to account for declination lines
		ruler_position_for_n += calculateLength(n_angle)*ratio_of_ruler
		print("Degree Segment: {0} = {1:.4f}*{2:.4f} = {3:.4f} = {4:.4f} cm".format(n_angle,
																				calculateLength(n_angle),
																				ratio_of_ruler,
																				calculateLength(n_angle)*ratio_of_ruler,
																				ruler_position_for_n))
		ruler_position_dict[n_angle] = ruler_position_for_n
	return ruler_position_dict

def plotLengthSegments(x_degreeSegments, y_lengthSegments):
	# plot segments (n) vs. Length of segments
	plt.xticks(x_degreeSegments)
	plt.title("Length of Declination Ruler Segments: tan(90 - angle) * (1/2)")
	plt.xlabel("Degree")
	plt.ylabel("Length of Segments when r = 1")
	plt.scatter(x_degreeSegments, y_lengthSegments)
	plt.show()

if __name__ == '__main__':
	# Generate and plot
	ruler_position_dict = triggerDeclinationCalculations(dec_min = -30, dec_max = 90)
	print(ruler_position_dict)
