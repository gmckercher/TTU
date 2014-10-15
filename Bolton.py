# -*- coding: utf-8 -*-
'''
Bolton (1980) formulae 
Created on 10/4/2014 by Grant McKercher
ATMO 5231 Cloud Physics Mid-semester project
Texas Tech University

FORMULAE SOURCE
Bolton, D. (1980). 
The computation of equivalent potential temperature. 
Monthly weather review, 108(7), 1046-1053.
'''

import numpy as np

C_to_K = 273.15 #K
c_p_dry = 1005.7 #J/kgK
c_V_dry = 4190. #J/kgK
eps = 0.622
k_dry = 0.2854

def sat_vapor_pressure(T):
	'''equation 10 from Bolton,
	given T in Celsius, 
	returns e_s in mb'''
	e_s = 6.112 * np.exp((17.67 * T) / (T + 243.5))
	return e_s

def sat_vapor_temperature(e_s):
	'''equation 11 from Bolton,
	given e_s in mb,
	returns T in Celsius'''
	T = (((243.5 * np.log(e_s)) - 440.8) / (19.48 - np.log(e_s)))
	return T

def sat_mixing_ratio(p,T):
	'''equation from assignment sheet,
	given p in mb and T in Celsius,
	returns w_s in kg/kg'''
	e_s = sat_vapor_pressure(T)
	w_s = eps * (e_s / (p - e_s))
	return w_s

def mixing_ratio_line(p,w_s):
	'''given p in mb and w_s in kg/kg, 
	returns T in Celsius'''
	e_s = ((w_s * p) / (eps + w_s))
	T = sat_vapor_temperature(e_s)
	return T

def RH(T,p,w):
	'''given T in Celsius, p in mb, w in kg/kg,
	returns RH in precent'''
	w_s = sat_mixing_ratio(p,T)
	RH = (w / w_s) * 100.
	return RH

def T_LCL(T,RH):
	'''equation 22 from Bolton,
	given T in Kelvin and RH in percent,
	returns LCL temperature in Kelvin'''
	T_LCL = (1 / ((1/(T-55.))-((np.log(RH/100.))/2840.))) + 55.
	return T_LCL

def theta_dry(theta,p,p_0=1000.0):
	'''equation 23 from Bolton,
	given potential temperature and pressures,
	return T in Kelvin. 

	Assume that e=0 (all p is due to dry air alone)
	Function can be used to calculate dry adiabats.'''
	theta_dry = theta / ((p_0 / p)**(k_dry))
	return theta_dry

def pseudoeq_potential_T(T,p,w,p_0=1000.0):
	'''equation 43 from Bolton,
	given T in Celsius, p in mb, and w in kg/kg,
	returns pseudoadiabatic equivalent potential temperature in Kelvin'''
	rh = RH(T,p,w) / 100.
	T_lcl = T_LCL((T+C_to_K),rh)
	r = w * 1000. # g/kg
	theta_eq = ((T+C_to_K) * ((p_0/p)**(k_dry*(1-0.28*10**-3*r)))) * np.exp(((3.376/T_lcl)-0.00254) * (r*(1+0.81*10**-3*r)))
	return theta_eq

def theta_ep_field(T,p,p_0=1000.0):
	'''Function dependant on both p and w.
	calculates a 2D field of theta_ep from T and p values
	and moist adiabats can be ploted using matplotlib contouring.

	given T in Celsius and p in mb,
	returns theta_ep in Kelvin
	'''
	w_s = sat_mixing_ratio(p,T)
	theta_ep = pseudoeq_potential_T(T,p,w_s) 
	return theta_ep


	






