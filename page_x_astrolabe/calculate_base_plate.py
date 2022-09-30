# python3 calculate_base_plate.py: Python 3.7.3
import numpy as np
import math
import matplotlib.pyplot as plt

def radiusOfTropicsAndEquator(base_plate_radius, obliquity_of_planet):
	# return the radius for all the cirlces on the base plate
	outer_tropic_radius = radius_of_base_plate # on base plate = Tropic of Capricorn
	equator_radius = radius_of_base_plate / (math.tan(np.deg2rad(45 + (obliquity_of_planet/2)))) # on base plate = Tropic of Cancer
	inner_tropic_radius = equator_radius * math.tan(np.deg2rad(45 - (obliquity_of_planet/2)))
	return outer_tropic_radius, equator_radius, inner_tropic_radius

if __name__ == '__main__':
	# Find Ratio between concentric circles for base plate based on obliquity
	"""#EARTH TESTING:
	earth_obliquity = 23.4
	radius_of_base_plate = 15
	
	capricorn_radius, equator_radius, cancer_radius = radiusOfTropicsAndEquator(radius_of_base_plate, earth_obliquity)
	print("Radius of Cirlces on Base Plate: \nCapricorn = {0}\nEquator = {1:04f}\nCancer = {2:04f}".format(capricorn_radius,
																										equator_radius,
																										cancer_radius))
	"""
	obliquity_range = np.arange(0, 90, 1) # undefined at 90 degrees
	radius_of_base_plate = 1 # 1 for simple calculations
	outer_radius_lst = []
	equator_radius_lst = []
	inner_radius_lst = []
	for ob in obliquity_range:
		outer_radius, equator_radius, inner_radius = radiusOfTropicsAndEquator(radius_of_base_plate, ob)
		outer_radius_lst.append(outer_radius)
		equator_radius_lst.append(equator_radius)
		inner_radius_lst.append(inner_radius)

	# Plot
	fig = plt.figure(figsize=(10,10), dpi=100)
	ax = fig.subplots()
	plot_every_x = np.arange(0, 89, 5) # plot every five increments for ease of readability
	plot_every_x = np.append(plot_every_x, 89) # include last point at 89 degrees
	plt.xticks(plot_every_x, fontsize=8)
	plt.title("Change in Obliquity vs. Base Plate Radius")
	plt.xlabel("Obliquity (°)")
	plt.ylabel("Radius")
	plt.scatter(obliquity_range, outer_radius_lst, label="Outer Radius")
	plt.scatter(obliquity_range, equator_radius_lst, label="Equator Radius")
	plt.scatter(obliquity_range, inner_radius_lst, label="Inner Radius")
	plt.legend()
	plt.show()
	fig.savefig('base_plate_change_due_to_obliquity.png', dpi=fig.dpi)



