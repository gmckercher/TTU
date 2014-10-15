# -*- coding: utf-8 -*-

'''Created on 10/4/2014 by Grant McKercher
ATMO 5231 Cloud Physics Mid-semester project
Texas Tech University

Reads, Analyzes, and plots Data from skewt.py and Bolton.py

Skips the number of lines before the data begins
'''

import numpy as np
def parse_SPC(filename, skip_rows=0):
	'''returns a record array with column names and data types'''
	dtype = [ ('p', float), ('z', float), ('T', float), ('Td', float)]
	'''pressure (mb), altitude (m), temperature (Celsius), dewpoint (Celsius), 
	wind direction (degrees), wind speed (knots)'''
	data = np.genfromtxt(filename, dtype=dtype, skip_header=skip_rows, delimiter=',')
	return data