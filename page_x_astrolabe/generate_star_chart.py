# Generate a star chart for astrolabe
# python3 generate_star_chart.py
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import generate_declination_ruler as declination_script # import declination script to retrieve declination values

# Declination ranges for North and South
northern_declination_min = -30
northern_declination_max = 90
southern_declination_min = 30
southern_declination_max = -90

# Start Year (JP2000)
j2000 = 2000 # start year of the star catalogue (jan 1 2000 via IAU)

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

def calculateRAandDeclinationViaProperMotion(years_since_2000, star_ra, star_dec, star_pm_speed, star_pm_angle):
	# Calculate the RA and Declination of a star based on changes due to Proper Motion
	# returns calculated RA and Declination

	#print("Proper Motion for {0} Years".format(years_since_2000))
	#print("Date {0}, RA = {1}, Dec = {2}, PM Speed = {3}, PM Angle = {4}".format(years_since_2000, star_ra, star_dec, star_pm_speed, star_pm_angle))

	star_pm_speed_degrees = 0.00000027777776630942 * star_pm_speed # convert mas/yr to degrees/yr
	star_pm_speed_radains = np.deg2rad(star_pm_speed_degrees) # radains/yr
	star_movement_radains_per_year = star_pm_speed_radains * years_since_2000
	#print("Years: {0}, speed {1} (rad/yr) and angle of {2} ({3} radians)".format(time_since_current_year, star_pm_speed_radains, star_pm_angle, np.deg2rad(star_pm_angle)))
	#print("Movement Over Time = {0} (rad), {1} (deg)".format(star_movement_radains_per_year, np.rad2deg(star_movement_radains_per_year)))

	ra_x_difference_component = star_movement_radains_per_year * math.cos(np.deg2rad(star_pm_angle))
	dec_y_difference_component = star_movement_radains_per_year * math.sin(np.deg2rad(star_pm_angle))
	#print("(RA)  x Difference = {0} (rad) = {1} degrees".format(ra_x_difference_component, np.rad2deg(ra_x_difference_component)))
	#print("(DEC) y Difference = {0} (rad) = {1} degrees".format(dec_y_difference_component, np.rad2deg(dec_y_difference_component)))

	star_adjusted_ra = star_ra + ra_x_difference_component # in radians with proper motion (potentionally will be flipped 180 based on new declination)
	#star_ra = np.deg2rad(15) # original (TEST)
	#star_adjusted_ra = np.deg2rad(90) # new with proper motions (TEST)
	star_adjusted_declination = star_dec + np.rad2deg(dec_y_difference_component) # in degrees new with proper motion
	#star_dec = 30 # orignal (TEST)
	#star_adjusted_declination = -360 # new with proper motion (TEST)

	dec_x = star_adjusted_declination
	# remap within -90 and 90 for postive declinations
	if star_adjusted_declination > 0: # Postive declinations
		dec_x = star_adjusted_declination % 360
		# map from 0 to 90 (postive declinations)
		if dec_x > 90 and dec_x <= 180: 
			dec_x = 90 + (90 - dec_x)
		# map from 0 to -90 (negative declinations)
		if dec_x <= 270 and dec_x > 180:
			dec_x = 180 - dec_x
		if dec_x < 360 and dec_x > 270:
			dec_x = -90 + (dec_x - 270)
	if star_adjusted_declination < -0: # Negative declinations
		dec_x = star_adjusted_declination % -360
		# map from 0 to -90 (negative declinations)
		if dec_x < -90 and dec_x >= -180: 
			dec_x = -90 - (90 + dec_x)
		# map from 0 to 90 (postive declinations)
		if dec_x >= -270 and dec_x <= -180:
			dec_x = 180 + dec_x
			dec_x = abs(dec_x)
		if dec_x > -360 and dec_x < -270:
			dec_x = 90 + (dec_x + 270)
	#print("New mapped dec = {0}".format(dec_x))
	#print("Original Dec = {0}, New Dec = {1}".format(star_dec, star_adjusted_declination))

	# flip over RA by rotating 180
	is_flipped_across_pole = False
	star_over_ninety_ra = star_adjusted_declination
	if star_over_ninety_ra >= 0: # postive declinations
		while (star_over_ninety_ra > 90):
			star_over_ninety_ra -= 90
			is_flipped_across_pole = not is_flipped_across_pole # flip across the center by 180
	if star_over_ninety_ra < 0: # negative declinations
		while (star_over_ninety_ra < -90):
			star_over_ninety_ra += 90
			is_flipped_across_pole = not is_flipped_across_pole # flip across the center by 180
	#print("Original RA = {0}, New RA = {1}, Flipped = {2} (if true +180?)".format(np.rad2deg(star_ra), np.rad2deg(star_adjusted_ra), is_flipped_across_pole))

	# If declination goes over ninety, flip over by 180
	if is_flipped_across_pole:
		star_adjusted_ra = star_adjusted_ra + np.deg2rad(180)

	star_adjusted_declination = dec_x
	#print("Final RA: {0} degrees".format(np.rad2deg(star_adjusted_ra)))
	#print("Final Dec: {0} degrees ".format(star_adjusted_declination))
	return star_adjusted_ra, star_adjusted_declination

def calculateObliquity(year_to_calculate_YYYY):
	# Calculate the obliquity for a given year referenced to Jan 1 2000
	# Ranges between 22.1 to about 24.5 degrees

	# Find Obliquity in Julian Centuries (via "Expressions for IAU Precession Quantities": https://www.aanda.org/articles/aa/pdf/2003/48/aa4068.pdf)
	days_since_1_jan_2000 = (year_to_calculate_YYYY - j2000) / 36525 # assumes year to measure is jan 1 YYYY (Julian Century = 36525)
	obliquity_2000 = 84381.448 # arcseconds or 23.439167
	obliquity_YYYY = obliquity_2000 - (46.84024 * days_since_1_jan_2000) - (0.00059 * days_since_1_jan_2000**2) + (0.001813 * days_since_1_jan_2000**3)
	#print("Obliquity for {0} years ago/since = {1} arcseconds = {2} degrees".format(year_to_calculate_YYYY - 2022, obliquity_YYYY, obliquity_YYYY/3600))

	obliquity_YYYY_in_degrees = obliquity_YYYY/3600
	obliquity_YYYY_in_degrees = 23.439167 ### FOR TESTING: TO BE REMOVED
	return obliquity_YYYY_in_degrees

'''
def plotObliquity():
	# plot obliquity to view
	x_dates = []
	for date_since_2000 in range(0, 10700): # Last Max 10.7K years ago
		x_dates.append(2000 - date_since_2000)
	for date_since_2000 in range(1, 9800): # Next Min in 9.8K year to go
		x_dates.append(2000 + date_since_2000)
	print(min(x_dates))
	print(max(x_dates))

	y_obliquity_degrees = []
	for date_YYYY in x_dates:
		y_obliquity_degrees.append(calculateObliquity(date_YYYY))
	fig = plt.figure(figsize=(12,12), dpi=100)
	plt.title("Obliquity Cycle")
	plt.scatter(x_dates, y_obliquity_degrees)
	plt.show()
'''

def calculatePositionOfPolePrecession(years_since_2000, original_declination, original_ra):
	# Calculate change in the position of the pole due to precession
	obliquity_for_YYYY = calculateObliquity(years_since_2000) # currently 23.439167 for testing
	print("Years Since 2000 = {0}".format(years_since_2000))

	#plot_obliquity = True # option to plot obliquity for testing
	#if plot_obliquity: plotObliquity()

	# Rate of change of right ascension and declination of a star due to precession
	declination_change_arcseconds_per_year = (19.9 * math.cos(original_ra)) * years_since_2000
	ra_change_arcseconds_per_year = (46.1 + 19.9 * math.sin(original_ra) * math.tan(original_declination)) * years_since_2000

	change_in_declination = declination_change_arcseconds_per_year/3600 # degrees
	change_in_ra = np.deg2rad(ra_change_arcseconds_per_year/3600) # degrees to radians

	final_declination = original_declination + change_in_declination
	final_ra = original_ra + change_in_ra

	print("Dec: {0} + {1} = {2}".format(original_declination, change_in_declination, final_declination))
	print("RA:  {0} + {1} = {2}".format(original_ra, change_in_ra, final_ra))
	return final_ra, final_declination 

def plotCircluar(full_star_list, northOrSouth, magnitude_filter, year_since_2000, displayStarNamesLabels, displayDeclinationNumbers, total_ruler_length, increment_by):
	# plot star chart as a circular graph
	fig = plt.figure(figsize=(12,12), dpi=100)
	ax = fig.subplots(subplot_kw={'projection': 'polar'})

	# Filter Stars by Magnitude (only display stars of X brightness)
	star_list = []
	for star in full_star_list:
		if star[5] < magnitude_filter: # 0 is bright, 6 is dimmest (includes negatives for very bright)
			star_list.append(star)
		else:
			#print("Removed Star based on Magnitude Filter: {0} ({1} V)".format(star[0], star[5]))
			pass

	# Set Declination (astronomical 'latitude') as Y

	# Split up chart into North/South hemisphere
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
																			min_dec_value,
																			max_dec_value,
																			increment_by,
																			northOrSouth)

	# Display declination lines on the chart from -min to +max
	def displayDeclinationMarksOnAxis(declination_values, dec_min, dec_max, isInverted):
		# set declination marks based on the ruler to space out lines
		ruler_declination_position = list(ruler_position_dict.values())
		ruler_declination_labels = list(ruler_position_dict.keys())
		both_label_values = [list(x) for x in zip(ruler_declination_position, ruler_declination_labels)] # for testing
		ax.set_ylim(0, max(ruler_declination_position))

		# Display Axis
		if displayDeclinationNumbers:
			ruler_declination_labels = ["{0}°".format(deg) for deg in ruler_declination_labels]
			plt.yticks(ruler_declination_position, fontsize=7)
			ax.set_yticklabels(ruler_declination_labels)
			ax.set_rlabel_position(120) # declination labels position
		else:
			plt.yticks(ruler_declination_position, fontsize=0) # do not display axis
			ax.set_yticklabels(ruler_declination_labels)
			ax.set_rlabel_position(120) # declination labels position

	# Display declination lines based on hemisphere
	if northOrSouth == "North":
		displayDeclinationMarksOnAxis(declination_values, northern_declination_min, northern_declination_max, False)
	if northOrSouth == "South":
		displayDeclinationMarksOnAxis(declination_values, southern_declination_min, southern_declination_max, True)

	#print("\n{0}ern Range of Declination: {1} to {2}".format(northOrSouth, min_dec_value, max_dec_value))

	radius_of_circle = declination_script.calculateRadiusOfCircle(declination_min, total_ruler_length, northOrSouth)
	# convert to x and y values for stars
	x_star_labels = []
	x_ra_values = []
	y_dec_values = []
	for star in star_list:
		#print(star[0])
		# Calculate position of star due to PROPER MOTION
		star_ra, star_declination = calculateRAandDeclinationViaProperMotion(year_since_2000, 
																			star[1], 
																			star[2], 
																			star[3], 
																			star[4])
		#print("Adjusted: {0} RA (radians) = {1}".format(star[1], star_ra))
		#print("Adjusted via Proper Motion: '{0}': {1} Declination (degrees) = {2} ".format(star[0], star[2], star_declination))

		# Calculate new position of star due to PRECESSION
		precession_change_in_ra, precession_change_in_declination = calculatePositionOfPolePrecession(year_since_2000, star_declination, star_ra)

		dec_ruler_position = declination_script.calculateLength(star_declination, radius_of_circle, northOrSouth) # convert degree to position on radius

		#print("{0}: {1} declination = {2:.4f} cm".format(star[0], star_declination, ruler_position))
		in_range_value = False # Determine if within range of South/North Hemisphere
		if star_declination > min_dec_value and star_declination < max_dec_value: # only display stars within range of declination values
			in_range_value = True # North
		if star_declination < min_dec_value and star_declination > max_dec_value: # only display stars within range of declination values
			in_range_value = True # South

		if in_range_value:
			x_star_labels.append(star[0])
			x_ra_values.append(star_ra)
			y_dec_values.append(dec_ruler_position)
			#print("Original: '{0}': {1} RA (degrees) and {2} Declination (degrees)".format(star[0], np.rad2deg(star[1]), star[2]))

	# Set Right Ascension (astronomical 'longitude') as X
	angles_ra = np.array([0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150,
						165, 180, 195, 210, 225, 240, 255, 270, 285, 300,
						315, 330, 345])
	plt.xticks(angles_ra * np.pi / 180, fontsize=8)
	labels_ra = np.array(['$0^h$','$1^h$','$2^h$','$3^h$', '$4^h$','$5^h$',
						'$6^h$','$7^h$', '$8^h$','$9^h$', '$10^h$',
						'$11^h$','$12^h$','$13^h$','$14^h$','$15^h$',
						'$16^h$','$17^h$','$18^h$','$19^h$','$20^h$', 
						'$21^h$', '$22^h$','$23^h$'])
	ax.set_xticklabels(labels_ra, fontsize=10)

	# Plot:
	# Label stars (optional)
	if displayStarNamesLabels:
		for i, txt in enumerate(x_star_labels):
			ax.annotate(txt, (x_ra_values[i], y_dec_values[i]), 
						horizontalalignment='center', verticalalignment='bottom', 
						fontsize=8)

	# Print for Testing:
	'''
	for i, txt in enumerate(x_star_labels):
		print("{0}: {1:05f} RA (degrees) and {2:05f} Declination (ruler)".format(txt, np.rad2deg(x_ra_values[i]), y_dec_values[i]))
		print("Proper Motion for {0} Years\n".format(year_since_2000))
	'''

	ax.scatter(x_ra_values, y_dec_values, s=10)
	years_for_title = year_since_2000
	suffix = ""
	if 1000 <  abs(years_for_title) and abs(years_for_title) < 100000:
		years_for_title = years_for_title / 1000
		suffix = "K"
	if abs(years_for_title) > 100000:
		years_for_title = years_for_title / 100000
		suffix = "M"
	ax.set_title("{0}ern Hemisphere [{1}{2} Years from Now]: {3}° to {4}°".format(northOrSouth, years_for_title, suffix, declination_max, declination_min))
	plt.show()
	fig.savefig('star_chart_{0}.png'.format(northOrSouth.lower()), dpi=fig.dpi)

if __name__ == '__main__':
	# stars to be included: 'name', ra HH.MM.SS, declination DD.SS
	# stars: ["name", "RA: HH.MM.SS", Declination DD.SS, Proper Motion Speed (mas/yr), Proper Motion Angle (DD.SS), Magnitude (V, Visual)]
	# Northern stars (+ declination)
	aldebaran_star = ["Aldebaran", "04.35.55", 16.30, 199.3, 161.4, 0.99]
	algol_star = ["Algol", "03.08.10", 40.57, 3.4, 119.0, 2.11]
	alioth_star = ["Alioth", "12.54.01", 55.57, 112.2, 94.2, 1.76] # Big Dipper
	alkaid_star = ["Alkaid", "13.47.32", 49.18, 122.1, 263.0, 1.86] # Big Dipper
	alphecca_star = ["Alphecca", "15.34.41", 26.42, 147.8, 126.4, 2.22]
	alpheratz_star = ["Alpheratz", "00.08.23", 29.05, 213.6, 139.9, 2.06]
	altair_star = ["Altair", "19.50.46", 8.52, 660.3, 54.3, 0.93]
	arcturus_star = ["Arcturus", "14.15.39", 19.10, 2279.4, 208.7, 0.16]
	barnards_star = ["Barnard's Star", "17.57.47", 4.44, 10393.3, 355.6, 9.6]
	bellatrix_star = ["Bellatrix", "05.25.07", 6.20, 15.2, 212.2, 1.66]
	betelgeuse_star = ["Betelgeuse", "05.55.10", 7.24, 29.8, 67.7, 0.57]
	chara_star = ["Chara", "12.33.43", 41.21, 762.9, 292.5, 4.25]
	caph_star = ["Caph", "00.09.10", 59.08, 553.5, 109.0, 2.28] # Beta Cassiopeiae
	capella_star = ["Capella", "05.16.41", 45.59, 433.5, 170.0, 0.08]
	castor_star = ["Castor", "07.34.35", 31.53, 240.3, 232.8, 1.58]
	cor_caroli_star = ["Cor-Caroli", "12.56.01", 38.19, 240.2, 283.2, 2.89]
	deneb_star = ["Deneb", "20.41.25", 45.16, 2.7, 47.4, 1.33]
	denebola_star = ["Denebola", "11.49.03", 14.34, 510.7, 257.0, 2.13]
	dubhe_star = ["Dubhe", "11.03.43", 61.45, 138.5, 255.5, 1.82] # Big Dipper
	hamal_star = ["Hamal", "02.07.10", 23.27, 239.7, 128.1, 2.02]
	megrez_star = ["Megrez", "12.15.25", 57.01, 104.3, 85.5, 3.30] # Big Dipper
	merak_star = ["Merak", "11.01.50", 56.22, 88.0, 67.6, 2.35] # Big Dipper
	muphrid_star = ["Muphrid", "13.54.41", 18.23, 361.5, 189.7, 2.68]
	mizar_star = ["Mizar", "13.23.55", 54.55, 124.6, 100.5, 2.22] # Big Dipper
	navi_star = ["Navi", "00.56.42", 60.43, 25.5, 98.9, 2.18] # Gamma Cassiopeiae
	pleiades_celaeno_star = ["Celaeno", "03.44.48", 24.17, 49.2, 156.2, 5.45]
	polaris_star = ["Polaris", "02.31.49", 89.15, 46.0, 104.9, 2.0]
	pollux_star = ["Pollux", "07.45.18", 28.01, 628.2, 265.8, 1.22]
	phecda_star = ["Phecda", "11.53.49", 53.41, 108.2, 84.2, 2.39] # Big Dipper
	procyon_star = ["Procyon", "07.39.18", 5.13, 1259.2, 214.6, 0.40]
	rasalhague_star = ["Rasalhague", "17.34.56", 12.33, 246.5, 154.0, 2.09]
	regulus_star = ["Regulus", "10.08.22", 11.58, 248.8, 271.3, 1.41]
	ruchbah_star = ["Ruchbah", "01.25.49", 60.14, 300.5, 99.4, 2.68] # Delta Cassiopeiae
	schedar_star = ["Schedar", "00.40.30", 56.32, 58.4, 122.7, 2.25] # Alpha Cassiopeiae
	segin_star = ["Segin", "01.54.23", 63.4, 37.3, 120.5, 3.35] # Epsilon Cassiopeiae
	seginus_star = ["Seginus", "14.32.04", 38.18, 190.4, 322.6, 3.04]
	spica_star = ["Spica", "13.25.11", -11.09, 52.3, 234.1, 1.06]
	vega_star = ["Vega", "18.36.56", 38.47, 349.7, 35.1, 0.03]

	#Southern stars (- declination)
	achernar_star = ["Achernar", "01.37.42", -57.14, 95.0, 113.7, 0.54]
	acamar_star = ["Acamar", "02.58.15", -40.18, 57.1, 293.8, 3.22]
	acrux_star = ["Acrux", "12.26.35", -63.05, 38.8, 247.5, 1.28] # Southern Cross
	alphard_star = ["Alphard", "09.27.35", -8.39, 37.6, 336.1, 1.98]
	alnilam_star = ["Alnilam", "05.36.12", -1.12, 1.6, 118.4, 1.72]
	alnitak_star = ["Alnitak", "05.40.45", -1.56, 3.8, 57.5, 1.90]
	ankaa_star = ["Ankaa", "00.26.17", -42.18, 425.7, 146.8, 2.38]
	antares_star = ["Antares", "16.29.24", -26.25, 26.3, 207.5, 1.07]
	beta_hydri_star = ["Beta Hydri", "00.25.45", -77.15, 2242.9, 81.6, 2.79]
	beta_phoenicis_star = ["Beta Phoenicis", "01.06.05", -46.43, 88.1, 293.4, 3.37]
	canopus_star = ["Canopus", "06.23.57", -51.41, 30.6, 40.6, -0.63]
	delta_crucis_star = ["Delta Crucis", "12.15.08", -58.44, 38.6, 253.0, 2.74] # Southern Cross
	diphda_star = ["Diphda", "00.43.35", -17.59, 234.7, 82.2, 2.05]
	formalhaut_star = ["Formalhaut", "22.57.38", -29.37, 367.9, 116.6, 1.23]
	gacrux_star = ["Gacrux", "12.31.09", -57.06, 266.6, 173.9, 1.65] # Southern Cross
	gamma_phoenicis_star = ["Gamma Phoenicis", "01.28.21", -43.19, 207.6, 184.9, 3.44]
	hadar_star = ["Hadar", "14.03.49", -60.22, 40.5, 235.2, 0.64]
	meissa_star = ["Meissa", "05.35.08", -9.56, 3.0, 186.6, 3.53]
	mintaka_star = ["Mintaka", "05.32.00", -0.18, 0.9, 137.2, 2.23]
	mimosa_star = ["Mimosa", "12.47.43", -59.41, 45.9, 249.4, 1.31] # Southern Cross
	rigel_star = ["Rigel", "05.14.32", -8.12, 1.4, 69.1, 0.28]
	sadalmelik_star = ["Sadalmelik", "22.05.47", -0.19, 21.3, 119.3, 2.93]
	saiph_star = ["Saiph", "05.47.45", -9.4, 1.9, 131.2, 2.06]
	sirius_star = ["Sirius", "06.45.08", -16.42, 1339.4, 204.1, -1.44]
	zubeneschamali_star = ["Zubeneschamali", "15.17.00", -9.22, 100.0, 258.7, 2.61]

	# add stars to total star list
	northern_star_chart_list = [aldebaran_star,
								algol_star,
								alioth_star,
								alkaid_star,
								alphecca_star,
								alpheratz_star,
								altair_star,
								arcturus_star,
								barnards_star,
								bellatrix_star,
								betelgeuse_star,
								chara_star,
								caph_star,
								capella_star,
								castor_star,
								cor_caroli_star,
								deneb_star,
								denebola_star,
								dubhe_star,
								hamal_star,
								megrez_star,
								merak_star,
								muphrid_star,
								mizar_star,
								navi_star,
								pleiades_celaeno_star,
								polaris_star,
								pollux_star,
								phecda_star,
								procyon_star,
								rasalhague_star,
								regulus_star,
								ruchbah_star,
								schedar_star,
								segin_star,
								seginus_star,
								spica_star,
								vega_star
								]

	southern_star_chart_list = [achernar_star,
								acamar_star,
								acrux_star,
								alphard_star,
								alnilam_star,
								alnitak_star,
								ankaa_star,
								antares_star,
								beta_hydri_star,
								beta_phoenicis_star,
								canopus_star,
								delta_crucis_star,
								diphda_star,
								formalhaut_star,
								gacrux_star,
								gamma_phoenicis_star,
								hadar_star,
								meissa_star,
								mintaka_star,
								mimosa_star,
								rigel_star,
								saiph_star,
								sirius_star,
								zubeneschamali_star
								]

	star_chart_list = northern_star_chart_list + southern_star_chart_list

	# Convert Star chart from RA hours to Radians to chart
	star_chart_list = convertRAhrtoRadians(star_chart_list)

	# Chart options
	displayStarNames = True # display chart with star names (False/True)
	displayDeclinationNumbers = True # display declination marks (False/True)
	northOrSouth = "South" # options: "North", "South", "Both" (changes the declination range)
	max_magnitude_filter = -1.0 # options: Filter by magnitude of star (magitude in Visual) (-2-10, 10 is dimmest, removes nothing)
	total_ruler_length = 30 # units (cut in half for each side of the ruler) (currently has to be even)
	increment_by = 10 # increment degrees by 1, 5, 10)
	year_of_plate_YYYY =  -53 # years since since 2000 (-53 = 1969)

	# Verify Hemisphere within valid range
	if northOrSouth not in ["Both", "North", "South"]:
		print("ERROR: Hemisphere not found")
		exit()

	# Plot star chart on a circular polar coordinate system
	if northOrSouth != "Both":
		if northOrSouth == "North":
			declination_min = northern_declination_min
			declination_max = northern_declination_max
		if northOrSouth == "South":
			declination_min = southern_declination_min
			declination_max = southern_declination_max
		plotCircluar(star_chart_list, 
					northOrSouth,
					max_magnitude_filter,
					year_of_plate_YYYY,
					displayStarNames,
					displayDeclinationNumbers,
					total_ruler_length,
					increment_by)
	if northOrSouth == "Both":
		# Run for both North and South
		# North:
		declination_min = northern_declination_min
		declination_max = northern_declination_max
		plotCircluar(star_chart_list, 
					"North",
					max_magnitude_filter,
					year_of_plate_YYYY,
					displayStarNames,
					displayDeclinationNumbers,
					total_ruler_length,
					increment_by)
		# South:
		declination_min = southern_declination_min
		declination_max = southern_declination_max
		plotCircluar(star_chart_list, 
					"South",
					max_magnitude_filter,
					year_of_plate_YYYY,
					displayStarNames,
					displayDeclinationNumbers,
					total_ruler_length,
					increment_by)

