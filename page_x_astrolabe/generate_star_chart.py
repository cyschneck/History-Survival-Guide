# Generate a star chart for astrolabe
# python3 generate_star_chart.py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

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
		ra_in_radians = ra_in_degrees / 180.0 * np.pi
		star[1] = ra_in_radians
	return star_list

def plotCircluar(star_list, northOrSouth, displayStarNamesLabels, displayDeclinationMarks):
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
	northern_chart_min = -30
	northern_chart_max = 70
	southern_chart_min = -70
	southern_chart_max = 30
	full_declination_min = -90
	full_declination_max = 90

	# Split up chart into North/South hemisphere
	if northOrSouth == "Both":
		ax.set_ylim(full_declination_min, full_declination_max)
		declination_values = np.arange(full_declination_min, full_declination_max+1, 10) # +1 to show max value in range
	if northOrSouth == "North":
		ax.set_ylim(northern_chart_min, northern_chart_max)
		declination_values = np.arange(northern_chart_min, northern_chart_max+1, 5) # +1 to show max value in range
	if northOrSouth == "South":
		ax.set_ylim(southern_chart_min, southern_chart_max)
		declination_values = np.arange(southern_chart_min, southern_chart_max+1, 5) # +1 to show max value in range

	if displayDeclinationMarks:
		plt.yticks(declination_values, fontsize=7)
		#ax.set_yticklabels(['$-80^{\circ}$', '$-70^{\circ}$', '$-60^{\circ}$'], fontsize=10)
		ax.set_rlabel_position(120)
	else:
		plt.yticks(declination_values, fontsize=0)
	
	# convert to x and y values for stars
	x_star_labels = []
	x_ra_values = []
	y_dec_values = []
	for star in star_list:
		x_star_labels.append(star[0])
		x_ra_values.append(star[1])
		y_dec_values.append(star[2])
	ax.scatter(x_ra_values, y_dec_values)

	# label stars (optional)
	if displayStarNamesLabels:
		for i, txt in enumerate(x_star_labels):
			ax.annotate(txt, (x_ra_values[i], y_dec_values[i]))

	plt.show()
	fig.savefig('star_chart.png', dpi=fig.dpi)

if __name__ == '__main__':
	# stars to be included: 'name', ra HH.MM.SS, declination DD.SS
	# Northern stars
	sirus_star = ["Sirus", "06.45.08", -16.42]
	dubhe_star = ["Dubhe", "11.03.43", 61.45]
	megrez_star = ["Megrez", "12.15.25", 57.01]
	polaris_star = ["Polaris", "02.31.49", 89.15]
	betelgeuse_star = ["Betelgeuse", "05.55.10", 7.24]
	rigel_star = ["Rigel", "05.14.32", -8.12]
	spica_star = ["Spica", "13.25.11", -11.09]
	vega_star = ["Vega", "18.36.56", 38.47]
	altair_star = ["Altair", "19.50.46", 8.52]
	procyon_star = ["Procyon", "07.39.18", 5.13]
	pollux_star = ["Pollux", "07.45.18", 28.01]
	castor_star = ["Castor", "07.34.35", 31.53]
	arcturus_star = ["Arcturus", "14.15.39", 19.10]
	#Southern stars
	mimosa_star = ["Mimosa", "12.47.43", -59.41]
	gamma_phoenics_star = ["Gamma Phoenics", "01.28.21", -43.19]
	beta_hydri_star = ["Beta Hydri", "00.25.45", -77.15]

	# add stars to total star list
	northern_star_chart_list = [sirus_star,
								dubhe_star,
								megrez_star,
								polaris_star,
								betelgeuse_star,
								rigel_star,
								spica_star,
								vega_star,
								altair_star,
								procyon_star,
								pollux_star,
								castor_star,
								arcturus_star]

	southern_star_chart_list = [mimosa_star,
								gamma_phoenics_star,
								beta_hydri_star]

	star_chart_list = northern_star_chart_list + southern_star_chart_list

	# Convert Star chart from RA hours to Radians to chart
	#print(star_chart_list)
	star_chart_list = convertRAhrtoRadians(star_chart_list)
	#print(star_chart_list)

	displayStarNames = True # display chart with star names
	displayDeclinationMarks = True # display declination marks
	northOrSouth = "Both" # options: "North", "South", "Both" (changes the declination range)

	plotCircluar(star_chart_list, northOrSouth, displayStarNames, displayDeclinationMarks)
