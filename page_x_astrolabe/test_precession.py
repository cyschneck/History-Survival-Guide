# Precession: http://slittlefair.staff.shef.ac.uk/teaching/phy115/session2/moreCel/moreCel.html
# python3 test_prcession.py
import math
import numpy as np

def timeSince2000(yearToCalculate):
	since2000 = (yearToCalculate - 2000) / 100
	print("{0} year = T = {1}".format(yearToCalculate, since2000))
	return since2000

def changeRaAndDec(T, original_declination, original_RA):
	M_radian = np.deg2rad((1.2812323 * T) + (0.0003879 * (T**2)) + (0.0000101 * (T**3)))
	N_radian = np.deg2rad((0.5567530 * T) - (0.0001185 * (T**2)) + (0.0000116 * (T**3)))
	#print("\nM = {0}".format(M))
	#print("N = {0}".format(N))

	print("\nOriginal Declination = {0}".format(original_declination))

	ra_in_hr = original_RA
	# convert RA from hours to degrees
	ra_hr, ra_min, ra_sec = list(map(int, ra_in_hr.split('.')))
	ra_min /= 60
	ra_sec /= 3600
	ra_total = ra_hr + ra_min + ra_sec
	ra_in_degrees = ra_total * 15
	print("Original RA = {0:4f}".format(ra_in_degrees))
	# convert RA from degrees to radians
	ra_in_radians = np.deg2rad(ra_in_degrees)

	change_declination = N_radian * math.cos(ra_in_radians) # radians
	change_ra = M_radian + ((N_radian * math.sin(ra_in_radians)) * math.tan(np.deg2rad(original_declination))) # radians

	new_declination_degree = np.rad2deg(change_declination) + original_declination
	new_ra_degree = np.rad2deg(change_ra) + ra_in_degrees

	print("\nChange in Declination = {0:04f} degrees".format(np.rad2deg(change_declination)))
	print("New Declination = {0:04f} degrees".format(new_declination_degree))
	print("Change in RA = {0:04f} degrees".format(change_ra))
	print("New RA = {0:04f} degrees\n".format(new_ra_degree))
	return new_declination_degree, new_ra_degree

if __name__ == '__main__':
	# testing:
	currentYear = 2022
	convertedTime = timeSince2000(currentYear)
	vega_dec = 38.47 # vega_declination 
	vega_ra = "18.36.56" # vega_ra
	#new_dec_degree, new_ra_degree = changeRaAndDec(convertedTime, vega_dec, vega_ra)

	# graph:
	import matplotlib.pyplot as plt
	x_change_time = np.arange(2000-2000, 2000+2000+1, 100)
	y_dec = []
	y_ra = []
	for year in x_change_time:
		T = timeSince2000(year)
		new_dec, new_ra = changeRaAndDec(T, vega_dec, vega_ra)
		y_dec.append(new_dec)
		y_ra.append(new_ra)

	plt.title("New Declination over Time")
	plt.scatter(x_change_time, y_dec)
	plt.ylabel("New Declination (degree)")
	plt.show()

	plt.title("New RA over Time")
	plt.scatter(x_change_time, y_ra)
	plt.ylabel("New RA (degree)")
	plt.show()
