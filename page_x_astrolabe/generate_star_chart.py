# Generate a star chart for astrolabe
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

if __name__ == '__main__':
	fig = plt.figure(figsize=(5, 5), dpi=120)
	gs = gridspec.GridSpec(1, 1)
	ax = plt.subplot(gs[0], polar=True)
	ax.set_ylim(-90, -55)

	# Set Right Ascension (astronomical 'longitude') as X
	angs = np.array([330, 345, 0, 15, 30, 45, 60, 75, 90, 105, 120,
					135, 150,  165, 180, 195, 210, 225, 240, 255,
					270, 285, 300, 315])
	plt.xticks(angs * np.pi / 180., fontsize=10)
	ax.set_xticklabels(['$22^h$', '$23^h$', '$0^h$', '$1^h$', '$2^h$',
						'$3^h$', '$4^h$', '$5^h$','$6^h$',
						'$7^h$',
						'$8^h$',
						'$9^h$',
						'$10^h$',
						'$11^h$',
						'$12^h$',
						'$13^h$',
						'$14^h$',
						'$15^h$',
						'$16^h$',
						'$17^h$',
						'$18^h$',
						'$19^h$',
						'$20^h$',
						'$21^h$'], fontsize=10)
	
	# Set Declination (astronomical 'latitude') as Y
	plt.yticks(np.arange(-80, -59, 10), fontsize=10)
	ax.set_rlabel_position(120)
	ax.set_yticklabels(['$-80^{\circ}$', '$-70^{\circ}$', '$-60^{\circ}$'],
		fontsize=10)
		
	plt.show()
