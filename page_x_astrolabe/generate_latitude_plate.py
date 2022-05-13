# Generate a declination ruler for astrolabe star chart
# python3 generate_latitude_plate.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import math
import generate_declination_ruler as declination_script # import declination script to retrieve declination values

def calculateLatitudeCirclePosition(latitude_in_degrees, degree_at_90, left_right_list, radius_plate):
	# Calculate the size and position of the latitude line/plate
	# position of center (offset)
	left_position = left_right_list[0]
	right_position = left_right_list[1]
	print("Degree: {0} at {1} and {2}".format(latitude_in_degrees, left_position, right_position))

	def lengthSegment(angle):
		#print(angle)
		angle_in_radians = np.deg2rad(45 - angle/2)
		equation_of_length = radius_plate * math.tan(angle_in_radians) # calculated
		return equation_of_length

	left_segment = lengthSegment(left_position)
	right_segment = lengthSegment(right_position)
	center_point = lengthSegment(degree_at_90) # position of the zenith
	radius_position = (abs(right_segment) + abs(left_segment)) / 2
	radius_length = radius_position - center_point
	#print("Left Length = {0:.2f}, Right Length = {1:.2f}, Center point = {2:.2f}".format(left_segment, right_segment, center_point))
	#print("Radius = {0}".format(radius_length))

	if latitude_in_degrees == 90:
		radius_length = 0

	radius = radius_length
	offset = center_point
	return radius, offset


def plotLatitudePlate(actual_observation_latitude, ruler_length, almucanter_degree_position_dict, northOrSouth, displayAxis):
	# Plot latitude plate
	fig = plt.figure(figsize=(12,12), dpi=100)
	ax = fig.subplots()

	radius_of_plate = ruler_length / 2

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

	def plotCircles(radius_pos, label_name, radius_offset, label_color, outer_radius):
		# plot 360 degrees circle
		declination_position.append(round(radius_pos, 4))
		declination_labels.append(label_name)
		declination_offset.append(radius_offset)
		ax.axis("equal")
		circle = plt.Circle(xy=(radius_offset,0), radius=radius_pos, fill=False, color=label_color)
		ax.add_patch(circle)

	# Draw circle/curve for: Tropic of Cancer, Equator, Tropic of Capricon
	tropics_labels = ["Tropic of Capricorn", "Equator", "Tropic of Cancer"]
	tropics_positions = [capricorn_radius, equator_radius, cancer_radius]
	for i, pos in enumerate(tropics_positions):
		plotCircles(pos, tropics_labels[i], 0, "Black", radius_of_plate)

	# Draw circle/curve for almucanter lines
	for latitude_in_degree, left_right_position in almucanter_degree_position_dict.items():
		#print(latitude_in_degree)
		#print(left_right_position)
		degree_position_at_90 = almucanter_degree_position_dict[90][0]
		latitude_radius, latitude_center = calculateLatitudeCirclePosition(latitude_in_degree, degree_position_at_90, left_right_position, radius_of_plate)
		if northOrSouth == "North":
			if latitude_in_degree != 0:
				plotCircles(latitude_radius, str(latitude_in_degree), latitude_center, "gold", radius_of_plate)
			else:
				plotCircles(latitude_radius, "Horizon", latitude_center, "blueviolet", radius_of_plate)
		if northOrSouth == "South":
			# flip latitude center to negative
			if latitude_in_degree != 0:
				plotCircles(latitude_radius, str(latitude_in_degree), -latitude_center, "gold", radius_of_plate)
			else:
				plotCircles(latitude_radius, "Horizon", -latitude_center, "blueviolet", radius_of_plate)

	# Display circle labels
	print(declination_position)
	print(declination_labels)
	print(declination_offset)
	if displayAxis:
		for i, txt in enumerate(declination_labels):
			ax.annotate(txt, xy=(declination_offset[i], declination_position[i]), fontsize=8)
		plt.axis('on')
	else:
		plt.axis('off')

	import matplotlib.patches as patches
	mask = patches.Circle((9,9),radius=7)
	ax.set_clip_path(mask)
	#ax.add_patch(mask)


	plt.title("{0}ern Latitude {1}".format(northOrSouth, actual_observation_latitude))
	plt.xlim([-radius_of_plate-1, radius_of_plate+1]) # limit range to within the tropics
	plt.ylim([-radius_of_plate-1, radius_of_plate+1]) # limit range to within the tropics
	#print("limit = {0}".format(radius_of_plate))

	plt.show()
	fig.savefig('latitude_plate.png', dpi=fig.dpi)

def calculateAlmucanters(observation_latitude, northOrSouth):
	# calculate the degree positions for almucanters
	almucanter_position_dict = {} # degree = [left, right]
	almucanter_position_dict[90] = [observation_latitude, observation_latitude] # zenith

	almucanter_degree_positions = np.arange(0, 81, 10) # in degrees (0-80)

	for degree in almucanter_degree_positions:
		# For Northern Hemisphere
		if northOrSouth == "North":
			left_degree_position = (observation_latitude + 90) - degree # calculate the left-most degree
			right_degree_positions = (observation_latitude - 90) + degree # calculate the right-most degree
			almucanter_position_dict[degree] = [left_degree_position, right_degree_positions]
		if northOrSouth == "South":
			left_degree_position = (observation_latitude - 90) + degree # calculate the left-most degree
			right_degree_positions = (observation_latitude + 90) - degree # calculate the right-most degree
			almucanter_position_dict[degree] = [left_degree_position, right_degree_positions]

	#print("Latitude {0}: {1}\n{2}".format(observation_latitude, northOrSouth, almucanter_position_dict))
	return almucanter_position_dict

if __name__ == '__main__':
	# Chart Options
	displayAxis= True # display chart with axis (False/True)
	total_ruler_length = 30 # units (cut in half for each side of the ruler) (currently has to be even)
	actual_observation_latitude = 40 # TODO: breaks 90

	if actual_observation_latitude >= 0:  # TODO: single line if/else
		northOrSouth = "North" 
		observation_latitude = 90 - actual_observation_latitude # TODO: fix equation to worko for a latiude relative to 180 instead
	else: 
		northOrSouth = "South" # TODO: fix southern values
		observation_latitude = 90 + actual_observation_latitude # TODO: fix equation to worko for a latiude relative to 180 instead

	almucanter_degree_position_dict =  calculateAlmucanters(observation_latitude, northOrSouth)
	plotLatitudePlate(actual_observation_latitude, total_ruler_length, almucanter_degree_position_dict, northOrSouth, displayAxis)
