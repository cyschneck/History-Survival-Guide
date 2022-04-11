# Generate a star chart for astrolabe
# python3 generate_declination_ruler.py
import numpy as np
import matplotlib.pyplot as plt
import math

def convertSegmentToDegree(segment_n):
	# convert segment (n) to a degree value
	angle_of_inclination = 90 - (segment_n*10)
	return angle_of_inclination

def rulerLengthSegments(graphPlotSegments):
	# define the length of each segment in ruler when radius = 1
	x_degreeSegments = np.arange(1,18,1)
	y_lengthSegments = []

	# convert segments into length segments
	for segment_in_circle in x_degreeSegments:
		angle_of_inclination = convertSegmentToDegree(segment_in_circle)

		segment_in_radians = (segment_in_circle * np.pi / 180)
		equation_of_length = math.tan(5*segment_in_radians) # previous
		#equation_of_length = math.tan((angle_of_inclination))/2 # temp

		print("segment: {0} = {1} = {2:.4f}".format(segment_in_circle, angle_of_inclination, equation_of_length))
		y_lengthSegments.append(equation_of_length)

	# optional graph of segments
	if graphPlotsegments:
		plotLengthSegments(x_degreeSegments, y_lengthSegments)

	# calculate the ruler
	calculateRuler(y_lengthSegments, equation_of_length)

def plotLengthSegments(x_degreeSegments, y_lengthSegments):
	# plot segments (n) vs. Length of segments
	plt.xticks(x_degreeSegments)
	plt.title("Length of Declination Ruler segments: EQUATION")
	plt.xlabel("Degree segments")
	plt.ylabel("Length of segment when r = 1")
	plt.scatter(x_degreeSegments, y_lengthSegments)
	plt.show()

def calculateRuler(rulerSegments, equation_of_length):
	# Calculate the ruler based on a ruler length and the range of the declinations
	length_of_the_ruler_to_be_used = 15 # cm

	declination_range_min = -30
	declination_range_max = 70
	segments_of_ruler = np.arange(declination_range_min, declination_range_max+1, 10)
	print("\nsegments of declination to use: {0}".format(segments_of_ruler))

	n_index = []
	for i in segments_of_ruler:
		n_index.append((int)((90 - i)/10))
	print("Number segments: {0}".format(n_index))

	total_ruler_ratio_length = 0
	for n in n_index:
		n -= 1
		total_ruler_ratio_length += rulerSegments[(int)(n)]
	print("Total length of ruler with r = 1: {0}".format(total_ruler_ratio_length))
	print("Length of ruler to compare to = {0}".format(length_of_the_ruler_to_be_used))

	ratio_of_ruler = length_of_the_ruler_to_be_used / total_ruler_ratio_length
	print("Ratio of ruler: {0}".format(ratio_of_ruler))
	ruler_position_for_n = 0
	for segment_n in reversed(n_index):
		ruler_position_for_n += rulerSegments[segment_n-1]*ratio_of_ruler
		print("segments: {0} = {1} = {2:.4f}*{3:.4f} = {4:.4f} cm".format(segment_n,
																		convertSegmentToDegree(segment_n),
																		rulerSegments[segment_n-1],
																		ratio_of_ruler,
																		ruler_position_for_n))

if __name__ == '__main__':
	# Generate and plot
	graphPlotsegments = True # should plot the segments on a graph
	rulerLengthSegments(graphPlotsegments)
