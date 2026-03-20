# Calculate the Offset and Angular Distance of the Eccentric Calendar for the Back of the Astrolabe
# pytho3 calculate_eccentric_calendar_offset.py
# Based on James Morrison's 'Astrolabe' pg. 116
import math
import numpy as np
import configparser
import logging
import matplotlib.pyplot as plt

yearToCalculate = 1961                 # Year (YYYY) in CE
longitude= 0                           # longitude of observation (-105.2705° for Boulder, 0° for Greenwich)
radiusOfPlate = 1                      # radius of the plate
plot_transparent_background = False    # set the background to transparent
plotGraphs = True                      # save plots

def determineApside(julian_time):
	# Define the line of apsides (longitude of aphelion and perihelion)
	apside_perihelion = 102.937348 + (1.7195269 * julian_time) + (0.00045962 * (julian_time**2)) + (0.000000499 * (julian_time**3))
	apside_aphelion = apside_perihelion + 180
	print(f"Perihelion = {apside_perihelion:3f}°")
	print(f"Aphelion   = {apside_aphelion:3f}°")
	return apside_perihelion, apside_aphelion

def determineEccentrictiyOverTime(julian_time):
	# Determine the change in eccentricity over time
	# James Morrison The Astrolabe (pg. 116)
	eccentricityAtJulianYear = 0.01670862 - (0.000042037 * julian_time) - (0.0000001236 * (julian_time**2)) + (0.00000000004 * (julian_time**3))
	#print(f"Eccentricity = {eccentricityAtJulianYear:6f}")
	# (see also: pg. 361)
	#eccentricityAtJulianYear = 0.016708617  - (0.000042037 * julian_time) - (0.000042037 * (julian_time**2)) + (0.00000000004 * (julian_time**3))
	#print(f"Eccentricity = {eccentricityAtJulianYear:6f}")
	return eccentricityAtJulianYear

def determineAngularDistanceEquinox(julian_time, given_longitude, given_aphelion):
	# Mean Anomaly of January 0
	
	# James Morrison The Astrolabe (pg. 361)
	mean_anomaly_jan0 = 357.52910 + (35999.0503 * julian_time) - (0.0001559 * (julian_time**2)) - (0.00000048 * (julian_time**3))
	mean_anomaly_jan0 = mean_anomaly_jan0 % 360 # keep anomaly within 0-360
	print(f"\nMorrison: Mean Anomaly of Jan 0 = {mean_anomaly_jan0:3f}°")
	
	# Astronomical Algorithms (Jean Meeus): "Sun's mean anomaly" (pg. 308) (Equation: 45.3)
	mean_anomaly_jan0 = 357.5291092 + (35999.0502909 * julian_time) - (0.0001536 * (julian_time**2)) - ((1/24490000) * (julian_time**3))
	mean_anomaly_jan0 = mean_anomaly_jan0 % 360 # keep anomaly within 0-360
	print(f"Meeus:    Mean Anomaly of Jan 0 = {mean_anomaly_jan0:3f}°")

	# Astronomical Algorithms (Jean Meeus): "Mean anomaly of the Sun (Earth)" (pg. 132)
	mean_anomaly_jan0 = 357.52772 + (35999.050340 * julian_time) - (0.0001603 * (julian_time**2)) - ((1/300000) * (julian_time**3))
	mean_anomaly_jan0 = mean_anomaly_jan0 % 360 # keep anomaly within 0-360
	print(f"Meeus     Mean Anomaly of Jan 0 = {mean_anomaly_jan0:3f}°\n")

	# Angular distane from vernal equinox to January 0 (midnight of Dec 31)
	ecliptic_long = np.mod(given_longitude - 180.0, 360.0) - 180.0
	print(f"Ecliptic longitude (λ) = {ecliptic_long}")
	angular_distance_equinox = (given_aphelion + mean_anomaly_jan0 + (given_longitude%360) / 365)
	# James Morrison The Astrolabe (pg. 117)
	# Jan 0 = perhelion + mean anomaly + eciplitic longitude / 365
	print("The angular distance from the vernal equinox to January 0 = π + M0 + λ / 365")
	print(f"({given_aphelion}° + {mean_anomaly_jan0}° + {abs(given_longitude)}°) / 365")
	angular_distance_equinox = angular_distance_equinox % 360
	angular_distance_equinox -= 360 # reversed from the original position
	print(f"Line of Apside relative to Vernal Equinox = {angular_distance_equinox}°\n")

	return angular_distance_equinox, mean_anomaly_jan0

def offsetfromCenterOfPlate(julian_time, radius_of_plate, given_perihelion):
	# offset from the center of the plate
	eccentricty = determineEccentrictiyOverTime(julian_time) # 0.01667061
	offset_eccentricity = 2 *  eccentricty * radius_of_plate # James Morrison The Astrolabe (pg. 117)
	x_delta = offset_eccentricity * math.cos(np.deg2rad(given_perihelion))
	y_delta = offset_eccentricity * math.sin(np.deg2rad(given_perihelion))
	print(f"Offset due to Eccentricity with radius of {radius_of_plate} = {offset_eccentricity:4f}")
	print(f"X offset with radius of {radius_of_plate} = {x_delta:4f}")
	print(f"Y offset with radius of {radius_of_plate} = {y_delta:4f}\n")
	return x_delta, y_delta

def plotEccentricityOverTime(offset_year):
	# change in eccentricity over time (time vs. eccentricity)
	fig = plt.figure(figsize=(10,10), dpi=100)
	ax = fig.subplots()
	x_year_range = np.arange(2000-offset_year, 2000+offset_year+1, 100)

	y_eccentricity = []
	for year in x_year_range:
		julian_time = (year - 2000) / 100 # Calculate the time in Julian centuries from J2000.0
		e = determineEccentrictiyOverTime(julian_time)
		y_eccentricity.append(e)

	plt.xticks(x_year_range, rotation=90)
	plt.yticks(np.linspace(min(y_eccentricity), max(y_eccentricity), 10))
	plt.title("Change in Year vs. Eccentricity", fontsize=15, weight='bold')
	plt.xlabel("Year (CE)", weight='bold')
	plt.ylabel("Eccentricity", weight='bold')
	plt.scatter(x_year_range, y_eccentricity, c="#C93924")
	plt.show()
	fig.savefig('calculate_eccentric_calendar_offset_outputs/eccentric_calendar_change_in_year_versus_eccentricity.png', dpi=fig.dpi, transparent=plot_transparent_background)

def plotYearToOffset(offset_year, year_to_calculate, radius_of_plate, given_longitude):
	# plot Year vs. Offset for fixed longitude (0°) for radius 1
	fig = plt.figure(figsize=(10,10), dpi=100)
	ax = fig.subplots()
	x_year_range = np.arange(2000-offset_year, 2000+offset_year+1, 100)

	y_offset_x = []
	y_offset_y = []
	for year in x_year_range:
		julian_time = (year - 2000) / 100 # Calculate the time in Julian centuries from J2000.0
		print(f"Julian Time in Centuries for the Year {year} = {julian_time}")
		offset_perihelion, offset_aphelion = determineApside(julian_time)
		vernal_equinox_angle, _ = determineAngularDistanceEquinox(julian_time, given_longitude, offset_aphelion)
		x_offset, y_offset = offsetfromCenterOfPlate(julian_time, radius_of_plate, offset_perihelion)
		y_offset_x.append(x_offset)
		y_offset_y.append(y_offset)

	plt.xticks(x_year_range, rotation=90)
	plt.yticks(np.linspace(max(y_offset_y), min(y_offset_x), 10))
	plt.title("Change in Year vs. Offset (X, Y) from Center of Plate", fontsize=15, weight='bold')
	plt.xlabel("Year (CE)", weight='bold')
	plt.ylabel(f"Offset with Fixed longitude (0°) and Radius ({radius_of_plate})", weight='bold')
	plt.scatter(x_year_range, y_offset_x, c="#C93924")
	plt.scatter(x_year_range, y_offset_y, c="#42617D")
	plt.legend(["X Offset", "Y Offset"])
	plt.show()
	fig.savefig('calculate_eccentric_calendar_offset_outputs/eccentric_calendar_change_in_year_versus_offset.png', dpi=fig.dpi, transparent=plot_transparent_background)

def plotLongitudeToAngularDistance(year_to_calculate):
	# plot Year vs. Longitude for fixed year (2024) for radius 1
	fig = plt.figure(figsize=(10,10), dpi=100)
	ax = fig.subplots()
	x_range_longitude = np.arange(-180, 180+1, 10)

	y_angular_distance_apside = []
	for x_longitude in x_range_longitude:
		julian_time = (year_to_calculate - 2000) / 100 # Calculate the time in Julian centuries from J2000.0
		print(f"Julian Time in Centuries for the Year {year_to_calculate} = {julian_time}")
		x_perihelion, x_aphelion = determineApside(julian_time)
		vernal_equinox_angle, _ = determineAngularDistanceEquinox(julian_time, x_longitude, x_aphelion)
		y_angular_distance_apside.append(vernal_equinox_angle)

	plt.xticks(x_range_longitude, rotation=90)
	plt.yticks(np.linspace(min(y_angular_distance_apside), max(y_angular_distance_apside), 10))
	plt.title("Change in Longitude vs. Angluar Distance to Vernal Equinox", fontsize=15, weight='bold')
	plt.xlabel("Longitude (°)", weight='bold')
	plt.ylabel(f"Vernal Equinox Angle (Apside) with Fixed Year ({year_to_calculate}) and Radius (1)", weight='bold')
	plt.scatter(x_range_longitude, y_angular_distance_apside, c="#C93924")
	plt.show()
	fig.savefig('calculate_eccentric_calendar_offset_outputs/eccentric_calendar_change_in_longitude_versus_angular_distance.png', dpi=fig.dpi, transparent=plot_transparent_background)
	
def plotMeanAnomaly(offset_year, year_to_calculate, radius_of_plate, given_longitude):
	# plot Year vs. Mean Anomaly for fixed longitude and for radius 1
	fig = plt.figure(figsize=(10,10), dpi=100)
	ax = fig.subplots()
	x_year_range = np.arange(1800, 2000+offset_year+1, 100)

	y_mean_anomaly = []
	for year in x_year_range:
		julian_time = (year - 2000) / 100 # Calculate the time in Julian centuries from J2000.0
		print(f"Julian Time in Centuries for the Year {year} = {julian_time}")
		x_perihelion, x_aphelion = determineApside(julian_time)
		_, mean_anomaly_jan0 = determineAngularDistanceEquinox(julian_time, given_longitude, x_aphelion)
		y_mean_anomaly.append(mean_anomaly_jan0)

	plt.xticks(x_year_range, rotation=90)
	plt.yticks(np.linspace(min(y_mean_anomaly), max(y_mean_anomaly), 10))
	plt.title("Change in Mean Anomaly on January 0 and Angular Distance to Vernal Equinox", fontsize=15, weight='bold')
	plt.xlabel("Year (CE)", weight='bold')
	plt.ylabel(f"Vernal Equinox Angle with Fixed Longitude ({given_longitude}) and Radius ({radius_of_plate})", weight='bold')
	plt.scatter(x_year_range, y_mean_anomaly, c="#C93924")
	plt.show()
	fig.savefig('calculate_eccentric_calendar_offset_outputs/eccentric_calendar_change_in_time_vs_mean_anomaly.png', dpi=fig.dpi, transparent=plot_transparent_background)

if __name__ == '__main__':
	# Calculate the time in Julian centuries from J2000.0 (example)
	julianTime = (yearToCalculate - 2000) / 100
	print(f"\nFor the Year {yearToCalculate} at longitude {longitude}° for a plate with a radius of {radiusOfPlate}")
	print(f"T = {julianTime:3f}")
	print(f"Eccentricity = {determineEccentrictiyOverTime(julianTime):6f}")
	print(f"Offset of calendar center = 2e = {2*determineEccentrictiyOverTime(julianTime):8f}")
	perihelion, aphelion = determineApside(julianTime)
	vernal_equinox_angle = determineAngularDistanceEquinox(julianTime, longitude, aphelion)
	x_offset, y_offset = offsetfromCenterOfPlate(julianTime, radiusOfPlate, perihelion)

	# Plot how the Longitude and Year change the Offset and Apside
	if plotGraphs:
		offset_year = 1000 # (+/-) x years
		plotEccentricityOverTime(offset_year)
		plotYearToOffset(offset_year, yearToCalculate, radiusOfPlate, longitude)
		plotLongitudeToAngularDistance(yearToCalculate)
		plotMeanAnomaly(offset_year, yearToCalculate, radiusOfPlate, longitude)
