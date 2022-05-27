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

	distance_position_for_days_of_year = [] # store the distance from the sun on each day of the sidereal year
	for day in all_days_of_the_year_list:
		position_distance_day_au = planet_dict[mean_distance] - planet_dict[eccentricity] * math.cos(np.deg2rad((360/planet_dict[sidereal]) * (day - day_of_perihelion)))
		distance_position_for_days_of_year.append(position_distance_day_au)

	# Plot Sidereal Year Distance
	plotOverSideRealDistance(planet_dict[planet_name],
							all_days_of_the_year_list,
							distance_position_for_days_of_year,
							planet_dict[sidereal]+1)

def plotOverSideRealDistance(planet_name, x, y, range_of_x):
	# Plot Distance from Sun on every day of the Sidereal Year for a planet
	fig = plt.figure(figsize=(12,12), dpi=100)
	plt.title("Distance from Sun on Every Day of the Sidereal Year: {0}".format(planet_name))
	plt.xticks(np.arange(0, range_of_x, 20))
	plt.scatter(x, y)
	plt.show()
	fig.savefig('{0}_eot_sidereal_year_distance.png'.format(planet_name.lower()), dpi=fig.dpi)

if __name__ == '__main__':
	# Set dictionary values: Planet Name, Semi-Major Axis, Eccentricity, Sidereal
	setDictionaryValues("Earth", 149598923, 0.0167086, 	365.25)
	setDictionaryValues("Mars", 227939366, 0.0934, 687)
	for planet, single_planet_dictionary in full_planet_dict.items():
		print(planet)
		print(single_planet_dictionary)
		determineEccentricityEffectDistance(single_planet_dictionary)
