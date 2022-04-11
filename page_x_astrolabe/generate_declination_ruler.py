# Generate a star chart for astrolabe
# python3 generate_declination_ruler.py
import numpy as np
import matplotlib.pyplot as plt
import math

def convertSegementToDegree(segement_n):
	# convert segement (n) to a degree value
	angle_of_inclination = 90 - (segement_n*10)
	return angle_of_inclination

def rulerLengthSegements(graphPlotSegements):
	# define the length of each segement in ruler when radius = 1
	x_degreeSegements = np.arange(1,18,1)
	y_lengthSegements = []

	# convert segements into length segements
	for segement_in_circle in x_degreeSegements:
		angle_of_inclination = convertSegementToDegree(segement_in_circle)

		segement_in_radians = (segement_in_circle * np.pi / 180)
		equation_of_length = math.tan(5*segement_in_radians) # previous
		#equation_of_length = math.tan((angle_of_inclination))/2 # temp

		print("Segement: {0} = {1} = {2:.4f}".format(segement_in_circle, angle_of_inclination, equation_of_length))
		y_lengthSegements.append(equation_of_length)

	# optional graph of segements
	if graphPlotSegements:
		plotLengthSegements(x_degreeSegements, y_lengthSegements)

	# calculate the ruler
	calculateRuler(y_lengthSegements, equation_of_length)

def plotLengthSegements(x_degreeSegements, y_lengthSegements):
	# plot Segements (n) vs. Length of Segements
	plt.xticks(x_degreeSegements)
	plt.title("Length of Declination Ruler Segements: EQUATION")
	plt.xlabel("Degree Segements")
	plt.ylabel("Length of Segement when r = 1")
	plt.scatter(x_degreeSegements, y_lengthSegements)
	plt.show()

def calculateRuler(rulerSegements, equation_of_length):
	# Calculate the ruler based on a ruler length and the range of the declinations
	length_of_the_ruler_to_be_used = 15 # cm

	declination_range_min = -30
	declination_range_max = 70
	segements_of_ruler = np.arange(declination_range_min, declination_range_max+1, 10)
	print("\nSegements of declination to use: {0}".format(segements_of_ruler))

	n_index = []
	for i in segements_of_ruler:
		n_index.append((int)((90 - i)/10))
	print("Number segements: {0}".format(n_index))

	total_ruler_ratio_length = 0
	for n in n_index:
		n -= 1
		total_ruler_ratio_length += rulerSegements[(int)(n)]
	print("Length of ruler with r = 1: {0}".format(total_ruler_ratio_length))
	print("Length of ruler to compare to = {0}".format(length_of_the_ruler_to_be_used))

	ratio_of_ruler = length_of_the_ruler_to_be_used / total_ruler_ratio_length
	print("Ratio of ruler: {0}".format(ratio_of_ruler))
	ruler_position_for_n = 0
	for segement_n in reversed(n_index):
		ruler_position_for_n += rulerSegements[segement_n-1]*ratio_of_ruler
		print("Segements: {0} = {1} = {2:.4f}*{3:.4f} = {4:.4f} cm".format(segement_n,
																		convertSegementToDegree(segement_n),
																		rulerSegements[segement_n-1],
																		ratio_of_ruler,
																		ruler_position_for_n))

if __name__ == '__main__':
	# Generate and plot
	graphPlotSegements = False # should plot the segements on a graph
	rulerLengthSegements(graphPlotSegements)
