# temporary fix to run python2.7 code for vondrak plugin for precession
# Python Implementation of "New precession expressions, valid for long time intervals" (J. Vondrak, N. Capitaine, and P. Wallace) (2011)
import argparse
import sys

if __name__ == '__main__':
	# file run: python2.7 return_ra_dec_precession_python27.py -S star_name
	parser = argparse.ArgumentParser(description="flag format given as: -S star_name")
	parser.add_argument('-S', '-star-name', help="star name to find precession movement")
	args = parser.parse_args()

	if args.S is None:
		print("ERROR: Include a star name to compute\n")
		exit()
	else:
		star_name = args.S

	print("Compute Precession for '{0}' using Python {1}.{2} for Vondrak Plugin".format(star_name, sys.version_info[0], sys.version_info[1]))
