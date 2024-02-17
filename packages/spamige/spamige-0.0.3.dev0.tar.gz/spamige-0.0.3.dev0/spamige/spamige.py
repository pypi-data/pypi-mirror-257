import spamige.utils as spu
import glob
import os
import natsort
import shutil

def spam_workflow(folder_img,mask,hws=16,iter_max=100,folder_prefix=''):
    '''
    workflow designed for 2D correlation from laboratory ice experiment

    :param folder_img: either path to thefolder containing the images or the list of path of each images
    :type folder_img: list or str
    :param hws: spam hws parameter for spam-ldic
    :type hws: int
    :param folder_prefix: folder prefix is wanted
    :type folder_prefix: str
    '''


    if isinstance(folder_img, list):
        im_list=folder_img
    else:
        im_list=natsort.natsorted(glob.glob(os.path.join(folder_img,'*.tiff')))


    if len(folder_prefix)!=0:
        if folder_prefix[-1]!='/':
            folder_prefix+='/'
        os.mkdir(folder_prefix)

    for count, im2 in enumerate (im_list[1:]):
        
        directories_to_remove = []
        
        if count==0:
            # Registration
            res_reg=spu.spamRegistration(im_list[0],im2,mask)
            # Init Guess
            init_guess=glob.glob(os.path.join(res_reg,'*.tsv'))[0]
            os.makedirs(folder_prefix+'spam-init_guess', exist_ok=True)
            shutil.copy(init_guess,folder_prefix+'spam-init_guess/'+str(count)+init_guess.split('/')[-1])
            directories_to_remove.append(res_reg)
            give_ns=True
        else:
            # Init Guess from last ldic
            give_ns=False
            init_guess=natsort.natsorted(glob.glob(os.path.join(folder_prefix+'spam-init_guess/','*.tsv')))[-1]
            print(init_guess)

        # LDIC
        res_ldic=spu.spamLDIC(im_list[0],im2,initGuess=init_guess,mask=mask,hws=hws,give_ns=give_ns,iterations=iter_max)
        directories_to_remove.append(res_ldic)

        # Filtering
        tsvFile=natsort.natsorted(glob.glob(os.path.join(res_ldic,'*.tsv')))
        corrected_ldic,filter_ldic,cor_ldic=spu.spamCorrection(tsvFile[0])
        
        directories_to_remove.append(corrected_ldic)
        directories_to_remove.append(filter_ldic)
        os.makedirs(folder_prefix+'spam-ldic-not-filtered', exist_ok=True)
        shutil.move(cor_ldic[0].replace('.tsv', '.vtk'),folder_prefix+'spam-ldic-not-filtered/'+cor_ldic[0].replace('.tsv', '.vtk').split('/')[-1])
        os.makedirs(folder_prefix+'spam-ldic-filtered', exist_ok=True)
        ldic_f_vtk=natsort.natsorted(glob.glob(os.path.join(filter_ldic,'*.vtk')))
        shutil.move(ldic_f_vtk[0],folder_prefix+'spam-ldic-filtered/'+ldic_f_vtk[0].split('/')[-1])

        # Strain rate on filtered data
        strain_f_tsv=natsort.natsorted(glob.glob(os.path.join(filter_ldic,'*.tsv')))
        strain_f=spu.spamStrain(strain_f_tsv[0])
        directories_to_remove.append(strain_f)

        os.makedirs(folder_prefix+'spam-strain-filtered', exist_ok=True)
        strain_f_vtk=natsort.natsorted(glob.glob(os.path.join(strain_f,'*.vtk')))
        shutil.move(strain_f_vtk[0],folder_prefix+'spam-strain-filtered/'+strain_f_vtk[0].split('/')[-1])

        # Strain rate on NONE filtered data
        strain_nf=spu.spamStrain(cor_ldic[0])
        directories_to_remove.append(strain_nf)

        os.makedirs(folder_prefix+'spam-strain-not-filtered', exist_ok=True)
        strain_nf_vtk=natsort.natsorted(glob.glob(os.path.join(strain_nf,'*.vtk')))
        shutil.move(strain_nf_vtk[0],folder_prefix+'spam-strain-not-filtered/'+strain_nf_vtk[0].split('/')[-1])

        # Save init guess at each time : can be used for re-run if one day it is implemented
        ldic_f_tsv=natsort.natsorted(glob.glob(os.path.join(filter_ldic,'*.tsv')))
        shutil.move(ldic_f_tsv[0],folder_prefix+'spam-init_guess/'+str(count+1)+ldic_f_tsv[0].split('/')[-1])

        # Remove directories
        for directory in directories_to_remove:
            shutil.rmtree(directory)
