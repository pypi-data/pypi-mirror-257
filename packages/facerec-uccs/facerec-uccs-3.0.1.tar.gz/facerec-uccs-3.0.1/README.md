Watchlist Challange: 3rd Open-set Face Detection and Identification Challenge
===============================================================================

This package implements the baseline algorithms and evaluation for the third version of the UCCS challange.

## Dataset
-------

This package does not include the original image and protocol files for the competition.

## Installation

The installation of this package follows via conda

Install via conda:
```bash
    conda env create -f environment.yaml
    conda activate uccs-facerec
```

## Scripts

There are four scripts to run the baseline. All scripts will be installed together with this package.
Their sources can be found in `facerec/script`.


### Face detection
  The first script is a face detection script, which will detect the faces in the validation (and test) set.
  You can call the face detector baseline script using:
  ``baseline_detection.py``

### Face identification
  For face recognition, we utilize the `MTCNN` face detector to detect all the faces (see above) and make sure that the bounding boxes with the highest overlap to the ground truth labels are used.
  You can call the face detector baseline script using:
  ``baseline_recognition.py``

### Scoring
  ``scoring.py``

### Evaluation
  ``evaluation.py``
