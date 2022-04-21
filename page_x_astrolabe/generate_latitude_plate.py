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

	declination_position = []
	declination_labels = []

	ax.set_ylim(0, radius_of_plate) # limit range to within the tropics

	def plotCircles(radius_pos, label_name, label_color):
		# plot 360 degrees circle
		declination_labels.append(label_name)
		declination_position.append(radius_pos)
		for curve in [[[0, 360], [radius_pos, radius_pos]]]: # draw a circle in 360 degrees
			curve[0] = np.deg2rad(curve[0])
			x = np.linspace(curve[0][0], curve[0][1], num=360)
			y = interp1d(curve[0], curve[1])(x)
			ax.plot(x, y, color=label_color)

	# Draw circle/curve for: Tropic of Cancer, Equator, Tropic of Capricon
	tropics_labels = ["Tropic of Capricorn", "Equator", "Tropic of Cancer"]
	tropics_positions = [capricorn_radius, equator_radius, cancer_radius]
	for i, pos in enumerate(tropics_positions):
		plotCircles(pos, tropics_labels[i], "Black")
	
	# Draw circle/curve for: Horizon
	horizon_position = 8
	declination_labels.append("Horizon")
	declination_position.append(horizon_position)
	plotCircles(horizon_position, "Horizon", "Blue")
	
	# Draw circle/curve for: Declination latitude angles
	##TODO

	# Display circle labels
	if displayDeclination:
		plt.yticks(declination_position, fontsize=7)
		ax.set_yticklabels(declination_labels, horizontalalignment="left", verticalalignment="bottom")
	else:
		plt.yticks(declination_position, fontsize=0) # do not display

	plt.show()
	fig.savefig('latitude_plate.png', dpi=fig.dpi)

if __name__ == '__main__':
	# Chart Options
	northOrSouth = "North" # options: "North", "South"
	displayDeclination = True # display chart with RA (False/True)
	total_ruler_length = 30 # units (cut in half for each side of the ruler) (currently has to be even)

	plotLatitudePlate(total_ruler_length, northOrSouth, displayDeclination)
