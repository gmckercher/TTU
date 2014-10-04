# -*- coding: utf-8 -*-

'''
Skew-T Log-P diagram
Created on 10/4/2014 by Grant McKercher
ATMO 5231 Cloud Physics Mid-semester project
Texas Tech University

Under direction of Dr. Eric Bruning 
'''

'1'

import numpy as np
import Bolton 
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist import Subplot
from matplotlib.ticker import FuncFormatter, Formatter
from mpl_toolkits.axisartist.grid_helper_curvelinear import GridHelperCurveLinear
from readsoundings.py import parse_SPC


C_to_K = 273.15
skew_slope = 40


def x_from_Tp(T,p):
	"calculates x(T,p)"
	x = T - (skew_slope * np.log(p))
	return x

def y_from_p(p):
	"calculates y(p)"
	y = -np.log(p)
	return y

def T_from_xp(x,p):
	"calculates T(x,p)"
	T = (skew_slope * np.log(p)) + x
	return T

def p_from_y(y):
	"calculates p(y)"
	p = np.exp(-y)
	return p

''' These functions help plot the sounding data,
which is why they take T in Celcius'''

def to_thermo(x,y):
	''' Transform (x,y) coordinates to T in degrees Celcius and p in mb '''
	p = p_from_y(y)
	T_C = T_from_xp(x,p) - C_to_K
	return T_C, p

def from_thermo(T_C,p):
	''' Transform T_C (degrees Celcius) and p (mb) to (x,y) '''
	y = y_from_p(p)
	x = x_from_Tp(T_C+C_to_K,p)
	return x,y

'2'

# axis values along the bottom and left edges
p_bottom = 1050.0
p_top = 150
T_min = -40 + C_to_K
T_max = 50 + C_to_K

# axis values converted to x and y coordinates
x_min = x_from_Tp(T_min,p_bottom)
x_max = x_from_Tp(T_max,p_bottom) #???? correct?
y_min = y_from_p(p_bottom)
y_max = y_from_p(p_top)

'3'

'''defining all the constant pressure levels and 
values of constant T,theta,theta_e,and mixing ratio'''

# pressure levels from 1000-150mb with 50mb intervals
p_levels_mb = np.arange(1000,150-50,-50)
p_levels = p_levels_mb
# temperature levels from -80 to 40 Celsius with 10 degree intervals
T_C_levels = np.arange(-80,40+10,10)
T_levels = T_C_levels + C_to_K 
# potential temperature levels from -40 to 100 Celsius with 10 degree intervals
theta_C_levels = np.arange(-40,100+10,10)
theta_levels = theta_C_levels + C_to_K
# same levels for theta_ep as theta
theta_ep_levels = theta_levels.copy()
# UCAR RAP sounding mixing ratios in kg/kg 
g_kg = np.array([.4,1,2,3,5,8,12,16,20])
mixing_ratios = g_kg / 1000
np.asarray(mixing_ratios)

'5'

"Convert from T,p to x,y"

# p_all ranges from p_bottom to p_top in 1mb increments
p_all = np.arange(p_bottom,p_top-1,-1)

y_p_levels = y_from_p(p_levels)
y_all_p = y_from_p(p_all)

# List of arrays of x positions corresponding to constant T values
x_T_levels = [x_from_Tp(Ti,P_all) for Ti in T_levels]

# Calling functions from Bolton
x_thetas = [x_from_Tp(Bolton.theta_dry(theta_i,p_all),p_all) for theta_i in theta_levels]
x_mixing_ratios = [x_from_Tp(Bolton.mixing_ratio_line(w_i,p_all),p_all) for w_i in mixing_ratios]
#??? mixing ratios

'''Calculate field of theta_ep values that will be contoured to define moist adiabats.
The meshgrid function produces 2D mesh_T and mesh_p from 1D arrays of T 
(from -60 to 40 Celsius in 0.1 degree increments) and p.

mesh_T[i,j] and mesh_p[i,j] define all the [i,j] locations theta_ep_mesh is calculated'''
mesh_T, mesh_p = np.meshgrid(np.arange(-60.0,T_levels.max() - C_to_K + 0.1, 0.1),p_all)
theta_ep_mesh = Bolton.theta_ep_field(mesh_T, mesh_p)

'6'

"Plotting Script"

skew_grid_helper = GridHelperCurveLinear((from_thermo,to_thermo))
gridhelper = fig.add_subplot(skew_grid_helper) # step e ????

fig = plt.figure()
ax = Subplot(fig,1,1,1)
fig.add_subplot(ax)

def format_coord(x,y):
	T,p = to_thermo(x,y)
	return "{0:5.1f} C, {1:5.1f} mb".format(float(T),float(p))

ax.format_coord = format_coord

for yi in y_p_levels:
	ax.plot((x_min,x_max),(yi,yi),color=(1.0,0.8,0.8))

for x_T in x_T_levels:
	ax.plot(x_T,y_all_p,color=(1.0,0.5,0.5))

for x_theta in x_thetas:
	ax.plot(x_theta,y_all_p,color=(1.0,0.7,0.7))

for x_mixing_ratio in x_mixing_ratios:
	good = all_P >= 600 # restrict mixing ratio lines to below 600mb
	ax.plot(x_mixing_ratio[good],y_all_p[good],color=(0.8,.8,0.6))

n_moist = len(theta_ep)
moist_colors = ((0.6,0.9,0.7),)*n_moist
ax.contour(x_from_Tp(mesh_T + C_to_K,mesh_p), y_from_p(mesh_p), theta_ep_mesh, theta_ep_levels, colors=moist_colors)

ax.axis((x_min,x_max,y_min,y_max))

'7'

# SPC sounding Denver/Boulder 10/04/2014 12:00 UTC
sounding_data = '/Users/Grant/Desktop/ttuwork/classes/Cloud Physics/coding/DNR141004_12Z.txt'
parse_SPC(sounding_data)
# all temperature values (Celsius) should be in this range
snd_T = sounding_data['T']
good_T = (snd_T > -100.0) & (snd_T < 60.0)
# all pressure values (mb) should be in this range
snd_p = sounding_data['p']
good_p = (snd_p > 0.0) & (snd_p < 2000.0)
# all dewpoint temperature values (Celsius) should be in this range
snd_Td = sounding_data['Td']
good_Td = (snd_Td > -100.0) & (snd_Td < 60.0)
# Conversions for plotting
snd_T = snd_T + C_to_K
snd_Td = snd_Td + C_to_K
x_snd_T = x_from_Tp(snd_T,snd_p)
x_snd_Td = x_from_Tp(snd_Td,snd_p)
y_snd_p = y_from_p(snd_p)
# Plot temperature and dewpoint temperature traces
ax.plot(x_snd_Td, y_snd_p, linewidth=2, color='g')
ax.plot(x_snd_T, y_snd_p, linewidth=2, color='r')

plt.show()

