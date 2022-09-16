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

def determineAngularDistanceEquinox(YYYY, longitude, aphelion):
	# Mean Anomaly of January 0
	mean_anomaly_jan0 = 357.52910 + (35999.0503 * julianTime) - (0.0001559 * (julianTime**2)) - (0.00000048 * (julianTime**3))
	mean_anomaly_jan0 = mean_anomaly_jan0 % 360 # keep anomaly within 0-360
	print("Mean Anomaly of Jan 0 = {0:3f}°".format(mean_anomaly_jan0))

	# Angular distane from vernal equinox to January 0 (midnight of Dec 31)
	angular_distance_equinox = aphelion + mean_anomaly_jan0 + (longitude / 365)
	angular_distance_equinox = angular_distance_equinox % 360
	angular_distance_equinox -= 360 # reversed from the original position
	print("\nLine of Apside relative to Vernal Equinox = {0:3f}°".format(angular_distance_equinox))

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

if __name__ == '__main__':
	yearToCalculate = 2022
	longitude = 105.2705 # 105.2705° for Boulder
	radius_of_plate = 1

	# Calculate the time in Julian centuries from J2000.0
	julianTime = (yearToCalculate - 2000) / 100
	print("Julian Time in Centuries for the Year {0} = {1}".format(yearToCalculate, julianTime))

	perihelion, aphelion = determineApside(julianTime)
	vernal_equinox_angle = determineAngularDistanceEquinox(yearToCalculate, longitude, aphelion)
	x_offset, y_offset = offsetfromCenterOfPlate(radius_of_plate, perihelion)
