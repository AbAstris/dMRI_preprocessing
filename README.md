# dMRI_preprocessing

This repository contains python scripts to pre-process and fit models to diffusion MRI data, specifically constrained spherical deconvolution (CSD) and diffusion tensor imaging (DTI) models. Software requirements are [MRtrix3](https://www.mrtrix.org/) and [FSL](https://fsl.fmrib.ox.ac.uk/fsl/docs/#/). This script has primarily been tested using [Python 3.11](https://www.python.org/downloads/release/python-3110/).

There are 3 main Python scripts (which should be run consecutively):

1. **automate_proc1.py**: The first script is designed to read in a CSV file of information for multiple subjects. Using this file, the script will establish that the image data, originally in either MIF (.mif) or NIfTI (.nii.gz), is in the same format and in the correct location by creating a 'raw' folder under each subject directory. A brain mask will also be generated and checked at this point for future pre-processing steps.

2. **automate_proc2.py**: The second script runs image denoising, removes Gibbs ringing artefacts, uses `topup` to correct for susceptibility-induced distortions in EPI images and uses `eddy` to correct for eddy current-induced distortions (from rapidly switching diffusion gradients), subject motion and slice-wise signal dropout.

3. **automate_proc3.py**: The final script runs CSD and DTI models to fit the diffusion data, which can be used for further analysis (e.g. tractography or TBSS).

Each Python script requires a CSV file of the subjects (each row is a subject). An example of the column structure is:
```
Subject_ID_1,Scan_Date_1,diffusion_data_1.mif,diffusion_negpe_1.mif,t1map_1.mif
Subject_ID_2,Scan_Date_2,diffusion_data_2.mif,diffusion_negpe_2.mif,t1map_2.mif
Subject_ID_3,Scan_Date_3,diffusion_data_3.mif,diffusion_negpe_3.mif,t1map_3.mif
```
where the columns correspond to the following:
* Subject_ID_1: This is the subject ID.
* Scan_Date_1: This is the scan date.
* diffusion_data_1.mif (or .nii.gz): This is the raw diffusion data in either .mif or .nii.gz format. If NIfTI format is used, then the corresponding b-value and b-vector files should be in `.bval` and `.bvec` formats.
* diffusion_negpe_1.mif (or .nii.gz): This is the raw negative (reversed) phase encoding image with either .mif or .nii.gz format.
* t1map_1.mif (or .nii.gz): This is a T1-weighted image that should be included for each subject. While it is not used in this script, it is useful for other analyses.

The directory structure should be as follows to run the code:

```
project_folder/
├── automate_proc1.py
├── automate_proc2.py
├── automate_proc3.py
├── subject_info.csv
├── Subject_ID_1/
│   ├── Scan_Date_1/
│   │   ├── diffusion_data_1.mif
│   │   ├── diffusion_negpe_1.mif
│   │   └── t1map_1.mif
├── Subject_ID_2/
│   └── Scan_Date_2/
│       ├── diffusion_data_2.mif
│       ├── diffusion_negpe_2.mif
│       └── t1map_2.mif
└── Subject_ID_3/
    └── Scan_Date_3/
        ├── diffusion_data_3.mif
        ├── diffusion_negpe_3.mif
        └── t1map_3.mif
```
