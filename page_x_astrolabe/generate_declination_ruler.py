# Generate a star chart for astrolabe
# python3 generate_declination_ruler.py
import numpy as np
import matplotlib.pyplot as plt

def rulerLengthSegements():
	# define the length of each segement in ruler when r = 1
	import math
	x_degreeSegements = np.arange(1,18,1)
	y_lengthSegements = []
	
	for segement in x_degreeSegements:
		segement_in_radains = (segement * np.pi / 180)
		print(math.tan(5*segement_in_radains))
		y_lengthSegements.append(math.tan(5*segement_in_radains))

	plt.xticks(x_degreeSegements)
	plt.title("Length of Declination Ruler Segements: tan(5n)")
	plt.xlabel("Degree Segements")
	plt.ylabel("Length of Segement when r = 1")
	plt.scatter(x_degreeSegements, y_lengthSegements)
	#plt.show()
	calculateRuler(y_lengthSegements)

def calculateRuler(rulerSegements):
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
	rulerLengthSegements()
