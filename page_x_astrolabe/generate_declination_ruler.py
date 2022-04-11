# Generate a star chart for astrolabe
# python3 generate_declination_ruler.py
import numpy as np
import matplotlib.pyplot as plt
import math

def rulerLengthSegements(graphPlotSegements):
	# define the length of each segement in ruler when radius = 1
	x_degreeSegements = np.arange(1,18,1)
	y_lengthSegements = []

	# convert segements into length segements
	for segement_in_circle in x_degreeSegements:
		angle_of_inclination = 90 - (segement_in_circle*10)

		segement_in_radians = (segement_in_circle * np.pi / 180)
		equation_of_length = math.tan(5*segement_in_radians) # previous
		#equation_of_length = math.tan((angle_of_inclination))/2 # temp

		print("Segement: {0} = {1} = {2}".format(segement_in_circle, angle_of_inclination, equation_of_length))
		y_lengthSegements.append(equation_of_length)

	# optional graph of segements
	if graphPlotSegements:
		plotLengthSegements(x_degreeSegements, y_lengthSegements)

	# calculate the ruler
	#calculateRuler(y_lengthSegements)

def plotLengthSegements(x_degreeSegements, y_lengthSegements):
	# plot Segements (n) vs. Length of Segements
	plt.xticks(x_degreeSegements)
	plt.title("Length of Declination Ruler Segements: EQUATION")
	plt.xlabel("Degree Segements")
	plt.ylabel("Length of Segement when r = 1")
	plt.scatter(x_degreeSegements, y_lengthSegements)
	plt.show()

def calculateRuler(rulerSegements):
	# Calculate the ruler based on a ruler length and the range of the declinations
	ruler_length = 15
	declination_range_min = -30
	declination_range_max = 70
	segements_of_ruler = np.arange(declination_range_min, declination_range_max+1, 10)
	print(segements_of_ruler)
	n_index = []
	for i in segements_of_ruler:
		n_index.append((90 - i)/10)
	print(n_index)

	total_ruler_length = 0
	for n in n_index:
		n -= 1
		total_ruler_length += rulerSegements[(int)(n)]
		#print(rulerSegements[(int)(n)])
	print(total_ruler_length)
	existing_ruler = 15 # cm
	ratio_x = existing_ruler / total_ruler_length
	print(ratio_x)

if __name__ == '__main__':
	# Generate and plot
	graphPlotSegements = True # should plot the segements on a graph
	rulerLengthSegements(graphPlotSegements)
