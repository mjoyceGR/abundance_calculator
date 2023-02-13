#!/usr/bin/env python3
import numpy as np
import pandas as pd
import argparse


def numfrac(feh,alpha,abundances):
    if abundances == '2009':
        table = pd.read_fwf('2009abundances.txt')
    if abundances == 'GS98':
        table = pd.read_fwf('GS98abundances.txt')

    setup(feh,alpha,table)

    b = np.exp(np.log(10)*table['A'])
    errb = b*np.log(10)*table['errA']
    sum0 = np.sum(b)
    errsum0 = np.sqrt(np.sum((errb)**2))

    b1 = np.copy(b)
    b1[0] = 0.0
    b1[1] = 0.0

    sum1 = np.sum(b1)

    b = b/sum0
    sumam = np.sum(b*table['awt'])
    b1 = b1/sum1
    errb1 = errb/sum1
    errb = errb/sum0

    print('----------------')
    print('Number Fractions')
    print('----------------')
    for idx in np.arange(23):
        print(table['element'][idx],b1[idx],errb1[idx])

    a = b*table['awt']/sumam
    erra = errb*table['awt']/sumam
    
    print('--------------')
    print('Mass fractions')
    print('--------------')
    for idx in np.arange(23):
        print(table['element'][idx],a[idx],erra[idx])

    sumz = np.sum(a[2:])
    errsumz = np.sqrt(np.sum(erra[2:]**2))  

    print('---')
    print(' sumZ =',sumz,'+/-',errsumz)
    print('Z/X = ',sumz/a[0],'+/-',errsumz/a[0])

#########################
def numfrac_justZ(feh,alpha,abundances):
    if abundances == '2009':
        table = pd.read_fwf('2009abundances.txt')
    if abundances == 'GS98':
        table = pd.read_fwf('GS98abundances.txt')

    setup(feh,alpha,table)

    b = np.exp(np.log(10)*table['A'])
    errb = b*np.log(10)*table['errA']
    sum0 = np.sum(b)
    errsum0 = np.sqrt(np.sum((errb)**2))

    b1 = np.copy(b)
    b1[0] = 0.0
    b1[1] = 0.0

    sum1 = np.sum(b1)

    b = b/sum0
    sumam = np.sum(b*table['awt'])
    b1 = b1/sum1
    errb1 = errb/sum1
    errb = errb/sum0

    a = b*table['awt']/sumam
    erra = errb*table['awt']/sumam
    
    sumz = np.sum(a[2:])
    errsumz = np.sqrt(np.sum(erra[2:]**2))  

    #print('---')
    # print(' sumZ =',sumz,'+/-',errsumz)
    # print('Z/X = ',sumz/a[0],'+/-',errsumz/a[0])
    #print(sumz,errsumz,sumz/a[0],errsumz/a[0])
    return sumz, errsumz, sumz/a[0], errsumz/a[0]

###############

def setup(feh,alpha,table):
    for index, row in table.iterrows():
        if row['element'] == 'C':
            table.at[index,'A'] += feh
        if row['element'] == 'N':
            table.at[index,'A'] += feh
        if row['element'] == 'O':
            table.at[index,'A'] += feh
            table.at[index,'A'] += alpha
        if row['element'] == 'Ne':
            table.at[index,'A'] += feh
            table.at[index,'A'] += alpha
        if row['element'] == 'Na':
            table.at[index,'A'] += feh
        if row['element'] == 'Mg':
            table.at[index,'A'] += feh
            table.at[index,'A'] += alpha
        if row['element'] == 'Al':
            table.at[index,'A'] += feh
        if row['element'] == 'Si':
            table.at[index,'A'] += feh
            table.at[index,'A'] += alpha
        if row['element'] == 'P':
            table.at[index,'A'] += feh
        if row['element'] == 'S':
            table.at[index,'A'] += feh
            table.at[index,'A'] += alpha
        if row['element'] == 'Cl':
            table.at[index,'A'] += feh
        if row['element'] == 'Ar':
            table.at[index,'A'] += feh
        if row['element'] == 'Ca':
            table.at[index,'A'] += feh
            table.at[index,'A'] += alpha
        if row['element'] == 'Ti':
            table.at[index,'A'] += feh
            table.at[index,'A'] += alpha
        if row['element'] == 'Cr':
            table.at[index,'A'] += feh
        if row['element'] == 'Mn':
            table.at[index,'A'] += feh
            table.at[index,'A'] -= alpha
        if row['element'] == 'Fe':
            table.at[index,'A'] += feh
        if row['element'] == 'Ni':
            table.at[index,'A'] += feh

# Main
parser = argparse.ArgumentParser(description='Calculates number, mass fractions given Fe/H and alpha/Fe')
parser.add_argument('feh', help='Fe/H', type=float)
parser.add_argument('alpha', help='alpha/Fe', type=float)
parser.add_argument('abundances', help='Soure of solar abundances: GS98, 2009', type=str)

# args = parser.parse_args()
# cmdLine=True

abundances = '2009' #'2009abundances.txt'

#numfrac(args.feh,args.alpha,args.abundances)

#feh_array = np.arange(-3.5,0.501,0.01)
#feh_array = np.arange(-3.5,0.5,0.002)
feh_array = np.arange(0.5,0.8,0.002)
aFe_array = np.arange(-0.4,0.6,0.002) #[0.0, 0.2, 0.4, 0.6]


#outfile = 'scaling_extended.dat'
#outfile = 'scaling_highres_extended.dat'
outfile = 'highZ_extension.dat'

overwrite=input('Are you sure you want to overwrite  '+ outfile +'? (Y/n) ')
if overwrite =='Y':
    outf = open(outfile,'w')
    outf.write('#FeH, alpha/Fe, sumZ, err_sumZ, Z/X, Z/X_err\n')
    for feh in feh_array:
        for alpha in aFe_array:
            sumZ, err_sumZ, ZX, err_ZX = numfrac_justZ(feh, alpha, abundances)
            #print(feh, alpha, sumZ, err_sumZ, ZX, err_ZX)
            outf.write("%.4f"%feh+ '  '+ "%.2f"%alpha+\
                  '  '+"%.6f"%sumZ+ '  '+"%.7f"%err_sumZ+
                  '  '+"%.6f"%ZX+ '  '+"%.7f"%err_ZX+ '  '+'\n')
    outf.close()
else:
    pass