#!/bin/env python

import subprocess, sys, os, re, math

if __name__ == "__main__":
    
    mhpps       = [200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900, 2000]
    #mhpps       = [200]

    for mhpp in mhpps:
        print mhpp
        
        template_gmmg5 = open('/afs/cern.ch/work/a/anlevin/gmcalc/gmcalc1.1.0_template/gmmg5.f')
        new_gmmg5 = open('/afs/cern.ch/work/a/anlevin/gmcalc/gmcalc1.1.0/gmmg5.f', 'w')

        template_gmpoint = open('/afs/cern.ch/work/a/anlevin/gmcalc/gmcalc1.1.0_template/gmpoint.f')
        new_gmpoint = open('/afs/cern.ch/work/a/anlevin/gmcalc/gmcalc1.1.0/gmpoint.f', 'w')

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

        in_inputset_3=False
        for line in template_gmpoint:

            if in_inputset_3:
                if "IMH5" in line:
                    new_gmpoint.write("            IMH5 = "+str(mhpp)+".00000D0\n")
                    continue
            if "INPUTSET.EQ.3" in line:
                in_inputset_3=True
            if "INPUTSET.EQ.4" in line:
                in_inputset_3=False

            new_gmpoint.write(line)

        new_gmpoint.close()    

        os.system("cd /afs/cern.ch/work/a/anlevin/gmcalc/gmcalc1.1.0/; make gmpoint; ./gmpoint.x >& gmpoint_output.txt; cat gmpoint_output.txt | tail -n 1; cd -;") 
        
        hpp_width=os.popen("cat /afs/cern.ch/work/a/anlevin/gmcalc/gmcalc1.1.0/gmpoint_output.txt | tail -n1 | awk '{print $2}'").read()

        hpp_width=hpp_width.rstrip('\n')

        os.system("cd /afs/cern.ch/work/a/anlevin/gmcalc/gmcalc1.1.0/; make gmmg5; ./gmmg5.x; diff param_card.dat ../gmcalc1.1.0_template/param_card.dat; cd -;")

        new_param_card = open ('/afs/cern.ch/work/a/anlevin/gmcalc/gmcalc1.1.0/param_card.dat')

        #the param card with the correct width in it
        new_new_param_card = open ('param_card_'+str(mhpp)+'.dat','w')

        for line in new_param_card:
            if "DECAY 255" in line:    
                new_new_param_card.write("DECAY 255 "+str(hpp_width)+" # WH5pp\n")
            else:
                new_new_param_card.write(line)
