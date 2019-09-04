# Calculate the angular distance between two given stars (S1, S2)
import math # math.cos

def declinationinDecimalDegrees(star_declination):
	# convert declination from hours to degrees
	star_declination_split = star_declination.split('.')
	degrees = star_declination_split[0]
	is_negative_degree = False
	if '-' in degrees:
		is_negative_degree = True
		degrees = degrees.strip('-')
	arcminutes = star_declination_split[1][:2]
	arcseconds = star_declination_split[1][2:]

	converted_declination = float(degrees) + float(float(arcminutes)/60) + float(float(arcseconds)/3600)
	if is_negative_degree:
		converted_declination *= -1
	return converted_declination

def rightAscensioninDegrees(star_ra):
	# convert right ascension from hours to degrees
	star_ra_split = star_ra.split('.')
	hours = star_ra_split[0]
	minutes = star_ra_split[1][:2]
	seconds = star_ra_split[1][2:]

	converted_ra = float(hours) + float(float(minutes)/60) + float(float(seconds)/3600)
	return converted_ra

def calculateAngularDistance(s1_ra, s1_declination, s2_ra, s2_declination):
	# calculate angular distance between two stars
	cos_a =  math.sin(math.radians(s1_declination))*math.sin(math.radians(s2_declination))
	cos_a += math.cos(math.radians(s1_declination))*math.cos(math.radians(s2_declination))*math.cos(math.radians(15*(s1_ra - s2_ra)))
	print("cos(A) = {0}".format(cos_a))
	angular_distance = math.acos(cos_a)

	print("Angular Distance = {0} in radians".format(angular_distance))
	print("Angular Distance = {0} in degrees".format(math.degrees(angular_distance)))

if __name__ == '__main__':
	# Replace star with name and right ascension/declination
	# Properties of stars can be found: https://in-the-sky.org/
	s1 = "Megrez"
	s1_ra = '12.1525' # hours.minutesecond (HH.MMSS)
	s1_ra = rightAscensioninDegrees(s1_ra)
	s1_declination =  '57.0157' # degree.arcminutearcsecond (DD.MMSS)
	s1_declination = declinationinDecimalDegrees(s1_declination)
	print("{0}'s right ascension in decimal hours = {1}".format(s1, s1_ra))
	print("{0}'s declination in decimal degrees = {1}".format(s1, s1_declination))

	s2 = "Dubhe"
	s2_ra = '11.0343' # hours.minutesecond (HH.MMSS)
	s2_ra = rightAscensioninDegrees(s2_ra)
	s2_declination = '61.4504' # degree.arcminutearcsecond (DD.MMSS)
	s2_declination = declinationinDecimalDegrees(s2_declination)
	print("{0}'s right ascension in decimal hours = {1}".format(s2, s2_ra))
	print("{0}'s declination in decimal degrees = {1}".format(s2, s2_declination))

	print("\n")
	calculateAngularDistance(s1_ra, s1_declination, s2_ra, s2_declination)

	'''
	# ADDITIONAL EXAMPLE:
	s1 = "Mimosa"
	s1_ra = '12.4743' # hours.minutesecond (HH.MMSS)
	s1_ra = rightAscensioninDegrees(s1_ra)
	s1_declination =  '-59.4119' # degree.arcminutearcsecond (DD.MMSS)
	s1_declination = declinationinDecimalDegrees(s1_declination)
	print("{0}'s right ascension in decimal hours = {1}".format(s1, s1_ra))
	print("{0}'s declination in decimal degrees = {1}".format(s1, s1_declination))

	s2 = "Delta-Crucis"
	s2_ra = '12.1508' # hours.minutesecond (HH.MMSS)
	s2_ra = rightAscensioninDegrees(s2_ra)
	s2_declination = '-58.4456' # degree.arcminutearcsecond (DD.MMSS)
	s2_declination = declinationinDecimalDegrees(s2_declination)
	print("{0}'s right ascension in decimal hours = {1}".format(s2, s2_ra))
	print("{0}'s declination in decimal degrees = {1}".format(s2, s2_declination))

	print("\n")
	calculateAngularDistance(s1_ra, s1_declination, s2_ra, s2_declination)
	'''
