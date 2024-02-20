# ENSEMBLE EEG

Ensemble EEG is a library of EEG analyis tools for the ENSEMBLE study. As of
today it is focuses on 4 seperate things:

- **Anonymizing** EDF files in accordance with the ENSEMBLE study and the
  requirements of EDF+
- **Converting** BRM to EDF+ files
- **Combining** seperate aEEG channels into one EDF+ file
- **Renaming** EEG files according to ENSEMBLE and BIDS standards
- **Fixing** EDF headers to adhere to the EDF+ standard

## Installation
##### Pip
```
python3 -m pip install ensemble_eeg
```

## Usage
##### Anonymizing EDF-files
```
>>> import ensemble_eeg
>>> ensemble_eeg.anonymize_edf_header('path/2/your/edf/file')
```
##### Fixing EDF headers
```
>>> import ensemble_eeg
>>> ensemble_eeg.fix_edf_header('path/2/your/edf/file')
```
##### Converting BRM to EDF files
```
>>> import brm_to_edf
>>> brm_to_edf.convert_brm_to_edf('path/2/your/brm/file')
```
##### Combine left and right aEEG channels into one single file
```
>>> import ensemble_eeg
>>> ensemble_eeg.combine_aeeg_channels('path/2/your/left/channel', 'path/2/your/right/channel', 'new_filename')
```
##### Rename EDF-files according to BIDS and ENSEMBLE standards
```
>>> import ensemble_eeg
>>> ensemble_eeg.rename_for_ensemble('path/2/your/edf/file')
```
### Situations
##### 1) File is already EDF, but you do not know whether header is EDF+, the file is not anonymized, and not renamed
```
>>> import ensemble_eeg
>>> file = 'path/2/your/edf/file'
>>> ensemble_eeg.fix_edf_header(file)       # for header check
>>> ensemble_eeg.anonymize_edf_header(file) # for anonymization
>>> ensemble_eeg.rename_for_ensemble(file)  # for renaming

```
##### 2) File is BRM 
```
>>> import ensemble_eeg
>>> brm_file = 'path/2/your/brm/file'
>>> brm_to_edf.convert_brm_to_edf(brm_file)     # for conversion, output edf is already anonymized
>>> edf_file = 'path/2/your/edf/file'           # check which file was made in previous step
>>> ensemble_eeg.rename_for_ensemble(edf_file)  # for renaming

```
##### 3) Files are edf, but left and right channel are seperate 
```
>>> import ensemble_eeg
>>> left_file = 'path/2/your/left/edf/file'
>>> right_file = 'path/2/your/right/edf/file'
>>> ensemble_eeg.combine_aeeg_channels(left_file, right_file) # output is automatically anonymized
>>> ensemble_eeg.rename_for_ensemble(file)                    # for renaming

```


## Acknowledgements

