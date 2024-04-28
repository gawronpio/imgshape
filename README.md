# imgshape - Pictures shape distribution plot

### Description

The program checks the shapes of images in the given directory and plots the distribution of these shapes.

### Usage

imgshape [-h] [-i INPUTDIR] [-R] [-S] [-r READ] [-s SAVE]

options:
- -h, --help -- show this help message and exit
- -i INPUTDIR, --inputdir INPUTDIR -- Input directory with images to check the shape of the images.
- -R, --recursive -- Check images in all subdirectories.
- -S, --followsymlinks -- Follow directories pointed to by symbolic links when searching for images.
- -r READ, --read READ -- Reads list of shapes from file instead of checking images.
- -s SAVE, --save SAVE -- Saves list of shapes to CSV file
