#!/usr/bin/env python3
# coding: utf-8

#=========================================================================================
# Diffusion MRI Pre-processing Scripts 
# Emily Drabek-Maunder
# 2025, UCL ICH (Developmental Imaging & Biophysics Section)
# Script 2 of 3

# This script runs denoising, degibbsing, topup and eddy for full image pre-processing.
# Note: topup and eddy do not fully output logs to check motion artefacts (i.e. for eddy_qc)
#=========================================================================================

import os
import sys
import numpy as np

directory='./'

filename=sys.argv[1]

id, date = np.loadtxt(directory + filename, delimiter = ',', usecols=(0,1), unpack=True, dtype='object')
DTI_multi_input, DTI_negPE_input = np.loadtxt(directory + filename, delimiter = ',', usecols=(2,3),unpack=True, dtype='object')
t1_input = np.loadtxt(directory + filename, delimiter = ',', usecols=(4), unpack=True, dtype='object')

for i in range (0,len(id)):

    data_dir = directory + id[i] + '/' + date[i] + '/'
    data_dir_raw = data_dir + 'raw/'
    data_dir_preproc = data_dir + 'preproc/'
    data_dir_mrtrix = data_dir + 'mrtrix/'
    
    data_dir_biascorr = data_dir+'bias_corr/'

    if DTI_multi_input[i].endswith(".nii.gz") or DTI_negPE_input[i].endswith(".nii.gz"):
        DTI_multi_nifti=DTI_multi_input[i]
        DTI_negPE_nifti=DTI_negPE_input[i]

    if DTI_multi_input[i].endswith(".mif"):
        DTI_multi_nifti='data.nii.gz'
        DTI_negPE_nifti='data_negpe.nii.gz'

    os.system('dwidenoise ' + data_dir_preproc + 'data.mif ' + data_dir_preproc + 'denoise.mif -noise ' + data_dir_preproc + 'noiselevel.mif -mask ' + data_dir_preproc + 'preproc_mask.mif -force')
    os.system('mrdegibbs ' + data_dir_preproc + 'denoise.mif ' + data_dir_preproc + 'degibbs.mif -force')

    os.system('fslroi ' + data_dir_raw + DTI_multi_nifti + ' ' + data_dir_preproc + 'b0.nii.gz 0 1')
    os.system('fslmerge -t ' + data_dir_preproc + 'b0pair.nii.gz ' + data_dir_preproc + 'b0.nii.gz ' + data_dir_raw + DTI_negPE_nifti)

    os.system('mkdir ' + data_dir + 'mrtrix')

    os.system('dwifslpreproc -rpe_pair -se_epi ' + data_dir_preproc + 'b0pair.nii.gz -pe_dir AP -eddy_options "--repol " ' + data_dir_preproc + 'degibbs.mif ' + data_dir_mrtrix + 'dwi.mif -force')
    
    os.system('mkdir ' + data_dir + 'bias_corr')
    
    os.system('dwibiascorrect fsl ' + data_dir_mrtrix + 'dwi.mif ' + data_dir_biascorr + 'biascorr.mif -mask ' + data_dir_preproc + 'preproc_mask.mif -bias ' + data_dir_biascorr + 'biasfield.mif -force')
