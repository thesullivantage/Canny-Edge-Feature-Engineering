import cv2
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import numpy as np

import argparse
import sys
import os


def load_and_recolor_image(image_path, new_cmap='hot'):
    
    
    '''Canny Edge Detection [CHECK]:
    - Any gradient magnitude larger than the higher threshold is considered to be an edge.
    - Any gradient magnitude smaller than the lower threshold is not considered to be an edge.
    - Gradient magnitudes between the two thresholds are considered edges only if they are connected to "sure-edge" pixels (i.e., those above the higher threshold).
    thresholds of [500, 1250] set through trial and error. Feel free to set your own
    '''
    
    edge_threshold1 = 500
    edge_threshold2 = 1250
    
    # Now, load the original image (read in grayscale)
    img_original = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Normalize image to 0-1 range (float)
    img_norm = img_original.astype(float) / 255
 
    try:
        # generate colormap
        cmap = plt.get_cmap(new_cmap)
    except Exception:
        # if invalid colormap name entered, throw:
        print('please enter a valid colormap name.')
        sys.exit(1)    

    # Normalize grayscale image to the range of non-black/white colors in the colormap
    img_norm = img_original.astype(float) / 255
    ### OLD:
    # img_norm = (img_norm - min_x) / (max_x - min_x)

    # Convert grayscale image to colormap using matplotlib
    colored_image = cmap(img_norm)

    # But first convert to float32 as cvtColor expects float data to be 32-bit
    colored_image = colored_image.astype(np.float32)

    # Matplotlib returns rgba images, we need to convert to rgb
    colored_image_rgb = cv2.cvtColor(colored_image, cv2.COLOR_RGBA2RGB)
    
    # Convert back to 0-255 range (uint8)
    colored_image_rgb = (colored_image_rgb * 255).astype(np.uint8)
    # colored_image_rgb[img_original < 10] = 0
    
    # Detect edges in the original grayscale image
    edges = cv2.Canny(img_original, edge_threshold1, edge_threshold2)
    
    # Dilate the edges to create a mask for areas near high contrast borders
    dilated_edges = cv2.dilate(edges, np.ones((3, 3), np.uint8))

    # Create a 3-channel version of the mask to apply on the rgb image
    edge_mask_rgb = np.stack([dilated_edges]*3, axis=-1)

    # Wherever the mask is true (near edges), restore the original grayscale color in the colored image
    img_original_rgb = cv2.cvtColor(img_original, cv2.COLOR_GRAY2RGB)

    colored_image_rgb[edge_mask_rgb > 0] = img_original_rgb[edge_mask_rgb > 0]

    # assure that white and black colors stay the same 
    colored_image_rgb[img_original == 0] = 0
    colored_image_rgb[img_original == 255] = 255

    return colored_image_rgb

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--image-path", help="Image to recolor")
    parser.add_argument("--cmap-name", help="Colormap to convert to")

    opts = parser.parse_args()

    image_path = os.path.join(os.getcwd(), opts.image_path)
    new_cmap = opts.cmap_name
    colored_image = load_and_recolor_image(image_path, new_cmap)

    imgName = '.'.join(image_path.split('.')[:-1])
    outPath = f'{imgName}_recolored_{new_cmap}.png'
    # Display the recolored image:
    
    cv2.imwrite(outPath, cv2.cvtColor(colored_image, cv2.COLOR_RGB2BGR))
