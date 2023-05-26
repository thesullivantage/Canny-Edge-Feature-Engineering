import cv2
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import numpy as np

import argparse
import sys
import os


def load_and_recolor_image(image_path, new_cmap='hot'):
    
    
    '''Canny Edge Detection [CHECK]:
    - [The comparision of gradients between borders of pixels] decides which are all edges are really edges and which are not. 
    - For this, we need two threshold values, minVal and maxVal. 
    - Any edges with intensity gradient more than maxVal are sure to be edges and those below minVal are sure to be non-edges, so discarded. 
    - Those who lie between these two thresholds are classified edges or non-edges based on their connectivity. 
    - If they are connected to "sure-edge" pixels, they are considered to be part of edges. 
    - Otherwise, they are also discarded.
    '''
    ### hand tune edge thresholds for individual use case
    edge_threshold1 = 500
    edge_threshold2 = 1250
    
    # Load original image (read in grayscale)
    img_original = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Normalize image to 0-1 range (float)
    img_norm = img_original.astype(float) / 255
 
    try:
        # generate colormap
        cmap = plt.get_cmap(new_cmap)
    except Exception:
        # if invalid colormap name entered for mpl, throw:
        print('please enter a valid colormap name.')
        sys.exit(1) 
        ### (see also docs for alternatives mentioned in README.md)   

    # map grayscale image to recoloring using matplotlib colormap
    colored_image = cmap(img_norm)

    # convert to float32 for cvtColor method; it expects floats to be 32-bit
    colored_image = colored_image.astype(np.float32)

    # matplotlib gives rgba images; we need to back in rgb
    colored_image_rgb = cv2.cvtColor(colored_image, cv2.COLOR_RGBA2RGB)
    
    # convert back to 0-255 pixel values for color (uint8)
    colored_image_rgb = (colored_image_rgb * 255).astype(np.uint8)
    
    # detect edges in the grayscale image conversion
    edges = cv2.Canny(img_original, edge_threshold1, edge_threshold2)
    
    # dilate the edges to create a blur for areas near high contrast (steep edge gradient) borders (OPTIONAL: DEPENDING ON DESIRED RESOLUTION)
    dilated_edges = cv2.dilate(edges, np.ones((3, 3), np.uint8))

    # make 3-channel (R,G,B) version of the mask to apply on the rgb image
    edge_mask_rgb = np.stack([dilated_edges]*3, axis=-1)

    # [OPTIONAL] edge mask applies near sharp edges, there: restore the original grayscale color in the colored image.
    ### Effect: keep sharp black and white outlines in current configuration. 
    ### BUT, also have some around i.e. spectrographic (blurred) features if not careful with thresholds. 
    img_original_rgb = cv2.cvtColor(img_original, cv2.COLOR_GRAY2RGB)

    # apply selected pixels from last step to (already) recolored pixels to "retrace solid outlines" of image features in B&W
    colored_image_rgb[edge_mask_rgb > 0] = img_original_rgb[edge_mask_rgb > 0]

    # (probably redundant) Floor white and black colors to those corresponding pixel values. 
    colored_image_rgb[img_original == 0] = 0
    colored_image_rgb[img_original == 255] = 255

    return colored_image_rgb

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--image-path", help="image path to recolor (relative to current directory).")
    parser.add_argument("--cmap-name", help="perceptually uniform sequential colormap (from matplotlib) to convert to (throws error if not a valid type).")
    parser.add_argument("--test", type=bool, help="create sample outputs of each perceptually uniform sequential colormap type, in matplotlib, in original image directory.")

    opts = parser.parse_args()

    image_path = os.path.join(os.getcwd(), opts.image_path)
    new_cmap = opts.cmap_name
    test = opts.test
    # Perceptually Uniform Sequential colormap list (matplotlib)
    cmap_list = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
    
    if test == False:
        colored_image = load_and_recolor_image(image_path, new_cmap)

        imgName = '.'.join(image_path.split('.')[:-1])
        outPath = f'{imgName}_recolored_{new_cmap}.png'
        # Display the recolored image:
        
        cv2.imwrite(outPath, cv2.cvtColor(colored_image, cv2.COLOR_RGB2BGR))
    else: 
        '''
        if we want to see samples of all colormaps which we could use from the above list on our image data,
        use --test True in the command line! Outputs all to same directory as input image (FIXME).
        '''
        for c in cmap_list:
            colored_image = load_and_recolor_image(image_path, c)

            imgName = '.'.join(image_path.split('.')[:-1])
            outPath = f'{imgName}_recolored_{c}.png'
            # Display the recolored image:
            
            cv2.imwrite(outPath, cv2.cvtColor(colored_image, cv2.COLOR_RGB2BGR))
