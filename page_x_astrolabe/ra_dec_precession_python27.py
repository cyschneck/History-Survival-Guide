# temporary fix to run python2.7 code for vondrak plugin for precession
# Python Implementation of "New precession expressions, valid for long time intervals" (J. Vondrak, N. Capitaine, and P. Wallace) (2011)
# python2.7 ra_dec_precession_python27.py -S Polaris -Y 1400
import argparse
import sys
import numpy as np
import math
import ephem
import vondrak

def position_matrix(ra=None, dec=None, x=None, y=None, z=None):
	if(ra == None or dec == None):
		ra  = 0.0
		dec = 0.0
	if(x==None or y ==None or z==None):
		x = math.cos(dec) * math.cos(ra)
		y = math.cos(dec) * math.sin(ra)
		z = math.sin(dec)
	return np.array([[x], [y], [z]])

def compute_star(year, star_name):
	import ephem
	given_star = ephem.star(star_name)
	given_star.compute(str(year),epoch='2000')
	ra = given_star.a_ra
	dec = given_star.a_dec
	return position_matrix(ra=ra,dec=dec)

if __name__ == '__main__':
	# file run: python2.7 return_ra_dec_precession_python27.py -S star_name
	parser = argparse.ArgumentParser(description="flag format given as: -S star_name")
	parser.add_argument('-S', '-star-name', help="star name to find precession movement")
	parser.add_argument('-Y', '-year-to-calculate', type=int, help="year to calculate for star's position")
	args = parser.parse_args()

	if args.S is None:
		print("ERROR: Include a star name to compute\n")
		exit()
	else:
		star_name = args.S
		if "-" in star_name: star_name = " ".join(star_name.split("-"))
	if args.Y is None:
		print("ERROR: Include a star year to compute\n")
		exit()
	else:
		year_to_calculate = args.Y

	try:
		P = vondrak.ltp_pbmat(year_to_calculate) # Precession matrix for the given year
		p_1 = compute_star(year_to_calculate, star_name) # compute star's position matrix for given year
		p_1 = vondrak.pdp(P, p_1) # apply precession matrix for given year
		(ra1, dec1) = vondrak.ra_dec(p_1)
		dec_as_deg = float(".".join(str(ephem.degrees(dec1)).split(":")[:2]))
		ra1_as_str = str(ephem.hours(ra1)).split(".")[0]
		ra1_as_str = ".".join(ra1_as_str.split(":"))
		"""print("Compute Precession for '{0}' in the year {1} using Python {2}.{3} for Vondrak Plugin".format(star_name, 
																										year_to_calculate,
																										sys.version_info[0],
																										sys.version_info[1]))
		"""
		print("{0},{1}".format(dec_as_deg, ra1_as_str)) # new declination and right ascension
	except KeyError as e:
		# Star Name not found
		print("{0} not found".format(star_name)) # do not add star name to list
