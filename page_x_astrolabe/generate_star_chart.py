# Generate a star chart for astrolabe
# python3 generate_star_chart.py
import math
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

def plotCircluar(star_list, northOrSouth, year_date_YYYY, displayStarNamesLabels, displayDeclinationNumbers, total_ruler_length, increment_by):
	# plot star chart as a circular graph
	fig = plt.figure(figsize=(12,12), dpi=100)
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
	if northOrSouth == "Full":
		declination_values = np.arange(full_declination_min, full_declination_max+1, increment_by) # +1 to show max value in range
		min_dec_value = full_declination_min
		max_dec_value = full_declination_max
	if northOrSouth == "North":
		declination_values = np.arange(northern_declination_min, northern_declination_max+1, increment_by) # +1 to show max value in range
		min_dec_value = northern_declination_min
		max_dec_value = northern_declination_max
	if northOrSouth == "South":
		declination_values = np.arange(southern_declination_min, southern_declination_max+1, increment_by) # +1 to show max value in range
		min_dec_value = southern_declination_min
		max_dec_value = southern_declination_max

	# Store the ruler positions based on degrees and the ratio of the ruler
	ruler_position_dict = declination_script.triggerDeclinationCalculations(total_ruler_length,
																			min_dec_value, max_dec_value, increment_by)

	# display declination lines on the chart from -min to +max
	def displayDeclinationMarksOnAxis(declination_values, dec_min, dec_max):
		# set declination marks based on the ruler to space out lines
		ruler_declination_position = list(ruler_position_dict.values())
		ruler_declination_labels = list(ruler_position_dict.keys())
		#both_label_values = [list(x) for x in zip(ruler_declination_position, ruler_declination_labels)] # for testing
		ax.set_ylim(0, max(ruler_declination_position))
		if displayDeclinationNumbers: # display axis
			plt.yticks(ruler_declination_position, fontsize=7)
			ax.set_yticklabels(ruler_declination_labels)
			ax.set_rlabel_position(120)
		else:
			plt.yticks(ruler_declination_position, fontsize=0) # do not display axis
			ax.set_yticklabels(ruler_declination_labels)
			ax.set_rlabel_position(120)

	# Display declination lines based on hemisphere
	if northOrSouth == "Full":
		displayDeclinationMarksOnAxis(declination_values, full_declination_min, full_declination_max)
	if northOrSouth == "North":
		displayDeclinationMarksOnAxis(declination_values, northern_declination_min, northern_declination_max)
	if northOrSouth == "South":
		displayDeclinationMarksOnAxis(declination_values, southern_declination_min, southern_declination_max)

	# Calculate the RA and Declination of a star based on changes due to Proper Motion
	def calculateRAandDeclinationViaProperMotion(year_date_YYYY, star_ra, star_dec, star_pm_speed, star_pm_angle):
		# returns calculated RA and Declination
		current_year = 2022
		time_since_current_year = year_date_YYYY - current_year # postive = future, negative = past
		print("Date {0}, RA = {1}, Dec = {2}, PM Speed = {3}, PM Angle = {4}".format(year_date_YYYY,
																					star_ra,
																					star_dec,
																					star_pm_speed,
																					star_pm_angle))

		star_pm_speed_degrees = 0.00000027777776630942 * star_pm_speed # convert mas to degrees
		star_movement_speed_vector = star_pm_speed_degrees * time_since_current_year
		print("Years: {0}, with speed of {1} degree and angle of {2} = {3}".format(time_since_current_year,
																			star_pm_speed_degrees, star_pm_angle,
																			star_movement_speed_vector))
		ra_x_difference_component = star_movement_speed_vector * math.sin(np.deg2rad(star_pm_angle))
		dec_y_difference_component = star_movement_speed_vector * math.cos(np.deg2rad(star_pm_angle))
		print("(RA) x = {0}".format(ra_x_difference_component))
		print("(DEC) y = {0}\n".format(dec_y_difference_component))

		star_adjusted_ra = star_ra #TODO: + ra_x_difference_component
		star_adjusted_declination = star_dec #TODO: + dec_y_difference_component

		return star_adjusted_ra, star_adjusted_declination

	print("\nRange of Declination: {0} to {1}".format(min_dec_value, max_dec_value))
	radius_of_circle = declination_script.calculateRadiusOfCircle(declination_min, total_ruler_length)
	# convert to x and y values for stars
	x_star_labels = []
	x_ra_values = []
	y_dec_values = []
	for star in star_list:
		ruler_position = declination_script.calculateLength(star[2], radius_of_circle) # convert degree to position on radius
		print("{0}: {1} = {2:.4f}".format(star[0], star[2], ruler_position))
		if star[2] > min_dec_value and star[2] < max_dec_value: # only display stars within range of declination values
			x_star_labels.append(star[0])
			star_ra, star_declination = calculateRAandDeclinationViaProperMotion(year_date_YYYY, 
																				star[1], 
																				ruler_position, 
																				star[3], 
																				star[4])
			x_ra_values.append(star_ra)
			y_dec_values.append(star_declination)
			#x_ra_values.append(star[1])
			#y_dec_values.append(ruler_position)
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
	# stars: ["name", "RA: HH.MM.SS", DD.SS, Proper Motion Speed (mas/yr), Proper motion pos angle (DD.SS)]
	# Northern stars (+ declination)
	aldebaran_star = ["Aldebaran", "04.35.55", 16.30, 199.3, 161.4]
	algol_star = ["Algol", "03.08.10", 40.57, 3.4, 119.0]
	alioth_star = ["Alioth", "12.54.01", 55.57, 112.2, 94.2]
	alkaid_star = ["Alkaid", "13.47.32", 49.18, 122.1, 263.0]
	alphecca_star = ["Alphecca", "15.34.41", 26.42, 147.8, 126.4]
	alpheratz_star = ["Alpheratz", "00.08.23", 29.05, 213.6, 139.9]
	altair_star = ["Altair", "19.50.46", 8.52, 660.3, 54.3]
	arcturus_star = ["Arcturus", "14.15.39", 19.10, 2279.4, 208.7]
	bellatrix_star = ["Bellatrix", "05.25.07", 6.20, 15.2, 212.2]
	betelgeuse_star = ["Betelgeuse", "05.55.10", 7.24, 29.8, 67.7]
	caph_star = ["Caph", "00.09.10", 59.08, 553.5, 109.0]
	capella_star = ["Capella", "05.16.41", 45.59, 433.5, 170.0]
	castor_star = ["Castor", "07.34.35", 31.53, 240.3, 232.8]
	deneb_star = ["Deneb", "20.41.25", 45.16, 2.7, 47.4]
	denebola_star = ["Denebola", "11.49.03", 14.34, 510.7, 257.0]
	dubhe_star = ["Dubhe", "11.03.43", 61.45, 138.5, 255.5]
	hamal_star = ["Hamal", "02.07.10", 23.27, 239.7, 128.1]
	megrez_star = ["Megrez", "12.15.25", 57.01, 104.3, 85.5]
	merak_star = ["Merak", "11.01.50", 56.22, 88.0, 67.6]
	mizar_star = ["Mizar", "13.23.55", 54.55, 124.6, 100.5]
	pleiades_celaeno_star = ["Celaeno", "03.44.48", 24.17, 49.2, 156.2]
	polaris_star = ["Polaris", "02.31.49", 89.15, 46.0, 104.9]
	pollux_star = ["Pollux", "07.45.18", 28.01, 628.2, 265.8]
	phecda_star = ["Phecda", "11.53.49", 53.41, 108.2, 84.2]
	procyon_star = ["Procyon", "07.39.18", 5.13, 1259.2, 214.6]
	rasalhague_star = ["Rasalhague", "17.34.56", 12.33, 246.5, 154.0]
	regulus_star = ["Regulus", "10.08.22", 11.58, 248.8, 271.3]
	schedar_star = ["Schedar", "00.04.30", 56.32, 58.4, 122.7]
	spica_star = ["Spica", "13.25.11", -11.09, 52.3, 234.1]
	vega_star = ["Vega", "18.36.56", 38.47, 349.7, 35.1]

	#Southern stars (- declination)
	achernar_star = ["Achernar", "01.37.42", -57.14, 95.0, 113.7]
	alphard_star = ["Alphard", "09.27.35", -8.39, 37.6, 336.1]
	ankaa_star = ["Ankaa", "00.26.17", -42.18, 425.7, 146.8]
	beta_hydri_star = ["Beta Hydri", "00.25.45", -77.15, 2242.9, 81.6]
	diphda_star = ["Diphda", "00.43.35", -17.59, 234.7, 82.2]
	gamma_phoenics_star = ["Gamma Phoenics", "01.28.21", -43.19, 207.6, 184.9]
	mimosa_star = ["Mimosa", "12.47.43", -59.41, 45.9, 249.4]
	rigel_star = ["Rigel", "05.14.32", -8.12, 1.4, 69.1]
	sadalmelik_star = ["Sadalmelik", "22.05.47", -0.19, 21.3, 119.3]
	sirius_star = ["Sirius", "06.45.08", -16.42, 1339.4, 204.1]
	theta_eridani_star = ["Acamar", "02.58.15", -40.18, 57.1, 293.8]
	zubeneschamali_star = ["Zubeneschamali", "15.17.00", -9.22, 100.0, 258.7]

	# add stars to total star list
	northern_star_chart_list = [aldebaran_star,
								algol_star,
								alioth_star,
								alkaid_star,
								alphecca_star,
								alpheratz_star,
								altair_star,
								arcturus_star,
								bellatrix_star,
								betelgeuse_star,
								caph_star,
								capella_star,
								castor_star,
								denebola_star,
								dubhe_star,
								hamal_star,
								megrez_star,
								merak_star,
								mizar_star,
								pleiades_celaeno_star,
								polaris_star,
								pollux_star,
								phecda_star,
								procyon_star,
								schedar_star,
								spica_star,
								vega_star
								]

	southern_star_chart_list = [achernar_star,
								alphard_star,
								ankaa_star,
								beta_hydri_star,
								diphda_star,
								gamma_phoenics_star,
								mimosa_star,
								rigel_star,
								sirius_star,
								theta_eridani_star,
								zubeneschamali_star
								]

	star_chart_list = northern_star_chart_list + southern_star_chart_list

	# Convert Star chart from RA hours to Radians to chart
	star_chart_list = convertRAhrtoRadians(star_chart_list)

	# Chart options
	displayStarNames = True # display chart with star names (False/True)
	displayDeclinationNumbers = True # display declination marks (False/True)
	northOrSouth = "North" # options: "North", "South", "Full" (changes the declination range)
	total_ruler_length = 30 # units (cut in half for each side of the ruler) (currently has to be even)
	increment_by = 5 # increment degrees by (1, 5, 10)
	year_of_plate_YYYY = 2024

	# Calculate declination values
	if northOrSouth == "North":
		declination_min = northern_declination_min
		declination_max = northern_declination_max
	if northOrSouth == "South":
		declination_min = southern_declination_min
		declination_max = southern_declination_max
	if northOrSouth == "Full":
		declination_min = full_declination_min
		declination_max = full_declination_max

	# Plot star chart on a circular polar coordinate system
	plotCircluar(star_chart_list,
				northOrSouth,
				year_of_plate_YYYY,
				displayStarNames,
				displayDeclinationNumbers,
				total_ruler_length,
				increment_by)
