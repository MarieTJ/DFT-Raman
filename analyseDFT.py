'''
###########################################
#Description : 
-read a serie of gaussian output files and extract Frequencies and intensity in txt files.
-extract Single points energy from  gaussian output files and takes the 10* lowest energy structures (*variable n_conf)
-get the frequency and intensity for those conformations where intensity is max and rescale using the saclling factor.
###########################################
#Usage : python analyseDFT.py gaussianoutputfileprefix      
###########################################
#Author : Marie Bluntzer
###########################################
'''

import numpy as np
import sys
import os

inputprefix=sys.argv[1]
n_conf=10
scaling_factor=0.968

qu_scaling_factor=0.0000015
files = []

for r, d, f in os.walk('.'):
    for file in f:
        if inputprefix in file and 'log' in file :
            files.append(os.path.join(r, file))

energies=np.zeros((n_conf, 3))
energy=False
for f in files:
    #print('grep \'Frequencies --\' %s |    awk \'{printf  ("%%d\\n%%d\\n%%d\\n",  $3,  $4 , $5 ) }\' >temp1'%(f) )
    os.system( 'grep \'Frequencies --\' %s |    awk \'{printf  ("%%d\\n%%d\\n%%d\\n",  $3,  $4 , $5 ) }\' >temp1'  %(f))
    os.system( 'grep \' Raman Activ --\' %s |    awk \'{printf  (\"%%d\\n%%d\\n%%d\\n\",  $4,  $5 , $6 ) }\' >temp2 ' %(f) )
    os.system( 'paste -d\' \' temp1 temp2 > %s.txt ;' %(f[:-4]))
    results=np.loadtxt(f[:-3]+ 'txt')
    f= open(f, 'r')
    lines=f.readlines()
    for l in range(len(lines)):

        if 'HF=' in lines[l] :
            longline= '%s%s' %(lines[l].replace('\n',''),lines[l+1])
            longline=longline.replace(' ','').split('\\')
            for e in longline :

                if 'HF' in e :
                    energy = float(e.replace('HF=', ''))
    f.close()
    print(results.shape)analyseDFT.py
    if energy and  0 in energies[:,0] and results.size != 0 :
        print(energy)
        index=np.where(energies[:,0] == 0)[0][0]
        energies[index,0] = energy
        intensity=results.max(axis=0)[1]
        frequency=results[results.argmax(axis=0)[1],0]
        energies[index,1] = frequency
        energies[index,2] =intensity

    elif energy and energy < energies[:,0].max()and results.size != 0 :
        index=energies.argmax(axis=0)
        energies[index,0] = energy
        intensity=results.max(axis=0)[1]
        frequency=results[results.argmax(axis=0)[1],0]
        energies[index,1] = frequency
        energies[index,2] =intensity


    energy=False
print(energies)
print(np.average(energies,axis=0))

scalled_avg=np.average(energies,axis=0)
scalled_avg[1]= scalled_avg[1]*scaling_factor
print(scalled_avg)
print(energies.std(axis=0))
