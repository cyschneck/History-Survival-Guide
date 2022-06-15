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
eot_effect_of_eccentricity = "EOT-Eccentricity"

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
	new_planet_dict[orbital_period] = new_planet_dict[sidereal] / 365.25 # TODO TODO
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

	date_range_split_into_months = np.arange(0, range_of_x+1, range_of_x/12) # split into 12 months (based on Earth)
	for i, value in enumerate(date_range_split_into_months): date_range_split_into_months[i] = math.floor(value) # round all values
	plt.xticks(date_range_split_into_months)
	plt.scatter(x, y) # plot with real sun: sun with eccentricity
	plt.scatter(x, y_mean_distance) # plot the mean sun: sun with no eccentricity

	plt.grid()
	#plt.show()
	fig.savefig('eot_graphs/eccentricity/{0}_eot_sidereal_year_distance.png'.format(planet_name.lower()), dpi=fig.dpi)

def determineTrueAnomoly(planet_dictionary):
	# determine the time difference due to the eccentricity of a planet (True Anomoly)
	print("{0} : Eccentricity {1} and Sidereal Length = {2}".format(planet_dictionary[planet_name],
																	planet_dictionary[eccentricity],
																	planet_dictionary[sidereal]))
	def newtonRhaephsonsIteration(anomoly_En_radians, difference_anomoly, planet_eccentricity):
		# E(n+1) = En - f(En) / f'(En) 
		# where f(E) = E - esin(E) - mean_anomoly)
		# so f'(E) = 1 - ecos(E)
		# so E(n+1) = En - [ (En - esin(En) - mean_anomoly) / (1 - ecos(En)) ]
		En = anomoly_En_radians - ((difference_anomoly) / (1 - planet_eccentricity * math.cos(anomoly_En_radians)))
		#guess_anoloy_amount = anomoly_guess_En_radians - (planet_eccentricity * math.sin(anomoly_guess_En_radians))
		En = round(En, 8)
		return En
	
	def calculateDifferenceInAnomoly(En, mean_anomoly_radians, planet_eccentricity):
		# Calculate the difference bteween the mean anomolies
		#print("en = {0}".format(En))
		#print("delta = {0}".format(mean_anomoly_radians))
		#print("eccentricity = {0}".format(planet_eccentricity))
		difference = En - (planet_eccentricity * math.sin(En)) - mean_anomoly_radians
		difference = round(difference, 8)
		return difference

	half_of_year = math.ceil(int(planet_dictionary[sidereal])/2) #TODO: allow negative values for after half year
	sidereal_day_list = np.arange(0, half_of_year, 1)#np.arange(0, int(planet_dictionary[sidereal])+1, 1)
	# Caught between values: 166, 169, 170, 234, 266
	# Breaks at 183 when values swap to negative
	check_value = 50000 # TESTING TESTING, to be REMOVED
	effect_of_eccentricity_dict = {} # {day : difference true to mean sun}

	for day_of_year in sidereal_day_list:
		#print("Day of the Year = {0}".format(day_of_year))
		mean_anomoly_radians = (2 * np.pi * day_of_year) / planet_dictionary[sidereal]
		mean_anomoly_radians = round(mean_anomoly_radians, 8)
		if day_of_year == check_value: print("\n1st Guess of True Anomoly: E1 = {0}".format(mean_anomoly_radians))

		differnce_e = calculateDifferenceInAnomoly(mean_anomoly_radians, mean_anomoly_radians, planet_dictionary[eccentricity])
		if day_of_year == check_value: print("1st Difference: D_e_1 = {0}".format(differnce_e))

		# iterate until mean_anomoly En = En-1
		iteration_end = False
		en_radians = mean_anomoly_radians
		en_difference = differnce_e
		previous_difference = differnce_e
		if day_of_year == check_value: print("\nIteration\n")
		n = 0
		while (iteration_end == False):
			n += 1
			En = newtonRhaephsonsIteration(en_radians, en_difference, planet_dictionary[eccentricity])
			difference_En = calculateDifferenceInAnomoly(En, mean_anomoly_radians, planet_dictionary[eccentricity])
			#difference_between_iterations = previous_difference - difference_En
			if difference_En == 0.0: iteration_end = True
			if day_of_year == check_value: print("{0} guess at True Anomoly: E{0} = {1}".format(n+1, En))
			if day_of_year == check_value: print("{0} Difference: D_e_{0} = {1}".format(n+1, difference_En))
			#if day_of_year == check_value: print("Difference Between E{0} and E{1} diff = {2}\n".format(n, n+1, difference_between_iterations))
			en_radians = En
			en_difference = difference_En
			#previous_difference = difference_En
			if n > 100: 
				print("Day of the Year = {0}".format(day_of_year))
				print("ERROR ERROR ERROR: Caught between two values")
				iteration_end = True #TESTING TO REMOVE
		if day_of_year == check_value: 
			print("Final En (E{0}) = {1}".format(n+2, En)) # +1 for first iteration, +1 for final iteration with no change
			print("Returned after: {0} iterations".format(n+2))

		# Calculate Calculate True Anomoly
		if day_of_year == check_value: print("\nCalculate True Anomoly")
		planet_eccentricty_anomoly = math.sqrt((1 + planet_dictionary[eccentricity]) / (1-planet_dictionary[eccentricity]))
		tan_anomoly = planet_eccentricty_anomoly * math.tan(en_radians / 2)
		if day_of_year == check_value: print("W = {0}".format(round(tan_anomoly, 8)))
		true_anomoly_radains = 2 * math.atan(tan_anomoly)
		true_anomoly_radains = round(true_anomoly_radains, 8)
		if day_of_year == check_value: print("Angle = {0}".format(true_anomoly_radains))

		# Calculate the Difference between the True and the Mean Sun
		if day_of_year == check_value: print("\nCalculate the Difference between the True and the Mean Sun")
		mean_anomoly_degrees = round(np.rad2deg(mean_anomoly_radians), 8)
		true_anomoly_degrees = round(np.rad2deg(true_anomoly_radains), 8)
		difference_anomoly_degrees = true_anomoly_degrees - mean_anomoly_degrees
		difference_anomoly_degrees = round(difference_anomoly_degrees, 8)
		if day_of_year == check_value: print("{0} - {1} = {2} degrees".format(true_anomoly_degrees, mean_anomoly_degrees, difference_anomoly_degrees))
		difference_in_minutues = 4 * difference_anomoly_degrees
		difference_in_minutues = round(difference_in_minutues, 8)
		if day_of_year == check_value: print("Difference Clock Minutes = {0}".format(difference_in_minutues))
		effect_of_eccentricity_dict[day_of_year] = difference_in_minutues
		effect_of_eccentricity_dict[half_of_year+day_of_year] = -difference_in_minutues # fill negative half: FIX BY ALLOWING NEGATIVE VALUES TO BE CALCULATED

	return effect_of_eccentricity_dict

def plotEffectOfEccentricty(planet_dict, effect_of_eccentricity_dict):
	# Plot Effect of Eccentricity Over the Year
	fig = plt.figure(figsize=(12,12), dpi=100)

	x_sidereal_days = effect_of_eccentricity_dict.keys()
	y_clock_minutes = effect_of_eccentricity_dict.values()

	# Set up x axis
	date_range_split_into_months = np.arange(0, planet_dict[sidereal]+1, planet_dict[sidereal]/12) # split into 12 months (based on Earth)
	for i, value in enumerate(date_range_split_into_months): date_range_split_into_months[i] = math.floor(value) # round all values
	plt.xticks(date_range_split_into_months)

	# Set up y axis
	interval_for_y = 1
	if max(y_clock_minutes) > 10:
		interval_for_y = (math.ceil(max(y_clock_minutes)) / 10) # split to only display 10 segments
	y_range_min = np.arange(math.floor(min(y_clock_minutes)), 0, interval_for_y)
	for i, value in enumerate(y_range_min): y_range_min[i] = math.ceil(value)
	y_range_max = np.arange(0, math.ceil(max(y_clock_minutes))+1, interval_for_y)
	for i, value in enumerate(y_range_max): y_range_max[i] = math.floor(value)
	y_range = np.concatenate([y_range_min, y_range_max])
	plt.yticks(y_range)

	plt.scatter(effect_of_eccentricity_dict.keys(), effect_of_eccentricity_dict.values())
	plt.title("{0}: Difference Between Dynamical Mean and True Solar Time - Effect of Eccentricity (Min: {1}, Max: {2} )".format(planet_dict[planet_name],
																																min(y_clock_minutes),
																																max(y_clock_minutes)))
	plt.xlabel("Days in the Sidereal Year")
	plt.ylabel("Minutes")
	plt.grid()
	plt.show()
	fig.savefig('eot_graphs/eccentricity/{0}_eot_effect_of_eccentricity.png'.format(planet_dict[planet_name].lower()), dpi=fig.dpi)

def plotChangeInTimeBasedOnEccentricity(all_planet_dict):
	# Plot the Effect of Eccentricity based on Eccentricity of the Planets
	fig, ax = plt.subplots(figsize=(12,12), dpi=100)

	x_eccentricity = []
	y_change_in_minutes = []
	planet_names = []
	for planet, planet_dict in all_planet_dict.items():
		x_eccentricity.append(planet_dict[eccentricity])
		y_change_in_minutes.append(planet_dict[eot_effect_of_eccentricity])
		planet_names.append(planet_dict[planet_name])

	a, b = np.polyfit(x_eccentricity, y_change_in_minutes, 1) # line of best fit
	plt.yticks(np.arange(0, math.ceil(max(y_change_in_minutes))+1, 5))
	plt.plot(x_eccentricity, a*np.array(x_eccentricity)+b, color='grey', linestyle='--', linewidth=1)
	plt.scatter(x_eccentricity, y_change_in_minutes)

	for i, planet_name_txt in enumerate(planet_names): # annotate data points with planet names
		ax.annotate(planet_name_txt, (x_eccentricity[i], y_change_in_minutes[i]))

	plt.title("Max Change in Minutes due to Eccentricity: Minutes = {0:.2f} + {1:.2f} * Eccentricity".format(b, a))
	plt.xlabel("Eccentricity")
	plt.ylabel("Max Change in Minutes")
	plt.show()
	fig.savefig('eot_graphs/eccentricity/change_in_time_due_to_eccentricity.png', dpi=fig.dpi)

if __name__ == '__main__':
	# Set dictionary values: Planet Name, Semi-Major Axis (km), Eccentricity, Sidereal
	setDictionaryValues("Mercury", 57909050, 0.205630, 87.97)
	setDictionaryValues("Venus", 108208000, 0.006772, 224.701)
	setDictionaryValues("Earth", 149598923, 0.016713, 365.24219100)
	setDictionaryValues("Mars", 227939366, 0.0934, 686.98)
	setDictionaryValues("Jupiter", 778479000, 0.0489, 4332.59)
	setDictionaryValues("Saturn", 1433536555, 0.0565, 10759.22)
	setDictionaryValues("Uranus", 2870971632, 0.04717, 30688.5)
	setDictionaryValues("Neptune", 4498410000, 0.008678, 60195)

	for planet, single_planet_dictionary in full_planet_dict.items():
		distance_pos_each_day_of_year = determineEccentricityEffectDistance(single_planet_dictionary)
		effect_of_eccentricity_over_year_dict = determineTrueAnomoly(single_planet_dictionary)
		single_planet_dictionary[eot_effect_of_eccentricity] = max(effect_of_eccentricity_over_year_dict.values()) # difference in EOT
		plotEffectOfEccentricty(single_planet_dictionary, effect_of_eccentricity_over_year_dict)
	plotChangeInTimeBasedOnEccentricity(full_planet_dict) # plot the change in minutes due to eccentricity
