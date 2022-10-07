# python3 calculate_base_plate.py: Python 3.7.3
import numpy as np
import math
import matplotlib.pyplot as plt

def convertObliquityWithin90(ob_planet):
	# obliquity converted to be within 0-89.99
	if ob_planet > 90: # obliquity over 90
		ob_planet = ob_planet % 90
	if ob_planet == 90: # Undefined at 90, convert to 89.99
		ob_planet = 89.99
	if ob_planet < 0: # negative
		ob_planet = 360 + ob_planet
		ob_planet = ob_planet % 90
	return ob_planet

def radiusOfTropicsAndEquator(base_plate_radius, obliquity_of_planet):
	# return the radius for all the cirlces on the base plate
	obliquity_of_planet = convertObliquityWithin90(obliquity_of_planet) # obliquity within 0-89.99
	outer_tropic_radius = base_plate_radius # on base plate = Tropic of Capricorn
	equator_radius = base_plate_radius / (math.tan(np.deg2rad(45 + (obliquity_of_planet/2)))) # on base plate = Tropic of Cancer
	inner_tropic_radius = equator_radius * math.tan(np.deg2rad(45 - (obliquity_of_planet/2)))
	return outer_tropic_radius, equator_radius, inner_tropic_radius

def plotEffectOfObliquityOnRadius(radius_of_base_plate):
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
	plt.title("Change in Obliquity vs. Base Plate Radius (where r=1)")
	plt.xlabel("Obliquity (°)")
	plt.ylabel("Radius")

	plt.scatter(obliquity_range, outer_radius_lst, label="Outer Radius")
	plt.scatter(obliquity_range, equator_radius_lst, label="Equator Radius")
	plt.scatter(obliquity_range, inner_radius_lst, label="Inner Radius")
	
	planet_8_obliquities = {"Mercury": 0.1,
							"Venus": 177.4,
							"Earth": 23.4,
							"Mars": 25.19,
							"Jupiter": 3.12,
							"Saturn": 26.73,
							"Uranus": 97.86,
							"Neptune": 29.56}

	for planet_given_name, planet_given_obliquity in planet_8_obliquities.items(): 
		# vertical dash line at the positions of planet's obliquities
		planet_given_obliquity = convertObliquityWithin90(planet_given_obliquity)
		plt.axvline(planet_given_obliquity, linewidth=0.5, color="black", linestyle="dashed")
		plt.text(x=planet_given_obliquity, y=0.1, s=planet_given_name, fontsize=8, rotation=90) # add label on figure

	plt.legend()
	plt.show()
	fig.savefig('base_plate_change_due_to_obliquity.png', dpi=fig.dpi)

def constructBasePlate(radius_plate, obliquity_planet, planet_name):
	# Construct base plate with concentric circles
	fig = plt.figure(figsize=(12,12), dpi=100)
	ax = fig.subplots(subplot_kw={'projection': 'polar'})
	ax.set_ylim([0,radius_plate]) # set outer limit
	ax.set_xticklabels([])# remove x labels for degrees
	ax.set_yticklabels([])
	ax.set_rticks(np.arange(0, radius_of_base_plate, radius_of_base_plate/10))
	ax.grid(True)

	outer_radius, equator_radius, inner_radius = radiusOfTropicsAndEquator(radius_plate, obliquity_planet)
	plt.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*outer_radius, linewidth=3.5, color='black', label="Outer Radius = {0:.02f}".format(outer_radius))
	plt.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*equator_radius, linewidth=3.5, color='black', label="Equator Radius = {0:.02f}".format(equator_radius))
	plt.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*inner_radius, linewidth=3.5, color='black', label="Inner Radius = {0:.02f}".format(inner_radius))

	# place legend outside of plot
	figure_size = ax.get_position()
	ax.set_position([figure_size.x0, figure_size.y0, figure_size.width * 0.8, figure_size.height]) # shrink horizontally by 20%
	ax.legend(loc="center left", bbox_to_anchor=(1, 0.5)) # show labels for radius

	plt.title("Base Plate for {0} with Obliquity {1}° for radius = {2}".format(planet_name, obliquity_planet, radius_plate))
	plt.show()
	fig.savefig('base_plate_for_{0}_at_{1}_degrees.png'.format(planet_name.lower(), obliquity_planet), dpi=fig.dpi)

if __name__ == '__main__':
	# Find Ratio between concentric circles for base plate based on obliquity
	radius_of_base_plate = 15
	plotEffectOfObliquityOnRadius(radius_of_base_plate)

	## Testing on Earth's obliquity
	#obliquity_of_planet = 23.4 # obliquity of Earth
	#constructBasePlate(radius_of_base_plate, obliquity_of_planet, "Earth")

	planet_8_obliquities = {"Mercury": 0.1,
							"Venus": 177.4,
							"Earth": 23.4,
							"Mars": 25.19,
							"Jupiter": 3.12,
							"Saturn": 26.73,
							"Uranus": 97.86,
							"Neptune": 29.56}
	for planet_name, planet_ob in planet_8_obliquities.items():
		constructBasePlate(radius_of_base_plate, planet_ob, planet_name)
