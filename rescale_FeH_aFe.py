#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import glob
import sys
import random 


#loadfile = 'scaling.dat'
#loadfile = 'scaling_extended.dat'
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

	# region = np.where( (find_nearest(feh, FeH_in) == feh ) &\
	# 				   (find_nearest(alpha,aFe_in) == alpha)\
	# 				  )[0]
	argmin_feh = find_nearest(feh, FeH_in)
	argmin_afe = find_nearest(alpha, aFe_in)

	region = np.where(  (argmin_feh <= (feh + feh_tolerance) ) &\
						(argmin_feh >= (feh - feh_tolerance) ) &\
  						(argmin_afe <= (alpha + afe_tolerance) ) &\
						(argmin_afe >= (alpha - afe_tolerance) )\
					  )[0]

	#solutions = log_sumZ[region]
	solutions = sumZ[region]
	all_values = []
	for j,i in enumerate(solutions):
		#print('solultion '+str(j)+': ',i)
		#pair_indices = np.where( i == log_sumZ)[0]
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
			#print('pair for smallest abs(alpha) after loop: (',entry[0],',',smallest,')')

	avg = sum(np.array(solutions))/len(solutions)
	return avg #zero_scaled_FeH

# print("zero-scaled Fe/H for FeH=-1.78, alpha/Fe=0.34: ",zero_scaled_FeH(-1.78,0.34))
# print("zero-scaled Fe/H for FeH=-1.79, alpha/Fe=0.31: ",zero_scaled_FeH(-1.79,0.31))
# # print("zero-scaled Fe/H for FeH=-1.79, alpha/Fe=0.40: ",zero_scaled_FeH(-1.79,0.40))
# #print("zero-scaled Fe/H for FeH=-1.6, alpha/Fe=0.40: ",zero_scaled_FeH(-1.6,0.40))
# print("zero-scaled Fe/H for FeH=-0.87, alpha/Fe=0.30: ",zero_scaled_FeH(-0.87,0.30))
# print("zero-scaled Fe/H for FeH=-0.87, alpha/Fe=0.40: ",zero_scaled_FeH(-0.87,0.40))

# 1.70, 0.15

FeH=float(input('enter [Fe/H]: '))
aFe=float(input('enter [alpha/Fe]: '))

print("for [Fe/H]="+"%.3f"%FeH+\
	", [$\alpha$/Fe]="+"%.1f"%aFe+"--> zero-scaled [Fe/H]=",\
	"%.3f"%zero_scaled_FeH(FeH,aFe))

# FeHs = np.loadtxt('../../MESA/bulge_isochrones/Bensby_FeH_measurements.dat')
# # FeHs = [0.5, 0.4, 0.3, 0.2, 0.1, 0.0,\
# # 		-0.2, -0.4, -0.6, -0.8, -1.0, -1.2,\
# # 		-1.4, -1.6, -1.8, -2.0, -2.2, -2.4]

# outf = open('../../MESA/bulge_isochrones/rescaled_Bensby_physical.dat',"w")
# #outf = open('../../MESA/bulge_isochrones/rescaled_isochrones.dat',"w")
# outf.write("FeH   aFe  rescaled FeH\n")

# # enhanced
# for i in range(len(FeHs)):
# 	FeH = FeHs[i]
# 	aFe = 0.3
# 	line = "%.3f"%FeH +"  "+\
# 	 "%.1f"%aFe + "  "+"%.3f"%zero_scaled_FeH(FeH,aFe) +"\n"

# 	print(line)
# 	outf.write(line)
# 	# print("for [Fe/H]="+"%.3f"%FeH+\
# 	# 	", [$\alpha$/Fe]="+"%.1f"%aFe+"--> zero-scaled [Fe/H]=",\
# 	# 	"%.3f"%zero_scaled_FeH(FeH,aFe))

# # zeros
# for i in range(len(FeHs)):
# 	FeH = FeHs[i]
# 	aFe = 0.0
# 	line = "%.3f"%FeH +"  "+\
# 	 "%.1f"%aFe + "  "+"%.3f"%FeH +"\n"

# 	print(line)
# 	outf.write(line)

# # depleted
# for i in range(len(FeHs)):
# 	FeH = FeHs[i]
# 	aFe = -0.3
# 	line = "%.3f"%FeH +"  "+\
# 	 "%.1f"%aFe + "  "+"%.3f"%zero_scaled_FeH(FeH,aFe) +"\n"

# 	print(line)
# 	outf.write(line)


# outf.close()