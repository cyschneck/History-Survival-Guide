# git clone https://github.com/digitalvapor/vondrak
# python3 vondrak/setup.py install
# python2.7 -m pip install ephem
# python2.7 -m pip install basemap
# Python Implementation of "New precession expressions, valid for long time intervals" (J. Vondrak, N. Capitaine, and P. Wallace) (2011)
# python2.7 test_prcession.py

import math
import numpy as np
import vondrak as v
import matplotlib.pyplot as plt
import ephem
from math import cos, sin
from ephem import hours as hrs
from ephem import degrees as deg

def periodicity():
	ecl_p_matrix_list_x = []
	ecl_p_matrix_list_y = []
	ecl_p_matrix_list_z = []
	equ_p_matrix_list_x = []
	equ_p_matrix_list_y = []
	equ_p_matrix_list_z = []
	year = np.arange(-200001.0, 200000.0, 100)
	for y in year:
		p_ecl = v.ltp_pecl(y)
		p_equ = v.ltp_pequ(y)
		ecl_p_matrix_list_x.append(p_ecl[0])
		ecl_p_matrix_list_y.append(p_ecl[1])
		ecl_p_matrix_list_z.append(p_ecl[2])
		equ_p_matrix_list_x.append(p_equ[0])
		equ_p_matrix_list_y.append(p_equ[1])
		equ_p_matrix_list_z.append(p_equ[2])

	fig = plt.figure(figsize=(12,12), dpi=100)
	plt.title("Ecliptic Components of Matrix over 400K Years")
	plt.plot(year, ecl_p_matrix_list_x)
	plt.plot(year, ecl_p_matrix_list_y)
	plt.plot(year, ecl_p_matrix_list_z)
	plt.xticks(rotation=90)
	plt.show()
	fig = plt.figure(figsize=(12,12), dpi=100)
	plt.title("Equatorial Components of Matrix over 400K Years")
	plt.plot(year, equ_p_matrix_list_x)
	plt.plot(year, equ_p_matrix_list_y)
	plt.plot(year, equ_p_matrix_list_z)
	plt.xticks(rotation=90)
	plt.show()


def position_matrix(ra=None, dec=None, x=None, y=None, z=None):
	if(ra == None or dec == None):
		ra  = 0.0
		dec = 0.0
	if(x==None or y ==None or z==None):
		x = cos(dec) * cos(ra)
		y = cos(dec) * sin(ra)
		z = sin(dec)
	return np.array([[x], [y], [z]])

def compute_star(year, star_name):
	import ephem
	given_star = ephem.star(star_name)
	given_star.compute(str(year),epoch='2000')
	ra = given_star.a_ra
	dec = given_star.a_dec
	return position_matrix(ra=ra,dec=dec)
   
def testingStar(star_name):
	p0 = compute_star(2000, star_name)
	(ra, dec) = v.ra_dec(p0)
	print("{0} in 2000".format(star_name))
	print('RA: {}'.format(hrs(ra)))
	print('DEC: {}'.format(deg(dec)))
	print('cartesian position of {0} in the year=2000, epoch=2000:'.format(star_name))
	x = p0[0][0]
	y = p0[1][0]
	z = p0[2][0]
	print('{}\nthis vector has length {}'.format(
		  (x,y,z),math.sqrt(x*x + y*y + z*z)))

	print("\nComputing:")
	p0 = compute_star(2000, star_name)
	print('The position of {0} at J2000 is \n{1}'.format(star_name, p0))
	epj = 15000
	P = v.ltp_pbmat(epj) # Precession matrix, GCRS
	p1 = compute_star(epj, star_name)
	p1 = v.pdp(P, p1)
	print('The new position of {0} in {1} years is \n{2}'.format(star_name, epj, p1))

	print("\n")
	(ra, dec) = v.ra_dec(p0)
	print('In hours of right ascension and degrees of declination')
	print('The position of {0} at J2000 is'.format(star_name))
	print(str(hrs(ra)),str(deg(dec)))
	print('The new position of {0} at {1} years is'.format(star_name, epj))
	(ra1, dec1) = v.ra_dec(p1)
	print(str(hrs(ra1)),str(deg(dec1)))

def graphOverTime(star_name):
	range_year = 13500 # full cycle = 26,000 
	years = np.arange(-range_year, range_year+1, 10)
	dec_list = []
	for year in years:
		P = v.ltp_pbmat(year) # Precession matrix for the given year
		p_1 = compute_star(year, star_name) # compute star's position matrix for given year
		p_1 = v.pdp(P, p_1) # apply precession matrix for given year
		(ra1, dec1) = v.ra_dec(p_1)
		as_deg = float(".".join(str(deg(dec1)).split(":")[:2]))
		dec_list.append(as_deg)
	
	fig = plt.figure(figsize=(12,12), dpi=100)
	ax = fig.subplots()
	plt.title("{0}'s Declination Due to Precession".format(star_name))
	plt.plot(years, dec_list)
	plt.axvline(2022, linewidth=0.5, color="black", linestyle="dashed")
	plt.text(x=2022+100, y=min(dec_list)+10, s="Year 2022", fontsize=10, rotation=90) # add label on figure
	plt.xlabel("Year (B.C.E)")
	plt.ylabel("Declination (Degrees)")
	ax.set_xticks(np.arange(years[0], years[-1]+1, 1000))
	ax.set_yticks(np.arange(min(dec_list), max(dec_list)+1, 3))
	plt.xticks(rotation=90)
	plt.show()
	fig.savefig('test_precession_vondrak_example.png', dpi=fig.dpi)

if __name__ == '__main__':
	star_name = "Vega"
	testingStar(star_name)
	graphOverTime(star_name)
