import numpy as np
import math
import matplotlib.pyplot as plt

def eot_gen(e, p_degs, axis_norm_degs, peri_day, orb_per, day_nums):
	eot_mins = []
	time_mins = (24 * 60) / (2 * math.pi)
	p = np.deg2rad(p_degs)
	axis_norm_rads = np.deg2rad(axis_norm_degs)
	t1 = (axis_norm_rads/2)*(1-4*pow(e, 2))
	tan2_1_4e2 = (1-math.cos(2*t1)) / (1+math.cos(2*t1))
	tan2 = (1-math.cos(axis_norm_rads)) / (1+math.cos(axis_norm_rads))
	e2 = 2*e
	tan2_2e = 2*e*tan2
	tan4_1_2 = (1/2)*pow(tan2, 2)
	e2_5_4 = (5/4)*(pow(e, 2))
	tan4_2e = 2*e*pow(tan2, 2)
	tan2_2e_13_4 = (13/4)*(pow(e, 2))*tan2
	tan6_1_3 = (1/3)*pow(tan2, 3)
	for d in day_nums:
		m = 2*math.pi*((d - peri_day)/orb_per)
		eot_mins.append(-(tan2_1_4e2*math.sin(2*(m+p))+e2*math.sin(m) -
						tan2_2e*math.sin(m+2*p)+tan2_2e*math.sin(3*m+2*p) +
						tan4_1_2*math.sin(4*(m+p))+e2_5_4*math.sin(2*m)-tan4_2e*math.sin((3*m)+(4*p)) +
						tan4_2e*math.sin((5*m)+(4*p))+tan2_2e_13_4*math.sin(4*m+2*p) +
						tan6_1_3*math.sin(6*(m+p)))*time_mins)
	return eot_mins

def ecc_gen(e, p, peri_day, orb_per, day_nums):
	return eot_gen(e, p, 0, peri_day, orb_per, day_nums)

def obl_gen(p, axis_norm_rads, peri_day, orb_per, day_nums):
	return eot_gen(0, p, axis_norm_rads, peri_day, orb_per, day_nums)

if __name__ == '__main__':
	day_nums = np.arange(1.5, 366.5, 1)  # base calculation on noon UT of day
	e = 0.01671022              # earth orbit eccentricity
	p_degs = 14.40              # angle covered by the Earth between the begnning of Winer (21st December) and the arrival of the Earth at perihelion (2nd January)
	axis_norm_degs = 23.4367    # obliquity: angle between the axis and the norm of the orbit
	peri_day = 5.325            # calendar day in January of perihelion (~3-5) (decimal/fractional format)
	orb_per = 365.25696         # earth orbital period

	#print("day_nums = {0}".format(day_nums))
	eot_y = eot_gen(e, p_degs, axis_norm_degs, peri_day, orb_per, day_nums)
	#print("eot_y = {0}".format(eot_y))

	obl_y = obl_gen(p_degs, axis_norm_degs, peri_day, orb_per, day_nums)
	#print("obl_y = {0}".format(obl_y))
	plt.scatter(day_nums, obl_y)
	plt.show()

	ecc_y = ecc_gen(e, p_degs, peri_day, orb_per, day_nums)
	#print("ecc_y = {0}".format(ecc_y))
	plt.scatter(day_nums, ecc_y)
	plt.show()
