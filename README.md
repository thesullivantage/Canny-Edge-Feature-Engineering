# Heatmap Recoloring & Edge Detection for ML Feature Engineering using OpenCV

### Description
Python script which recolors spectrographic images (or heatmaps) using the OpenCV Python package, in the following steps:
- Convert image to grayscale
- Applying  Canny edge detection and slightly dilating the image regions around found edge locations (optional), found in the grayscale representation, to reduce smudging and pre-process images for segmentation models.
- Overlay found edges in black & white atop the color image.
---

## Usage
1. Run:
```bash
cd repositoryName/
pip install -r requirements.txt # to install required dependencies
```

2. After running:
```bash
python recolorimage.py --help
```
We can see the possible options:
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
It may be a good option to try all possibilities using the test flag!

3. Change the edge detection margins in the script as you find useful for your images, here:
```python
def load_and_recolor_image(image_path, new_cmap='hot'):
    edge_threshold1 = 500
    edge_threshold2 = 1250
``` 
4. Substitute some your desired, alternative colormaps at this point of the script
```python
    try:
        # generate colormap
        cmap = plt.get_cmap(new_cmap)
    except Exception:
        # if invalid colormap name entered, throw:
        print('please enter a valid colormap name.')
        sys.exit(1) 
```
by consulting the [Matplotlib Colormap Documentation](https://matplotlib.org/stable/tutorials/colors/colormaps.html)

---
### More on Canny Edge Detection (from the [OpenCV Docs](https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html)):
- [The comparision of gradients between borders of pixels] decides which are all edges are really edges and which are not. 
- For this, we need two threshold values, minVal and maxVal. [hysterisis-based inclusion]
- Any edges with intensity gradient more than maxVal are sure to be edges and those below minVal are sure to be non-edges, so discarded. 
- Those who lie between these two thresholds are classified edges or non-edges based on their connectivity. 
    - If they are connected to "sure-edge" pixels, they are considered to be part of edges. 
    - Otherwise, they are also discarded.

