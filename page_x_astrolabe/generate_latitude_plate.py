# Generate a declination ruler for astrolabe star chart
# python3 generate_latitude_plate.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import math

def plotLatitudePlate(ruler_length, northOrSouth, displayDeclination):
	# Plot latitude plate
	fig = plt.figure(figsize=(12,12), dpi=100)
	ax = fig.subplots(subplot_kw={'projection': 'polar'})

	radius_of_plate = ruler_length / 2

	# Set Right Ascension (astronomical 'longitude') as X
	plt.xticks([])
	ax.set_xticklabels([], fontsize=0) # do not display RA

	# Set Declination (astronomical 'latitude') as Y
	tropic_of_capricorn = -23.5 # degrees
	tropic_of_cancer = 23.5 # degrees
	equator = 0.0 # degrees
	
	# Calculate radius for tropics and equator
	if northOrSouth == "North":
		capricorn_radius = radius_of_plate
		equator_radius = radius_of_plate / math.tan(np.deg2rad(45-(tropic_of_capricorn)/2))
		cancer_radius = equator_radius * math.tan(np.deg2rad(45-tropic_of_cancer/2))
	if northOrSouth == "South":
		cancer_radius = radius_of_plate
		equator_radius = radius_of_plate / math.tan(np.deg2rad(45-(tropic_of_capricorn)/2))
		capricorn_radius = equator_radius * math.tan(np.deg2rad(45-tropic_of_cancer/2))

	# Display Declination lines
	print("Tropic of Capricorn radius ({0}) = {1}".format(45-(tropic_of_capricorn)/2, capricorn_radius))
	print("Equator radius = {0:.4f}".format(equator_radius))
	print("Tropic of Cancer radius ({0}) = {1:.4f}".format(45-tropic_of_cancer/2, cancer_radius))
	declination_labels = ["Tropic of Capricorn", "Equator", "Tropic of Cancer"]
	declination_position = [capricorn_radius, equator_radius, cancer_radius]
	if displayDeclination:
		plt.yticks(declination_position, fontsize=7)
		ax.set_yticklabels(declination_labels, horizontalalignment="left", verticalalignment="bottom")
	else:
		plt.yticks(declination_position, fontsize=0) # do not display
	#ax.set_yticklabels(declination_position)

	# Draw circle/curve at specific position
	ax.set_ylim(0, radius_of_plate)
	for dec in declination_position:
		for curve in [[[0, 360], [dec, dec]]]: # draw a circle in 360 degrees
			curve[0] = np.deg2rad(curve[0])
			x = np.linspace(curve[0][0], curve[0][1], num=360)
			y = interp1d(curve[0], curve[1])(x)
			ax.plot(x, y, color="black")

	plt.show()
	fig.savefig('latitude_plate.png', dpi=fig.dpi)

if __name__ == '__main__':
	# Chart Options
	northOrSouth = "North" # options: "North", "South"
	displayDeclination = True # display chart with RA (False/True)
	total_ruler_length = 30 # units (cut in half for each side of the ruler) (currently has to be even)

	plotLatitudePlate(total_ruler_length, northOrSouth, displayDeclination)
