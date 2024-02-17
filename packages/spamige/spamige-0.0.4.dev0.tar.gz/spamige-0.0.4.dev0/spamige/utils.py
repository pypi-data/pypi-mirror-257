import glob
import os
import natsort
import shutil
from datetime import datetime
import subprocess


# Wrapper for registration
def spamRegistration( img1, 
                      img2,
                      mask = None, 
                      iterations = 50 ):
    dt = datetime.now()

    prefix =  'tmp_reg'+str(round(datetime.timestamp(dt)))+'/'
    os.mkdir(prefix)
    cmd = [ 'spam-reg', img1, img2, '-bb', '4', '-it', str( iterations ), '-od', prefix, '-mf1', mask ]
    subprocess.Popen(cmd).wait()
    
    return prefix

# Wrapper for LDIC
def spamLDIC( img1,
              img2,
              initGuess = None,
              mask = None,
              iterations = 200,
              hws = 16,
              give_ns=True):
            
    # set ns to 2*hws+1
    ns=2*hws+1

    dt = datetime.now()

    prefix =  'tmp_ldic'+str(round(datetime.timestamp(dt)))+'/'
    os.mkdir(prefix)
    
    cmd = ['spam-ldic', img1, img2, '-pf', initGuess, '-it', str(iterations),'-vtk', '-od', prefix, '-dp', '0.001', '-glt', '1', '-mf1', mask, '-hws', str(hws)]
    
    if give_ns:
        cmd.append('-ns')
        cmd.append(str(ns))
    
    subprocess.Popen(cmd).wait()
    
    return prefix

# Wrapper for correction
def spamCorrection(tsvFile):

    # Correction
    dt = datetime.now()
    OutputCorrected='tmp_corrected'+str(round(datetime.timestamp(dt)))+'/'
    os.mkdir(OutputCorrected)
    
    cmd = ['spam-filterPhiField', '-pf', tsvFile, '-srs', '-srst', '1', '-nn', '4', '-cint', '-F', 'all','-od', OutputCorrected]
    subprocess.Popen( cmd ).wait()

    im_cor=natsort.natsorted(glob.glob(os.path.join(OutputCorrected,'*.tsv')))
    
    # Filtering
    dt = datetime.now()
    OutputFiltered = 'tmp_filtered'+str(round(datetime.timestamp(dt)))+'/'
    os.mkdir(OutputFiltered)

    if len(im_cor)==0:
        im_cor=[tsvFile]
        print( '\n Filtering non corrected file !')

    cmd = ['spam-filterPhiField', '-pf', im_cor[0], '-fm', '-fmr', '1', '-F', 'all', 
               '-vtk', '-od', OutputFiltered]
    subprocess.Popen( cmd ).wait()

    #shutil.rmtree(OutputCorrected)

    return OutputCorrected,OutputFiltered,im_cor

# Wrapper for strain calculation
def spamStrain(tsvFile):
    
    dt = datetime.now()
    OutputStrain = 'tmp_strain'+str(round(datetime.timestamp(dt)))+'/'

    cmd = [ 'spam-regularStrain', tsvFile, '-comp', 'vol', 'dev', 'U','e', '-rst', "1", '-vtk','-noTSV', '-od', OutputStrain]
    subprocess.Popen( cmd ).wait()

    return OutputStrain