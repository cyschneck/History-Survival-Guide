# Calculate the Equation of Time
# python3 calculate_equation_of_time.py
import math

planet_dict = {}

def setDictionaryValues(planet_name, semi_major_axis_value, eccentricity_value, sidereal_length_in_days):
	# set a dictionary value
	new_planet_dict = {}
	# Set names as variables to edit
	semi_major_axis = "Semi-Major Axis (km)"
	eccentricity = "Eccentricity"
	sidereal = "Sidereal (days)"
	semi_minor_axis = "Semi-Minor Axis (km)"
	perhelion = "Perhelion (AU)"
	aphelion = "Aphelion (AU)"
	orbital_period = "Orbital Period (years)"
	mean_distance = "Mean Distance from Sun (AU)"

	new_planet_dict[semi_major_axis] = semi_major_axis_value
	new_planet_dict[eccentricity] = eccentricity_value
	new_planet_dict[sidereal] = sidereal_length_in_days
	new_planet_dict[semi_minor_axis] = new_planet_dict[semi_major_axis] * math.sqrt(1 - new_planet_dict[eccentricity]**2)
	new_planet_dict[perhelion] = new_planet_dict[semi_major_axis] * (1 - new_planet_dict[eccentricity])
	new_planet_dict[aphelion] = new_planet_dict[semi_major_axis] * (1 + new_planet_dict[eccentricity])
	new_planet_dict[orbital_period] = new_planet_dict[sidereal] / 365.25
	new_planet_dict[mean_distance] = new_planet_dict[orbital_period] ** (2.0 / 3.0) # Kepler's Third Law: P^2 = D^3 solved for D
	planet_dict[planet_name] = new_planet_dict # add planet to Dictionary

def determineEccentricityEffectDistance():
	# determine difference between mean sun and real sun (with eccentricity)
	#distance_in_au = mean_distance_sun_planet - eccentricity * math.cos(np.deg2rad((360/sidereal_length) * (day_of_sidereal - day_of_perihelion)))

if __name__ == '__main__':
	# Set dictionary values: Planet Name, Semi-Major Axis, Eccentricity, Sidereal
	setDictionaryValues("Earth", 149598923, 0.0167086, 	365.25)
	setDictionaryValues("Mars", 227939366, 0.0934, 687)
	for planet, values in planet_dict.items():
		print(planet)
		print(values)
