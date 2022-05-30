# Calculate the Equation of Time
# python3 calculate_equation_of_time.py
import math
import numpy as np
import matplotlib.pyplot as plt

# Dictionary and Key Names
full_planet_dict = {}
planet_name = "Planet Name"
semi_major_axis = "Semi-Major Axis (km)"
eccentricity = "Eccentricity"
sidereal = "Sidereal (days)"
semi_minor_axis = "Semi-Minor Axis (km)"
perhelion = "Perhelion (AU)"
aphelion = "Aphelion (AU)"
orbital_period = "Orbital Period (years)"
mean_distance = "Mean Distance from Sun (AU)"
mean_sun_area = "Mean Sun Area (AU)"

def setDictionaryValues(planet_name_value, semi_major_axis_value, eccentricity_value, sidereal_length_in_days):
	# set a dictionary value
	new_planet_dict = {}

	new_planet_dict[planet_name] = planet_name_value
	new_planet_dict[semi_major_axis] = semi_major_axis_value
	new_planet_dict[eccentricity] = eccentricity_value
	new_planet_dict[sidereal] = sidereal_length_in_days
	#new_planet_dict[semi_minor_axis] = new_planet_dict[semi_major_axis] * math.sqrt(1 - new_planet_dict[eccentricity]**2)
	#new_planet_dict[perhelion] = new_planet_dict[semi_major_axis] * (1 - new_planet_dict[eccentricity])
	#new_planet_dict[aphelion] = new_planet_dict[semi_major_axis] * (1 + new_planet_dict[eccentricity])
	new_planet_dict[orbital_period] = new_planet_dict[sidereal] / 365.25
	new_planet_dict[mean_distance] = new_planet_dict[orbital_period] ** (2.0 / 3.0) # Kepler's Third Law: P^2 = D^3 solved for D
	full_planet_dict[planet_name_value] = new_planet_dict # add planet to Dictionary

def determineEccentricityEffectDistance(planet_dict):
	# determine difference between mean sun and real sun (with eccentricity)
	all_days_of_the_year_list = np.arange(0, planet_dict[sidereal]+1)
	day_of_perihelion = 4 # for Earth: TODO

	distance_position_for_days_of_year_with_eccentricity = [] # store the distance from the sun on each day of the sidereal year
	distance_position_for_days_of_year_without_eccentricity = [] # store distance from sun for a mean distance
	for day in all_days_of_the_year_list:
		position_distance_day_au = planet_dict[mean_distance] - planet_dict[eccentricity] * math.cos(np.deg2rad((360/planet_dict[sidereal]) * (day - day_of_perihelion)))
		distance_position_for_days_of_year_with_eccentricity.append(position_distance_day_au)
		distance_position_for_days_of_year_without_eccentricity.append(planet_dict[mean_distance])

	# Plot Sidereal Year Distance
	plotOverSideRealDistance(planet_dict[planet_name],
							all_days_of_the_year_list,
							distance_position_for_days_of_year_with_eccentricity,
							planet_dict[sidereal]+1,
							distance_position_for_days_of_year_without_eccentricity)
	return distance_position_for_days_of_year_with_eccentricity

def plotOverSideRealDistance(planet_name, x, y, range_of_x, y_mean_distance):
	# Plot Distance from Sun on every day of the Sidereal Year for a planet
	fig = plt.figure(figsize=(12,12), dpi=100)
	plt.title("{0}: Distance from Sun on Every Day of the Sidereal Year".format(planet_name))
	plt.xticks(np.arange(0, range_of_x, 20))
	plt.scatter(x, y) # plot with real sun: sun with eccentricity
	plt.scatter(x, y_mean_distance) # plot the mean sun: sun with no eccentricity

	plt.show()
	fig.savefig('eot_graphs/{0}_eot_sidereal_year_distance.png'.format(planet_name.lower()), dpi=fig.dpi)

### TESTING ###
def areaOfMeanSun(mean_distance_of_planet, sidereal_length):
	# calculate the area for the distance that the mean sun moves every 'day'
	#print("Mean Distance = {0} AU".format(mean_distance_of_planet))
	#print("Sidereal Length = {0} Days".format(sidereal_length))
	angle_for_day = 360 / sidereal_length
	#print("Angle = {0}".format(math.cos(np.deg2rad(angle_for_day))))
	#print(2 * (mean_distance_of_planet**2))
	#print(2*(mean_distance_of_planet*mean_distance_of_planet) * math.cos(np.deg2rad(angle_for_day)))
	# a = sqrt(b^2 + c^2 - 2bc * cos(angle))
	distance_traveled = (2 * (mean_distance_of_planet**2)) - (2*(mean_distance_of_planet*mean_distance_of_planet) * math.cos(np.deg2rad(angle_for_day)))
	distance_traveled = math.sqrt(distance_traveled)
	#print("Distance Traveled = {0}".format(distance_traveled))
	# s = 1/2 (a+b+c)
	s = 0.5 * (distance_traveled + mean_distance_of_planet + mean_distance_of_planet) # semi-perimeter of triangle
	#print("Semi-Perimeter = {0}".format(s))
	# Area = sqrt(s(s-a)(s-b)(s-c))
	mean_sun_area = (s-distance_traveled)*(s-mean_distance_of_planet)*(s-mean_distance_of_planet)
	mean_sun_area = math.sqrt(s*mean_sun_area)
	print("Mean Area = {0} AU".format(mean_sun_area))
	return mean_sun_area

def calculateAnglesForEachDay(area_of_mean_sun, distance_pos_list):
	# calculate the angles for each day of the year based on Kepler's Second Law
	# Area_mean = Area_with_eccentricity
	# Area = 1/2 * bc * sin(angle) == angle = sin^-1(2*Area_Mean / bc)
	angle_list_for_each_day = []
	for i in distance_pos_list:
		print(i)
		#angle_of_position = math.arcsin((2 * area_of_mean_sun) / (
### TESTING ###

if __name__ == '__main__':
	# Set dictionary values: Planet Name, Semi-Major Axis (km), Eccentricity, Sidereal
	setDictionaryValues("Mercury", 57909050, 0.205630, 87.97)
	#setDictionaryValues("Venus", 108208000, 0.006772, 224.701)
	setDictionaryValues("Earth", 149598923, 0.0167086, 	365.25)
	#setDictionaryValues("Mars", 227939366, 0.0934, 686.98)
	#setDictionaryValues("Jupiter", 778479000, 0.0489, 4332.59)
	#setDictionaryValues("Saturn", 1433536555, 0.0565, 10759.22)
	#setDictionaryValues("Uranus", 2870971632, 0.04717, 30688.5)
	#setDictionaryValues("Neptune", 4498410000, 0.008678, 60195)
	for planet, single_planet_dictionary in full_planet_dict.items():
		print(planet)
		print(single_planet_dictionary)
		distance_pos_each_day_of_year = determineEccentricityEffectDistance(single_planet_dictionary)
		#single_planet_dictionary[mean_sun_area] = areaOfMeanSun(single_planet_dictionary[mean_distance], single_planet_dictionary[sidereal])

