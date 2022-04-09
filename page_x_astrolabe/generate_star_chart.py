# Generate a star chart for astrolabe
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def convertRAtoRadians(ra_in_degrees):
	# convert RA from degrees to radians
	ra_in_radains = ra_in_degrees / 180.0 * np.pi
	return ra_in_radains

def plotCircluar():
	# plot star chart as a circular graph
	fig = plt.figure(figsize=(8,8), dpi=120)
	ax = fig.subplots(subplot_kw={'projection': 'polar'})

	# Set Right Ascension (astronomical 'longitude') as X
	angles_ra = np.array([330, 345, 0, 15, 30, 45, 60, 75, 90, 105, 120,
						135, 150,  165, 180, 195, 210, 225, 240, 255,
						270, 285, 300, 315])
	plt.xticks(angles_ra * np.pi / 180, fontsize=8)
	ax.set_xticklabels(['$22^h$', '$23^h$', '$0^h$', '$1^h$', '$2^h$',
						'$3^h$', '$4^h$', '$5^h$','$6^h$',
						'$7^h$',
						'$8^h$',
						'$9^h$',
						'$10^h$',
						'$11^h$',
						'$12^h$',
						'$13^h$',
						'$14^h$',
						'$15^h$',
						'$16^h$',
						'$17^h$',
						'$18^h$',
						'$19^h$',
						'$20^h$',
						'$21^h$'], fontsize=10)
	
	# Set Declination (astronomical 'latitude') as Y
	ax.set_ylim(-90, 90)
	declination_values = np.arange(-90, 91, 10)
	plt.yticks(declination_values, fontsize=5)
	#ax.set_rlabel_position(120)
	#ax.set_yticklabels(['$-80^{\circ}$', '$-70^{\circ}$', '$-60^{\circ}$'],
	#	fontsize=10)
	plt.show()

if __name__ == '__main__':
	plotCircluar()
