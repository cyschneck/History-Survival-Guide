# Generate a star chart for astrolabe
# python3 generate_star_chart.py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import generate_declination_ruler as declination_script # import declination script to retrieve declination values

# Declination ranges for North, South, Both (full)
northern_declination_min = -30
northern_declination_max = 70
southern_declination_min = -70
southern_declination_max = 30
full_declination_min = -80 # -90 = 0 length
full_declination_max = 80 # 90 = Large enough value that makes ratio = 0

def convertRAhrtoRadians(star_list):
	# change first element in the list object [RA, dec]
	for star in star_list:
		ra_in_hr = star[1]
		# convert RA from hours to degrees
		ra_hr, ra_min, ra_sec = list(map(int, ra_in_hr.split('.')))
		ra_min /= 60
		ra_sec /= 3600
		ra_total = ra_hr + ra_min + ra_sec
		ra_in_degrees = ra_total * 15

		# convert RA from degrees to radians
		ra_in_radians = np.deg2rad(ra_in_degrees)
		star[1] = ra_in_radians
	return star_list

def plotCircluar(star_list, northOrSouth, displayStarNamesLabels, displayDeclinationNumbers, total_ruler_length):
	# plot star chart as a circular graph
	#fig = plt.figure(figsize=(12,12), dpi=100)
	fig = plt.figure(figsize=(10,10), dpi=100)
	ax = fig.subplots(subplot_kw={'projection': 'polar'})

	# Set Right Ascension (astronomical 'longitude') as X
	angles_ra = np.array([330, 345, 0, 15, 30, 45, 60, 75, 90, 105, 120,
						135, 150,  165, 180, 195, 210, 225, 240, 255,
						270, 285, 300, 315])
	plt.xticks(angles_ra * np.pi / 180, fontsize=8)
	ax.set_xticklabels(['$22^h$','$23^h$','$0^h$','$1^h$','$2^h$','$3^h$',
						'$4^h$','$5^h$','$6^h$','$7^h$', '$8^h$','$9^h$',
						'$10^h$','$11^h$','$12^h$','$13^h$','$14^h$','$15^h$',
						'$16^h$','$17^h$','$18^h$','$19^h$','$20^h$',
						'$21^h$'], fontsize=10)

	# Set Declination (astronomical 'latitude') as Y

	# Split up chart into North/South hemisphere
	if northOrSouth == "Both":
		declination_values = np.arange(full_declination_min, full_declination_max+1, 10) # +1 to show max value in range
		min_dec_value = full_declination_min
		max_dec_value = full_declination_max
	if northOrSouth == "North":
		declination_values = np.arange(northern_declination_min, northern_declination_max+1, 10) # +1 to show max value in range
		min_dec_value = northern_declination_min
		max_dec_value = northern_declination_max
	if northOrSouth == "South":
		declination_values = np.arange(southern_declination_min, southern_declination_max+1, 10) # +1 to show max value in range
		min_dec_value = southern_declination_min
		max_dec_value = southern_declination_max

	# conversion length of a ruler for -90 to 90
	print(min_dec_value)
	print(max_dec_value)
	full_ruler_length_180 = (180 * (total_ruler_length/2)) / (abs(min_dec_value) + abs(max_dec_value))
	print("Length of full ratio ruler from {0} (1/2 {1}) = {2}".format(total_ruler_length, total_ruler_length/2, full_ruler_length_180))

	ruler_position_dict = declination_script.triggerDeclinationCalculations(full_ruler_length_180,
																			min_dec_value, max_dec_value)
	ruler_ratio = ruler_position_dict.pop("RATIO") # remove ratio value and store

	# add values to get the distance for ruler in max-min range
	degree_ruler_for_min_max_range_dict = {} # dictionary for degrees in max/min range and their lengths
	ruler_position_for_n_total = 0

	# create a ruler for the range used instead of the full range
	from collections import OrderedDict
	ordered_dict_declination = OrderedDict(reversed(sorted(ruler_position_dict.items(), key=lambda x:x[0])))
	for n_angle, ruler_length in ordered_dict_declination.items(): # add values from the largest to the smallest to account for declination lines
		# convert to be within range of ruler/2
		ruler_position_for_n_total += ruler_length # add lengths as iterating
		percent_of_total = ruler_position_for_n_total / sum(ordered_dict_declination.values()) # find percentage of full length
		ruler_position = percent_of_total * total_ruler_length/2 # convert to fit on the ruler of x length
		print("Degree {0} = {1} = {2:.4f}% =  {3:4f} [saved]".format(n_angle, 
													ruler_length,
													percent_of_total,
													ruler_position))
		degree_ruler_for_min_max_range_dict[n_angle] = round(ruler_position, 4)

	# display declination lines on the chart from -min to +max
	def displayDeclinationMarksOnAxis(declination_values, dec_min, dec_max):
		# set declination marks based on the ruler to space out lines
		ruler_declination_position = list(degree_ruler_for_min_max_range_dict.values())
		ruler_declination_labels = list(degree_ruler_for_min_max_range_dict.keys())
		both_label_values = [list(x) for x in zip(ruler_declination_position, ruler_declination_labels)]
		ax.set_ylim(0, max(ruler_declination_position))
		if displayDeclinationNumbers: # display axis
			plt.yticks(ruler_declination_position, fontsize=7)
			ax.set_yticklabels(both_label_values)
			ax.set_rlabel_position(270)
		else:
			plt.yticks(ruler_declination_labels, fontsize=0) # do not display axis

	# Display declination lines based on hemisphere
	if northOrSouth == "Both":
		displayDeclinationMarksOnAxis(declination_values, full_declination_min, full_declination_max)
	if northOrSouth == "North":
		displayDeclinationMarksOnAxis(declination_values, northern_declination_min, northern_declination_max)
	if northOrSouth == "South":
		displayDeclinationMarksOnAxis(declination_values, southern_declination_min, southern_declination_max)

	print("\n{0} to {1}".format(min_dec_value, max_dec_value))
	# convert to x and y values for stars
	x_star_labels = []
	x_ra_values = []
	y_dec_values = []
	for star in star_list:
		x_star_labels.append(star[0])
		x_ra_values.append(star[1])

		ruler_position = star[2]
		#if star[2] <= max_dec_value and star[2] >= min_dec_value: # within range of declination being displayed
		#	if star[2] > 0:
		#		nearest_five = star[2] - (star[2]%5) # round to the nearest length to round (55.56 to 55)
		#	else:
		#		nearest_five = star[2]  - (star[2]%5) + 5 # round to nearest length to round when negatigve (-15 instead of -20)
		#	length_at_nearest_five = degree_ruler_for_min_max_range_dict[nearest_five]
		#	declination_length_of_angle = declination_script.calculateLength(star[2])*ruler_ratio
		#	ruler_position = length_at_nearest_five + declination_length_of_angle
		#	print("{0}: {1} = {2:4f}({3}) + {4:4f} = {5:4f}".format(star[0], star[2], 
		#														length_at_nearest_five, nearest_five, 
		#														declination_length_of_angle, ruler_position))
		#else:
		#	ruler_position = -1
		#print("{0} : {1} = {2} = {3}".format(star[0], star[2], position_on_full_length_ruler, ruler_position))

		y_dec_values.append(ruler_position)
	ax.scatter(x_ra_values, y_dec_values, s=10)

	# label stars (optional)
	if displayStarNamesLabels:
		for i, txt in enumerate(x_star_labels):
			ax.annotate(txt, (x_ra_values[i], y_dec_values[i]), 
						horizontalalignment='center', verticalalignment='bottom', 
						fontsize=8)

	plt.show()
	fig.savefig('star_chart.png', dpi=fig.dpi)

if __name__ == '__main__':
	# stars to be included: 'name', ra HH.MM.SS, declination DD.SS
	# Northern stars (+ declination)
	alioth_star = ["Alioth", "12.54.01", 55.57]
	alkaid_star = ["Alkaid", "13.47.32", 49.18]
	alpheratz_star = ["Alpheratz", "00.08.23", 29.05]
	altair_star = ["Altair", "19.50.46", 8.52]
	arcturus_star = ["Arcturus", "14.15.39", 19.10]
	bellatrix_star = ["Bellatrix", "05.25.07", 6.20]
	betelgeuse_star = ["Betelgeuse", "05.55.10", 7.24]
	castor_star = ["Castor", "07.34.35", 31.53]
	dubhe_star = ["Dubhe", "11.03.43", 61.45]
	hamal_star = ["Hamal", "02.07.10", 23.27]
	megrez_star = ["Megrez", "12.15.25", 57.01]
	merak_star = ["Merak", "11.01.50", 56.22]
	mizar_star = ["Mizar", "13.23.55", 54.55]
	polaris_star = ["Polaris", "02.31.49", 89.15]
	pollux_star = ["Pollux", "07.45.18", 28.01]
	phecda_star = ["Phecda", "11.53.49", 53.41]
	procyon_star = ["Procyon", "07.39.18", 5.13]
	schedar_star = ["Schedar", "00.04.30", 56.32]
	spica_star = ["Spica", "13.25.11", -11.09]
	vega_star = ["Vega", "18.36.56", 38.47]
	#Southern stars (- declination)
	achernar_star = ["Achernar", "01.37.42", -57.14]
	ankaa_star = ["Ankaa", "00.26.17", -42.18]
	beta_hydri_star = ["Beta Hydri", "00.25.45", -77.15]
	diphda_star = ["Diphda", "00.43.35", -17.59]
	gamma_phoenics_star = ["Gamma Phoenics", "01.28.21", -43.19]
	mimosa_star = ["Mimosa", "12.47.43", -59.41]
	rigel_star = ["Rigel", "05.14.32", -8.12]
	sirus_star = ["Sirus", "06.45.08", -16.42]
	theta_eridani_star = ["Theta Eridani", "02.58.15", -40.18]

	# add stars to total star list
	northern_star_chart_list = [alioth_star,
								alkaid_star,
								alpheratz_star,
								altair_star,
								arcturus_star,
								bellatrix_star,
								betelgeuse_star,
								castor_star,
								dubhe_star,
								hamal_star,
								megrez_star,
								merak_star,
								mizar_star,
								polaris_star,
								pollux_star,
								phecda_star,
								procyon_star,
								schedar_star,
								spica_star,
								vega_star
								]

	southern_star_chart_list = [achernar_star,
								ankaa_star,
								beta_hydri_star,
								diphda_star,
								gamma_phoenics_star,
								mimosa_star,
								rigel_star,
								sirus_star,
								theta_eridani_star
								]

	star_chart_list = northern_star_chart_list + southern_star_chart_list

	# Convert Star chart from RA hours to Radians to chart
	star_chart_list = convertRAhrtoRadians(star_chart_list)

	# Chart options
	displayStarNames = True # display chart with star names (False/True)
	displayDeclinationNumbers = True # display declination marks (False/True)
	northOrSouth = "North" # options: "North", "South", "Both" (changes the declination range)
	total_ruler_length = 30 # units (cut in half for each side of the ruler) (currently has to be even)

	# Calculate declination values
	if northOrSouth == "North":
		declination_min = northern_declination_min
		declination_max = northern_declination_max
	if northOrSouth == "South":
		declination_min = southern_declination_min
		declination_max = southern_declination_max
	if northOrSouth == "Both":
		declination_min = full_declination_min
		declination_max = full_declination_max

	# Plot star chart on a circular polar coordinate system
	plotCircluar(star_chart_list,
				northOrSouth,
				displayStarNames,
				displayDeclinationNumbers,
				total_ruler_length)
