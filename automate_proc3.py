#!/usr/bin/env python3
# coding: utf-8

#=========================================================================================
# Diffusion MRI - Spherical Deconvolution and Diffusion Tensor Imaging 
# Emily Drabek-Maunder
# 2025, UCL ICH (Developmental Imaging & Biophysics Section)
# Script 3 of 3

# This script runs CSD and DTI.
#=========================================================================================

import os
import sys
import numpy as np

directory='./'

filename=sys.argv[1]

id, date = np.loadtxt(directory + filename, delimiter = ',', usecols=(0,1), unpack=True, dtype='object')
DTI_multi_input, DTI_negPE_input = np.loadtxt(directory + filename, delimiter = ',', usecols=(2,3), unpack=True, dtype='object')
t1_input = np.loadtxt(directory + filename, delimiter = ',', usecols=(4), unpack=True, dtype='object')

for i in range (0,len(id)):

    data_dir = directory + id[i] + '/' + date[i] + '/'
    data_dir_raw = data_dir + 'raw/'
    data_dir_preproc = data_dir + 'preproc/'
    data_dir_biascorr = data_dir + 'bias_corr/'
    data_dir_mrtrix = data_dir + 'mrtrix/'
    
    data_dir_biascorr_mrtrix = data_dir_biascorr + 'mrtrix/'
    data_dir_dtifit = data_dir_biascorr + 'dtifit/'

    os.system('mkdir ' + data_dir_biascorr_mrtrix)

    os.system('mrconvert ' + data_dir_biascorr + 'biascorr.mif  ' + data_dir_biascorr_mrtrix + 'dwi.mif -force')
    os.system('mrconvert ' + data_dir_biascorr_mrtrix + 'dwi.mif  ' + data_dir_biascorr_mrtrix + 'data.nii.gz -stride 1,2,3,4 -force')

    os.system('fslroi  ' + data_dir_biascorr_mrtrix + 'data.nii.gz  ' + data_dir_biascorr_mrtrix + 'nodif.nii.gz 0 1')
    os.system('bet  ' + data_dir_biascorr_mrtrix + 'nodif.nii.gz  ' + data_dir_biascorr_mrtrix + 'brain -m -n -f 0.3')
    os.system('mrconvert ' + data_dir_biascorr_mrtrix + 'brain_mask.nii.gz ' + data_dir_biascorr_mrtrix + 'mask.mif')

    os.system('dwi2response dhollander ' + data_dir_biascorr_mrtrix + 'dwi.mif ' + data_dir_biascorr_mrtrix + 'wm_response.txt ' + data_dir_biascorr_mrtrix + 'gm_response.txt ' + data_dir_biascorr_mrtrix + 'csf_response.txt -nocleanup -scratch ' + data_dir_biascorr_mrtrix + ' -nocleanup -force')
    os.system('dwi2fod msmt_csd -mask ' + data_dir_biascorr_mrtrix + 'mask.mif ' + data_dir_biascorr_mrtrix + 'dwi.mif ' + data_dir_biascorr_mrtrix + 'wm_response.txt ' + data_dir_biascorr_mrtrix + 'wm.mif ' + data_dir_biascorr_mrtrix + 'gm_response.txt ' + data_dir_biascorr_mrtrix + 'gm.mif ' + data_dir_biascorr_mrtrix + 'csf_response.txt ' + data_dir_biascorr_mrtrix + 'csf.mif -force')

    os.system('mkdir ' + data_dir_dtifit)
    
    os.system('mrconvert ' + data_dir_biascorr_mrtrix + 'dwi.mif ' + data_dir_dtifit + 'data_proc.nii.gz -stride 1,2,3,4 -export_grad_fsl ' + data_dir_dtifit + 'bvecs.txt ' + data_dir_dtifit + 'bvals.txt -force')
    os.system('dtifit -k ' + data_dir_dtifit + 'data_proc.nii.gz -o ' + data_dir_dtifit + id[i] + '_' + date[i] + ' -m ' + data_dir_biascorr_mrtrix + 'brain_mask.nii.gz -r ' + data_dir_dtifit + 'bvecs.txt -b ' + data_dir_dtifit + 'bvals.txt -w')