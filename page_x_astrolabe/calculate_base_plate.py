# python3 calculate_base_plate.py: Python 3.7.3
import numpy as np

if __name__ == '__main__':
	# Find Ratio between concentric circles for base plate based on obliquity
	obliquity_range = np.arange(0, 360+1, 5)
	print(obliquity_range)
