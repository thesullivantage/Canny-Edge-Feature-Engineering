# Spectrogram Recoloring Script 

### Description
Python script which recolors spectrographic images via:
- Conversion to grayscale
- Applying a chosen Matplotlib colorsmap as a mask
- Applying applying Canny edge detection and dilating the image regions around found edge locations, found in the grayscale representation, to reduce smudging.
- The flooring of the recolored image, in detected white or black regions, to those colors (perhaps redundantly).

### Usage
1. 
```bash
cd repositoryName/
pip install -r requirements.txt # to install required dependencies
```

2. After running:
```bash
python recolorimage.py --help
```
We can see the possible arguments:
```
usage: recolorimage.py [-h] [--image-path IMAGE_PATH] [--cmap-name CMAP_NAME] [--test TEST]
options:
  -h, --help            show this help message and exit
  --image-path IMAGE_PATH
                        image path to recolor (relative to current directory).
  --cmap-name CMAP_NAME
                        perceptually uniform sequential colormap (from matplotlib) to convert to (throws error if not a valid type).
  --test TEST           create sample outputs of each perceptually uniform sequential colormap type, in matplotlib, in original image directory.
```
