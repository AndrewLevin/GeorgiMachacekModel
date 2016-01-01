#!/bin/env python

import subprocess, sys, os, re, math

if __name__ == "__main__":
    
    mhpps       = [200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900, 2000]
    #mhpps       = [200]

    for mhpp in mhpps:
        print mhpp
        
        template_gmmg5 = open('/afs/cern.ch/work/a/anlevin/gmcalc/gmcalc1.2.0_template/gmmg5.f')
        new_gmmg5 = open('/afs/cern.ch/work/a/anlevin/gmcalc/gmcalc1.2.0/gmmg5.f', 'w')

        in_inputset_3=False
        for line in template_gmmg5:

            if in_inputset_3:
                if "IMH5" in line:
                    new_gmmg5.write("            IMH5 = "+str(mhpp)+".00000D0\n")
                    continue
            if "INPUTSET.EQ.3" in line:
                in_inputset_3=True
            if "INPUTSET.EQ.4" in line:
                in_inputset_3=False

            new_gmmg5.write(line)

        new_gmmg5.close()    

        os.system("cd /afs/cern.ch/work/a/anlevin/gmcalc/gmcalc1.2.0/; make gmmg5; ./gmmg5.x; diff param_card-NLO.dat ../gmcalc1.2.0_template/param_card-NLO.dat; cd -; cp /afs/cern.ch/work/a/anlevin/gmcalc/gmcalc1.2.0/param_card-NLO.dat param_card_"+str(mhpp)+".dat")
