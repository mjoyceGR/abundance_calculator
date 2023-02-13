#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import glob
import sys
import random 

do_plot = True

#loadfile = 'scaling.dat'
#loadfile = 'scaling_extended.dat'
#oadfile = 'scaling_highres_extended.dat'
loadfile = 'highZ_extension.dat'


feh, alpha, sumZ, sumZerr, ZX, ZX_err= np.loadtxt(loadfile, usecols=(0,1,2,3,4,5), unpack= True)

if do_plot:
	fig, ax = plt.subplots(figsize = (18,12))
	sc = plt.scatter(feh, alpha, c = np.log10(sumZ))
	plt.colorbar(sc, label='log10(sumZ)')

	# sc = plt.scatter(feh, alpha, c = sumZ)
	# plt.colorbar(sc, label='sumZ')

	# sc = plt.scatter(feh, alpha, c = ZX)
	# plt.colorbar(sc, label='Z/X')

	plt.xlabel('[Fe/H]')
	plt.ylabel('[alpha/Fe]')
	plt.show()
	plt.close()
	sys.exit()