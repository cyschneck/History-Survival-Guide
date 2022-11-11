# Calculate the Offset and Angular Distance of the Eccentric Calendar for the Back of the Astrolabe
# python3 calculate_eccentric_calendar_offset.py: Python 3.7.3
# Based on James Morrison's 'Astrolabe' pg. 116
import math
import numpy as np
import configparser
import matplotlib.pyplot as plt

def determineApside(julian_time):
	# Define the line of apsides (longitude of aphelion and perihelion)
	apside_perihelion = 102.937348 + (1.7195269 * julian_time) + (0.00045962 * (julian_time**2)) + (0.000000499 * (julian_time**3))
	apside_aphelion = apside_perihelion + 180
	print("Perihelion = {0:3f}°".format(apside_perihelion))
	print("Aphelion   = {0:3f}°".format(apside_aphelion))
	return apside_perihelion, apside_aphelion

def determineEccentrictiyOverTime(julian_time):
	# Determine the change in eccentricity over time
	eccentricityAtJulianYear = 0.01670862 - (0.000042037 * julian_time) - (0.0000001236 * (julian_time**2)) + (0.00000000004 * (julian_time**3))
	return eccentricityAtJulianYear

def determineAngularDistanceEquinox(julian_time, given_longitude, given_aphelion):
	# Mean Anomaly of January 0
	mean_anomaly_jan0 = 357.52910 + (35999.0503 * julian_time) - (0.0001559 * (julian_time**2)) - (0.00000048 * (julian_time**3))
	mean_anomaly_jan0 = mean_anomaly_jan0 % 360 # keep anomaly within 0-360
	print("Mean Anomaly of Jan 0 = {0:3f}°".format(mean_anomaly_jan0))

	# Angular distane from vernal equinox to January 0 (midnight of Dec 31)
	angular_distance_equinox = given_aphelion + mean_anomaly_jan0 + (given_longitude / 365)
	angular_distance_equinox = angular_distance_equinox % 360
	angular_distance_equinox -= 360 # reversed from the original position
	print("\nLine of Apside relative to Vernal Equinox for Longitude {0}° = {1}°".format(given_longitude, angular_distance_equinox))

	return angular_distance_equinox

def offsetfromCenterOfPlate(julian_time, radius_of_plate, given_perihelion):
	# offset from the center of the plate
	eccentricty = determineEccentrictiyOverTime(julian_time) # 0.01667061
	offset_eccentricity = 2 *  eccentricty * radius_of_plate
	x_delta = offset_eccentricity * math.cos(np.deg2rad(given_perihelion))
	y_delta = offset_eccentricity * math.sin(np.deg2rad(given_perihelion))
	print("Offset due to Eccentricity with radius of {0} = {1:4f}".format(radius_of_plate, offset_eccentricity))
	print("X offset with radius of {0} = {1:4f}".format(radius_of_plate, x_delta))
	print("Y offset with radius of {0} = {1:4f}\n".format(radius_of_plate, y_delta))
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
	plt.title("Change in Year vs. Eccentricity")
	plt.xlabel("Year (CE)")
	plt.ylabel("Eccentricity")
	plt.scatter(x_year_range, y_eccentricity)
	plt.show()
	fig.savefig('{0}/eccentric_calendar_change_in_year_versus_eccentricity.png'.format("calculate_eccentric_calendar_offset_outputs"), dpi=fig.dpi)

def plotYearToOffset(offset_year, year_to_calculate, radius_of_plate, given_longitude):
	# plot Year vs. Offset for fixed longitude (0°) for radius 1
	fig = plt.figure(figsize=(10,10), dpi=100)
	ax = fig.subplots()
	x_year_range = np.arange(2000-offset_year, 2000+offset_year+1, 100)

	y_offset_x = []
	y_offset_y = []
	for year in x_year_range:
		julian_time = (year - 2000) / 100 # Calculate the time in Julian centuries from J2000.0
		print("Julian Time in Centuries for the Year {0} = {1}".format(year, julian_time))
		offset_perihelion, offset_aphelion = determineApside(julian_time)
		vernal_equinox_angle = determineAngularDistanceEquinox(julian_time, given_longitude, offset_aphelion)
		x_offset, y_offset = offsetfromCenterOfPlate(julian_time, radius_of_plate, offset_perihelion)
		y_offset_x.append(x_offset)
		y_offset_y.append(y_offset)

	plt.xticks(x_year_range, rotation=90)
	plt.title("Change in Year vs. Offset (X, Y) from Center of Plate")
	plt.xlabel("Year (CE)")
	plt.ylabel("Offset with Fixed longitude (0°) and Radius (1)")
	plt.scatter(x_year_range, y_offset_x)
	plt.scatter(x_year_range, y_offset_y)
	plt.legend(["X Offset", "Y Offset"])
	plt.show()
	fig.savefig('{0}/eccentric_calendar_change_in_year_versus_offset.png'.format("calculate_eccentric_calendar_offset_outputs"), dpi=fig.dpi)

def plotLongitudeToAngularDistance(year_to_calculate):
	# plot Year vs. Longitude for fixed year (2022) for radius 1
	fig = plt.figure(figsize=(10,10), dpi=100)
	ax = fig.subplots()
	x_range_longitude = np.arange(-180, 180+1, 10)

	y_angular_distance_apside = []
	for x_longitude in x_range_longitude:
		julian_time = (2022 - 2000) / 100 # Calculate the time in Julian centuries from J2000.0
		print("Julian Time in Centuries for the Year {0} = {1}".format(year_to_calculate, julian_time))
		x_perihelion, x_aphelion = determineApside(julian_time)
		vernal_equinox_angle = determineAngularDistanceEquinox(julian_time, x_longitude, x_aphelion)
		y_angular_distance_apside.append(vernal_equinox_angle)

	plt.xticks(x_range_longitude, rotation=90)
	plt.title("Change in Longitude vs. Angluar Distance to Vernal Equinox")
	plt.xlabel("Longitude (°)")
	plt.ylabel("Vernal Equinox Angle (Apside) with Fixed Year (2022) and Radius (1)")
	plt.scatter(x_range_longitude, y_angular_distance_apside)
	plt.show()
	fig.savefig('{0}/eccentric_calendar_change_in_longitude_versus_angular_distance.png'.format("calculate_eccentric_calendar_offset_outputs"), dpi=fig.dpi)

if __name__ == '__main__':
	config = configparser.ConfigParser()
	config.read("config.ini")
	yearToCalculate = int(config["calculateEccentricCalendarOffset"]["yearToCalculate"]) # Year (YYYY) in CE
	longitude = float(config["calculateEccentricCalendarOffset"]["longitude"]) # longitude of observation (-105.2705° for Boulder, 0° for Greenwich)
	radiusOfPlate = float(config["calculateEccentricCalendarOffset"]["radiusOfPlate"]) 
	plotGraphs = True

	# Calculate the time in Julian centuries from J2000.0
	julianTime = (yearToCalculate - 2000) / 100
	perihelion, aphelion = determineApside(julianTime)
	vernal_equinox_angle = determineAngularDistanceEquinox(julianTime, longitude, aphelion)
	x_offset, y_offset = offsetfromCenterOfPlate(julianTime, radiusOfPlate, perihelion)

	# Plot how the Longitude and Year change the Offset and Apside
	if plotGraphs:
		offset_year = 1000 # (+/-) x years
		plotEccentricityOverTime(offset_year)
		plotYearToOffset(offset_year, yearToCalculate, radiusOfPlate, longitude)
		plotLongitudeToAngularDistance(yearToCalculate)
