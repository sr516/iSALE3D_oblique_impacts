########################################################################
# Author: S.D. Raducan
# Date: 2021
# Description: Python script to plot ejecta angle vs launch position, for azimuth segments
########################################################################
import pySALEPlot as psp
import matplotlib.pyplot as plt
import numpy as np
import math as m
import scipy.integrate as integrate
from matplotlib import colors

# Set up a pyplot figure 
fig, ((ax1_1, ax1_2, ax1_3), (ax2_1, ax2_2, ax2_3), (ax3_1, ax3_2, ax3_3), (ax4_1, ax4_2, ax4_3), (ax5_1, ax5_2, ax5_3), (ax6_1, ax6_2, ax6_3)) = plt.subplots(nrows=6, ncols=3,  figsize=(9.5,12.), sharex = True, sharey = True)


# Set up the subplot axes.
fig.subplots_adjust(left=0.08, right=0.98, bottom=0.045, top = 0.98, wspace=0.0, hspace = 0.0)

axs = [ax1_1, ax1_2, ax1_3, ax2_1, ax2_2, ax2_3, ax3_1, ax3_2, ax3_3, ax4_1, ax4_2, ax4_3, ax5_1, ax5_2, ax5_3, ax6_1, ax6_2, ax6_3]

########################################################################

def cc(cc):
	return plt.cm.viridis(cc)


#Define constants
rho = 2120.
delta = 1000.
a = 0.42
m = 4./3.*np.pi*delta*a**3.

radius = 11.5 
U = np.array([7e3, 7e3*(3.)**(1./2.)/2., 7e3*(2.)**(1./2.)/2., 7e3/2.])

col = [0., 0.3, 0.55, 0.9]

# Define azimuth segments
i_max1 = np.array(range(5, 95, 5))
i_min1 = np.array(range(0, 90, 5))

i_max2 = i_max1 + 90 
i_min2 = i_min1+ 90 

i_max = np.concatenate((i_max1, i_max2), axis=0)
i_min = np.concatenate((i_min1, i_min2), axis=0)

datafiles = ['ejecta_90.txt', 'ejecta_60.txt', 'ejecta_45.txt', 'ejecta_30.txt']

label_name = [r'$\theta$ = 90$^\circ$', r'$\theta$ = 60$^\circ$', r'$\theta$ = 45$^\circ$', r'$\theta$ = 30$^\circ$']


for h in range(0, 4, 1):
	# Read data
	xx = np.loadtxt(datafiles[h])
	i = 0
	mu_list = []
	c1_list = []
	rad_list = []
	
	
	azimuth, x_proj = xx[0, :], xx[1, :] 
	vel_z, vel_x = xx[2, :], xx[3, :]
	vel_ej = vel_z
	
	
	# Filter uprange & downrange ejecta
	for i in range(0, 18, 1):
		if h ==0:
			print (i_min[i], i_max[i])
		
		# Add thresholds	
		vel_y2, vel_x2 = vel_y[azimuth>=(i_min[i])], vel_x[azimuth>=(i_min[i])]
		x_proj2, vel_ej2, azimuth2= x_proj[azimuth>=(i_min[i])], vel_ej[azimuth>=(i_min[i])], azimuth[azimuth>=(i_min[i])]
		x_proj2, vel_ej2= x_proj2[azimuth2<(i_max[i])], vel_ej2[azimuth2<(i_max[i])] 
		
		
		vel_y2, vel_x2 = vel_y2[azimuth2<(i_max[i])], vel_x2[azimuth2<(i_max[i])]
	
		j = i
		theta =  np.degrees(np.arctan((vel_y2/vel_x2)))

		x_proj22, theta2 = x_proj2[vel_ej2>0.04*np.max(vel_ej2)], theta[[vel_ej2>0.04*np.max(vel_ej2)]]

		# Plot data
		axs[j].scatter(x_proj22/a, theta2, s = vel_ej22*5.0, edgecolors='none', marker='.', facecolors = cc(h/3.), rasterized = True, linewidth = None )


az_label = [r'$\zeta=$0-5$^o$', r'$\zeta=$5-10$^o$', r'$\zeta=$10-15$^o$', r'$\zeta=$15-20$^o$', r'$\zeta=$20-25$^o$', r'$\zeta=$25-30$^o$', r'$\zeta=$30-35$^o$', r'$\zeta=$35-40$^o$', r'$\zeta=$40-45$^o$', r'$\zeta=$45-50$^o$', r'$\zeta=$50-55$^o$', r'$\zeta=$55-60$^o$', r'$\zeta=$60-65$^o$', r'$\zeta=$65-70$^o$', r'$\zeta=$70-75$^o$', r'$\zeta=$75-80$^o$', r'$\zeta=$80-85$^o$', r'$\zeta=$85-90$^o$']

l=0
for ax in axs:
	ax.set_xscale('log')
	ax.set_xlim([1.2, 29.])
	ax.set_ylim([15, 60])
	ax.grid(linewidth = 0.5)
	
	ax.annotate(az_label[l], xy=(8.0, 55),fontsize = 10., rotation=0)
	l+=1
	
# Axes legends
ax1_1.legend(loc=3, fontsize = 9.0)


# Set axes labels
ax1_1.set_ylabel(r'Ejection angle [$^\circ$]')
ax2_1.set_ylabel(r'Ejection angle [$^\circ$]')
ax3_1.set_ylabel(r'Ejection angle [$^\circ$]')
ax4_1.set_ylabel(r'Ejection angle [$^\circ$]')
ax5_1.set_ylabel(r'Ejection angle [$^\circ$]')
ax6_1.set_ylabel(r'Ejection angle [$^\circ$]')

ax6_1.set_xlabel('Radial distance, r/a')
ax6_2.set_xlabel('Radial distance, r/a')
ax6_3.set_xlabel('Radial distance, r/a')

#Save figure
fig.savefig('./azimuth_angle.png', dpi=400)

#Close plot
plt.close(fig)
