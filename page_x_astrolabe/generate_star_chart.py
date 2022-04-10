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

def plotCircluar(star_list):
	# plot star chart as a circular graph
	fig = plt.figure(figsize=(8,8), dpi=120)
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
	ax.set_ylim(-90, 90)
	declination_values = np.arange(-90, 91, 10)
	plt.yticks(declination_values, fontsize=5)
	ax.set_rlabel_position(120)
	#ax.set_yticklabels(['$-80^{\circ}$', '$-70^{\circ}$', '$-60^{\circ}$'], fontsize=10)
	
	# convert to x and y values
	x_star_labels = []
	x_ra_values = []
	y_dec_values = []
	for star in star_list:
		x_star_labels.append(star[0])
		x_ra_values.append(star[1])
		y_dec_values.append(star[2])
	ax.scatter(x_ra_values, y_dec_values)
	# label stars
	for i, txt in enumerate(x_star_labels): 
		ax.annotate(txt, (x_ra_values[i], y_dec_values[i]))
	plt.show()
	fig.savefig('star_chart.png', dpi=fig.dpi)

if __name__ == '__main__':
	sirus_star = ["Sirus", "06.45.08917", -16.42]
	dubhe_star = ["Dubhe", "11.03.4367152", 61.45]

	# add stars to total star list
	star_chart_list = []
	star_chart_list.append(sirus_star)
	star_chart_list.append(dubhe_star)
	
	# Convert Star chart from RA hours to Radians to chart
	print(star_chart_list)
	star_chart_list = convertRAhrtoRadians(star_chart_list)
	print(star_chart_list)
	
	plotCircluar(star_chart_list)
