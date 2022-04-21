# Generate a declination ruler for astrolabe star chart
# python3 generate_latitude_plate.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import math

def calculateLatitudeCirclePosition(latitude_in_degrees):
	radius = 10
	offset = 15
	return radius, offset

def plotLatitudePlate(ruler_length, northOrSouth, displayAxis):
	# Plot latitude plate
	fig = plt.figure(figsize=(12,12), dpi=100)
	ax = fig.subplots()

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
	declination_offset = []
	declination_labels = []

	#ax.set_ylim(0, radius_of_plate) # limit range to within the tropics
	#ax.set_xlim(-radius_of_plate, radius_of_plate+1) # limit range to within the tropics
	#ax.set_ylim(-radius_of_plate, radius_of_plate+1) # limit range to within the tropics
	#print("limit = {0}".format(radius_of_plate))

	def plotCircles(radius_pos, label_name, radius_offset, label_color, outer_radius):
		# plot 360 degrees circle
		declination_position.append(round(radius_pos, 4))
		declination_labels.append(label_name)
		declination_offset.append(radius_offset)
		ax.axis("equal")
		circle = plt.Circle(xy=(radius_offset,0), radius=radius_pos, fill=False, color=label_color)
		ax.add_patch(circle)

		#import matplotlib.patches as patches
		#mask = patches.Circle((8,8),radius=5)
		#circle.set_clip_path(mask)
		#ax.add_patch(mask)

	# Draw circle/curve for: Tropic of Cancer, Equator, Tropic of Capricon
	tropics_labels = ["Tropic of Capricorn", "Equator", "Tropic of Cancer"]
	tropics_positions = [capricorn_radius, equator_radius, cancer_radius]
	for i, pos in enumerate(tropics_positions):
		plotCircles(pos, tropics_labels[i], 0, "Black", radius_of_plate)
	
	# Draw circle/curve for: Horizon
	horizon_position = 0 # degrees
	horizon_radius, horizon_offset = calculateLatitudeCirclePosition(horizon_position)
	plotCircles(horizon_radius, "Horizon", horizon_offset, "Blue", radius_of_plate)
	
	# Draw circle/curve for: Declination latitude angles
	latitude_list = np.arange(-90, 90+1, 10) # in degrees
	#for latitude_in_degrees in latitude_list:
	#	plotCircles(latitude_in_degrees, str(latitude_in_degrees), 0, "Green")

	# Display circle labels
	print(declination_position)
	print(declination_labels)
	print(declination_offset)
	if displayAxis:
		for i, txt in enumerate(declination_labels):
			ax.annotate(txt, xy=(declination_offset[i], declination_position[i]), 
						horizontalalignment='center', verticalalignment='bottom', 
						fontsize=8)
		plt.axis('off')
	else:
		plt.axis('off')

	plt.show()
	fig.savefig('latitude_plate.png', dpi=fig.dpi)

if __name__ == '__main__':
	# Chart Options
	northOrSouth = "North" # options: "North", "South"
	displayAxis= True # display chart with axis (False/True)
	total_ruler_length = 30 # units (cut in half for each side of the ruler) (currently has to be even)

	plotLatitudePlate(total_ruler_length, northOrSouth, displayAxis)
