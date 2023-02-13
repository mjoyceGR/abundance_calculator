#!/usr/bin/env python3
####################################################
#
# Author: M Joyce
#
####################################################
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import glob
import sys
import random 


loadfile = 'scaling_highres_extended.dat' #includes highZ extension
feh, alpha, sumZ, sumZerr, ZX, ZX_err= np.loadtxt(loadfile, usecols=(0,1,2,3,4,5), unpack= True)
log_sumZ = np.log10(sumZ)

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def find_iso_surface(FeH_in, aFe_in):
	####################################
	#
	# returns set of ordered pairs (Fe/H, alpha/Fe)
	# that give equivalent global metallicities, sumZ, 
	# to the input (Fe/H, alpha/Fe) combination
	#
	#####################################
	feh_tolerance = 0.03 #0.02
	afe_tolerance = 0.03 #0.02

	argmin_feh = find_nearest(feh, FeH_in)
	argmin_afe = find_nearest(alpha, aFe_in)

	region = np.where(  (argmin_feh <= (feh + feh_tolerance) ) &\
						(argmin_feh >= (feh - feh_tolerance) ) &\
  						(argmin_afe <= (alpha + afe_tolerance) ) &\
						(argmin_afe >= (alpha - afe_tolerance) )\
					  )[0]


	solutions = sumZ[region]
	all_values = []
	for j,i in enumerate(solutions):
		pair_indices = np.where( i == sumZ)[0]
		
		for pair_index in pair_indices:
			all_values.append( [feh[pair_index], alpha[pair_index]] ) 
	
	return all_values



def zero_scaled_FeH(FeH_in, aFe_in):
	pairs = find_iso_surface(FeH_in, aFe_in)
	smallest=100
	
	for entry in pairs:
		#print('entry: ',entry)
		if abs(entry[1]) < abs(smallest):
			smallest= entry[1]
	

	solutions = []
	for entry in pairs:
		if entry[1] ==smallest:
			solutions.append(entry[0])
	avg = sum(np.array(solutions))/len(solutions)
	return avg #zero_scaled_FeH


# FeH=float(input('enter [Fe/H]: '))
# aFe=float(input('enter [alpha/Fe]: '))

FeHs = [-2.0,-1.6,-1.2,-0.8,-0.4, 0.0, 0.4]
aFes = [0.0,0.2,0.4]

for FeH in FeHs:
	for aFe in aFes:
		print("for [Fe/H]="+"%.3f"%FeH+\
			", [$\alpha$/Fe]="+"%.1f"%aFe+"--> zero-scaled [Fe/H]=",\
		"%.3f"%zero_scaled_FeH(FeH,aFe))
