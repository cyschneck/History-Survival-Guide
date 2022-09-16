# Calculate the Offset and Angular Distance of the Eccentric Calendar for the Back of the Astrolabe
# python3 calculate_eccentric_calendar_offset.py
# Based on James Morrison's 'Astrolabe'
import math
import numpy as np
import matplotlib.pyplot as plt

def determineApside(julianTime):
	# Define the line of apsides (longitude of aphelion and perihelion)
	perihelion = 102.937348 + (1.7195269*julianTime) + (0.00045962 * (julianTime**2)) + (0.000000499 * (julianTime**3))
	aphelion = perihelion + 180
	print("\nPerihelion = {0:3f}°".format(perihelion))
	print("Aphelion   = {0:3f}°".format(aphelion))

	return perihelion, aphelion

def determineAngularDistanceEquinox(julianTime, longitude, aphelion):
	# Mean Anomaly of January 0
	mean_anomaly_jan0 = 357.52910 + (35999.0503 * julianTime) - (0.0001559 * (julianTime**2)) - (0.00000048 * (julianTime**3))
	mean_anomaly_jan0 = mean_anomaly_jan0 % 360 # keep anomaly within 0-360
	print("Mean Anomaly of Jan 0 = {0:3f}°".format(mean_anomaly_jan0))

	# Angular distane from vernal equinox to January 0 (midnight of Dec 31)
	angular_distance_equinox = aphelion + mean_anomaly_jan0 + (longitude / 365)
	angular_distance_equinox = angular_distance_equinox % 360
	angular_distance_equinox -= 360 # reversed from the original position
	print("\nLine of Apside relative to Vernal Equinox for Longitude {0}° = {1}°".format(longitude, angular_distance_equinox))

	return angular_distance_equinox

def offsetfromCenterOfPlate(radiusOfPlate, perihelion):
	# offset from the center of the plate
	eccentricty = 0.01667061
	offset_eccentricity = 2 *  eccentricty * radiusOfPlate
	x_delta = offset_eccentricity * math.cos(np.deg2rad(perihelion))
	y_delta = offset_eccentricity * math.sin(np.deg2rad(perihelion))
	print("\nX offset with radius of {0} = {1:4f}".format(radius_of_plate, x_delta))
	print("Y offset with radius of {0} = {1:4f}".format(radius_of_plate, y_delta))

	return x_delta, y_delta

def plotYearToOffset():
	# plot Year vs. Offset for fixed longitude (0°) for radius 1
	fig = plt.figure(figsize=(10,10), dpi=100)
	ax = fig.subplots()
	offset_year = 1000 # (+/-) x years
	x_year_range = np.arange(2000-offset_year, 2000+offset_year+1, 10)

	y_offset_x = []
	y_offset_y = []
	for year in x_year_range:
		julianTime = (year - 2000) / 100 # Calculate the time in Julian centuries from J2000.0
		print("Julian Time in Centuries for the Year {0} = {1}".format(yearToCalculate, julianTime))
		perihelion, aphelion = determineApside(julianTime)
		vernal_equinox_angle = determineAngularDistanceEquinox(julianTime, longitude, aphelion)
		x_offset, y_offset = offsetfromCenterOfPlate(radius_of_plate, perihelion)
		y_offset_x.append(x_offset)
		y_offset_y.append(y_offset)

	plt.xticks(x_year_range)
	plt.title("Offset vs. Year")
	plt.xlabel("Year")
	plt.ylabel("Offset for fixed longitude (0°) for radius 1")
	plt.scatter(x_year_range, y_offset_x)
	plt.scatter(x_year_range, y_offset_y)
	plt.legend(["X Offset", "Y Offset"])
	plt.show()

def plotLongitudeToAngularDistance():
	# plot Year vs. Longitude for fixed year (2022) for radius 1
	fig = plt.figure(figsize=(10,10), dpi=100)
	ax = fig.subplots()
	x_longitude = np.arange(-180, 180+1, 10)

	y_angular_distance_apside = []
	for longitude in x_longitude:
		julianTime = (2022 - 2000) / 100 # Calculate the time in Julian centuries from J2000.0
		print("Julian Time in Centuries for the Year {0} = {1}".format(yearToCalculate, julianTime))
		perihelion, aphelion = determineApside(julianTime)
		vernal_equinox_angle = determineAngularDistanceEquinox(julianTime, longitude, aphelion)
		y_angular_distance_apside.append(vernal_equinox_angle)

	plt.xticks(x_longitude)
	plt.title("Longitude vs. Angluar Distance to Vernal Equinox")
	plt.xlabel("Longitude")
	plt.ylabel("Vernal Equinox Angle (Apside) for fixed year (2022) for radius 1")
	plt.scatter(x_longitude, y_angular_distance_apside)
	plt.show()

if __name__ == '__main__':
	yearToCalculate = 2022
	longitude = 105.2705 # 105.2705° for Boulder
	radius_of_plate = 1
	plotGraphs = True

	# Calculate the time in Julian centuries from J2000.0
	julianTime = (yearToCalculate - 2000) / 100
	perihelion, aphelion = determineApside(julianTime)
	vernal_equinox_angle = determineAngularDistanceEquinox(julianTime, longitude, aphelion)
	x_offset, y_offset = offsetfromCenterOfPlate(radius_of_plate, perihelion)

	if plotGraphs:
		plotYearToOffset()
		plotLongitudeToAngularDistance()