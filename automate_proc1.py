#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import numpy as np

directory='./'

filename=sys.argv[1]

id, date  = np.loadtxt(directory + filename, delimiter = ',', usecols=(0,1), unpack=True, dtype='object')
DTI_multi_input, DTI_negPE_input = np.loadtxt(directory + filename, delimiter = ',', usecols=(2,3),unpack=True, dtype='object')
t1_input = np.loadtxt(directory + filename, delimiter = ',', usecols=(4), unpack=True, dtype='object')

for i in range (0,len(id)):

    DTI_multi_mif=''
    DTI_multi_nifti=''
    DTI_negPE_mif=''
    DTI_negPE_nifti=''

    data_dir = directory + id[i] + '/' + date[i] + '/'
    data_dir_raw = data_dir + 'raw/'

    print(data_dir)

    os.system('mkdir -p ' + data_dir + 'raw')
    os.system('mv ' + data_dir + DTI_multi_input[i] + ' ' + data_dir_raw)
    os.system('mv ' + data_dir + DTI_negPE_input[i] + ' ' + data_dir_raw)
    os.system('mv ' + data_dir + t1_input[i] + ' ' + data_dir_raw)

    if DTI_multi_input[i].endswith(".nii.gz") or DTI_negPE_input[i].endswith(".nii.gz"):
        print("Participant: "+ id[i] + ' ' + date[i] + ' is in Nifti format. Making a copy to mif format.')

        bvec = ''
        bval = ''

        base_name = DTI_multi_input[i]
        if base_name.endswith(".nii.gz"):
            base_name = base_name[:-7]  # Remove ".nii.gz"
        elif base_name.endswith(".nii"):
            base_name = base_name[:-4]  # Remove ".nii"
        print(base_name)

        for j in os.listdir(data_dir):
            if j.endswith(".bvec") and base_name + ".bvec" in j:
                bvec=j
                os.system('mv ' + data_dir + j + ' ' + data_dir_raw)
            if j.endswith(".bval") and base_name + ".bval" in j:
                bval=j
                os.system('mv ' + data_dir + j + ' ' + data_dir_raw)
        
        print("Converting Nifti to mif format using: " + bvec + " and " + bval)

        print('mrconvert -fslgrad ' + data_dir_raw + bvec + ' ' + data_dir_raw + bval + ' ' + data_dir_raw + DTI_multi_input[i] + ' ' + data_dir_raw + 'data.mif')
        os.system('mrconvert -fslgrad ' + data_dir_raw + bvec + ' ' + data_dir_raw + bval + ' ' + data_dir_raw + DTI_multi_input[i] + ' ' + data_dir_raw + 'data.mif')
        
        DTI_multi_nifti = DTI_multi_input[i]
        DTI_negPE_nifti = DTI_negPE_input[i]

    if DTI_multi_input[i].endswith(".mif"):
        print("Participant: " + id[i] + ' is in mif format. Making a copy in Nifti.')

        os.system('mrconvert ' + data_dir_raw + DTI_negPE_input[i] + ' ' + data_dir_raw + 'data_negpe.nii.gz -stride 1,2,3')
        os.system('mrconvert ' + data_dir_raw + DTI_multi_input[i] + ' ' + data_dir_raw + 'data.nii.gz -stride 1,2,3,4')   

        os.system('mrconvert ' + data_dir_raw + DTI_multi_input[i] + ' -stride 1,2,3,4 ' + data_dir_raw + 'data.mif')

        DTI_multi_nifti = 'data.nii.gz'
        DTI_negPE_nifti = 'data_negpe.nii.gz'

    os.system('mkdir -p ' + data_dir + 'preproc')

    data_dir_preproc = data_dir + 'preproc/'

    os.system('mv ' + data_dir_raw + 'data.mif ' + data_dir_preproc + 'data.mif')

    os.system('bet ' + data_dir_raw + DTI_multi_nifti + ' ' + data_dir_preproc + 'preproc -m -n -f 0.3')
    os.system('mrconvert ' + data_dir_preproc + 'preproc_mask.nii.gz ' + data_dir_preproc + 'preproc_mask.mif')
    
    os.system('mrview ' + data_dir_preproc + 'data.mif -roi.load ' + data_dir_preproc + 'preproc_mask.mif -roi.opacity 0.4')

